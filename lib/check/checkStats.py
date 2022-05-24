import os

from .base import Base
from .utils import format_name


class CheckStats(Base):
    api_call = '/containers/json'  # To get container ids
    interval = int(os.getenv('OSDA_CHECK_STATS_INTERVAL', '300'))

    @staticmethod
    def calculate_memory_percentage(stats):
        memory_stats = stats['memory_stats']

        used_memory = memory_stats['usage'] - memory_stats['stats']['cache']
        return (used_memory / memory_stats['limit']) * 100.0

    @staticmethod
    def calculate_cpu_percentage(stats):
        cpu_stats = stats['cpu_stats']
        cpu_usage = cpu_stats['cpu_usage']
        precpu_stats = stats['precpu_stats']
        precpu_usage = precpu_stats['cpu_usage']

        cpu_delta = cpu_usage['total_usage'] - precpu_usage['total_usage']
        system_cpu_delta = cpu_stats['system_cpu_usage'] - \
            precpu_stats['system_cpu_usage']
        number_cpus = len(cpu_usage['percpu_usage'])
        return (cpu_delta / system_cpu_delta) * number_cpus * 100.0

    @classmethod
    async def get_data(cls, query: str):
        # 1. get container ids
        containers = await cls.docker_api_call(query)
        stats = []
        for container in containers:
            container_id = container['Id']
            query = f'/containers/{container_id}/stats?stream=false'
            # 2. get stats per container
            s = await cls.docker_api_call(query)
            s['name'] = format_name(container['Names'])
            stats.append(s)
        return stats

    @classmethod
    def on_item_memory(cls, itm: dict):
        resp_data = {
            'name': itm['name'],
            'percentUsed': cls.calculate_memory_percentage(itm),
        }
        return resp_data

    @classmethod
    def on_item_cpu(cls, itm: dict):
        resp_data = {
            'name': itm['name'],
            'percentUsed': cls.calculate_cpu_percentage(itm),
        }
        return resp_data

    @classmethod
    def iterate_results(cls, data: list):
        out = {
            'memory': {},
            'cpu': {},
        }
        for i in data:
            itm_m = cls.on_item_memory(i)
            name_m = itm_m['name']
            out['memory'][name_m] = itm_m

            itm_c = cls.on_item_cpu(i)
            name_c = itm_c['name']
            out['cpu'][name_c] = itm_c
        return out
