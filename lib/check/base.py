import asyncio
import re

import aiohttp


URL_RE = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|'
    r'[A-Z0-9-]{2,}\.?)|'  # domain
    r'localhost|'  # localhost
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


class Base:

    api_call = ''
    api_version = 'v1.41'
    interval = 300
    type_name = None

    @classmethod
    async def run(cls):
        if cls.interval == 0:
            raise Exception(f'{cls.__name__} is disabled')

        data = await asyncio.wait_for(
            cls.get_data(cls.api_call),
            timeout=60.0  # 60 seconds
        )
        state_data = cls.iterate_results(data)
        return state_data

    @classmethod
    async def get_data(cls, query: str):
        return await cls.docker_api_call(query)

    @classmethod
    async def docker_api_call(cls, query: str):
        url = f'http://{cls.api_version}' + query
        async with aiohttp.ClientSession(connector=cls.get_conn()) as session:
            async with session.get(url) as resp_data:
                return await resp_data.json()

    @classmethod
    def get_conn(cls):
        address = '/var/run/docker.sock'

        if URL_RE.match(address):
            raise NotImplementedError('TCP connector is not implemented')

        return aiohttp.UnixConnector(path=address)

    @staticmethod
    def on_item(itm: dict):
        return itm

    @classmethod
    def on_items(cls, itms: list):
        out = {}
        for i in itms:
            itm = cls.on_item(i)
            name = itm['name']
            out[name] = itm
        return out

    @classmethod
    def iterate_results(cls, data: list):
        itms = cls.on_items(data)
        state = {}
        state[cls.type_name] = itms
        return state
