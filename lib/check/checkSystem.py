import os

from .base import Base
from .utils import get_ts_from_time_str, format_list


class CheckSystem(Base):
    api_call = '/info'
    interval = int(os.getenv('OSDA_CHECK_SYSTEM_INTERVAL', '300'))
    type_name = 'system'

    @staticmethod
    def on_item(itm: dict):
        return {
            'id': itm['ID'],
            'containers': itm['Containers'],
            'containersRunning': itm['ContainersRunning'],
            'containersPaused': itm['ContainersPaused'],
            'containersStopped': itm['ContainersStopped'],
            'images': itm['Images'],
            'driver': itm['Driver'],
            # SystemStatus is omitted if the field is not set
            # https://github.com/moby/moby/pull/40340
            'systemStatus': str(itm.get('SystemStatus', None)),
            'memoryLimit': itm['MemoryLimit'],
            'swapLimit': itm['SwapLimit'],
            'kernelMemory': itm['KernelMemory'],
            'kernelMemoryTCP': itm['KernelMemoryTCP'],
            'cpuCfsPeriod': itm['CpuCfsPeriod'],
            'cpuCfsQuota': itm['CpuCfsQuota'],
            'cpuShares': itm['CPUShares'],
            'cpuSet': itm['CPUSet'],
            'pidsLimit': itm['PidsLimit'],
            'ipv4Forwarding': itm['IPv4Forwarding'],
            'bridgeNfIptables': itm['BridgeNfIptables'],
            'bridgeNfIp6tables': itm['BridgeNfIp6tables'],
            'debug': itm['Debug'],
            'oomKillDisable': itm['OomKillDisable'],
            'nGoroutines': itm['NGoroutines'],
            'systemTime': get_ts_from_time_str(itm['SystemTime']),
            'loggingDriver': itm['LoggingDriver'],
            'nEventsListener': itm['NEventsListener'],
            'kernelVersion': itm['KernelVersion'],
            'operatingSystem': itm['OperatingSystem'],
            'osType': itm['OSType'],
            'architecture': itm['Architecture'],
            'indexServerAddress': itm['IndexServerAddress'],
            'nCpu': itm['NCPU'],
            'memTotal': itm['MemTotal'],
            'genericResources': str(itm['GenericResources']),
            'dockerRootDir': itm['DockerRootDir'],
            'httpProxy': itm['HttpProxy'],
            'httpsProxy': itm['HttpsProxy'],
            'noProxy': itm['NoProxy'],
            'name': itm['Name'],
            'experimentalBuild': itm['ExperimentalBuild'],
            'serverVersion': itm['ServerVersion'],
            'clusterStore': itm.get('ClusterStore', None),
            'clusterAdvertise': itm.get('ClusterAdvertise', None),
            'defaultRuntime': itm['DefaultRuntime'],
            'liveRestoreEnabled': itm['LiveRestoreEnabled'],
            'isolation': itm['Isolation'],
            'initBinary': itm['InitBinary'],
            'warnings': format_list(itm['Warnings'])
        }

    @classmethod
    def iterate_results(cls, data: dict):
        itm = cls.on_item(data)
        name = itm['name']
        state = {}
        state[cls.type_name] = {name: itm}
        return state
