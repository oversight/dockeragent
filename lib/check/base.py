import asyncio
import logging
import re

import aiohttp

from ..logger import setup_logger


URL_RE = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|'
    r'[A-Z0-9-]{2,}\.?)|'  # domain
    r'localhost|'  # localhost
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


class Base:

    address = None
    api_version = 'v1.41'
    interval = 300
    type_name = None

    @classmethod
    async def run(cls):
        try:
            state_data = await cls.get_data()
        except asyncio.TimeoutError:
            raise Exception('Check timed out.')
        except Exception as err:
            raise Exception(f'Check error: {err.__class__.__name__}: {err}')
        else:
            return state_data

    @classmethod
    async def get_data(cls):
        data = None
        try:
            data = await cls.run_check()
        except Exception as err:
            logging.exception(f'Docker error: `{err}`\n')
            raise

        try:
            state = cls.iterate_results(data)
        except Exception as err:
            logging.exception(f'Dockeragent parse error: `{err}`\n')
            raise

        return state

    @classmethod
    async def run_check(cls):
        if cls.interval == 0:
            raise Exception(f'{cls.__name__} is disabled')
        await asyncio.sleep(cls.interval)  # TODO is this right?
        # TODO asyncio.wait_for?
        return await cls.dockerApiCall(cls.api_call)

    @classmethod
    async def dockerApiCall(cls, query):
        url = f'http://{cls.api_version}' + query
        async with aiohttp.ClientSession(connector=cls.get_conn()) as session:
            async with session.get(url) as resp_data:
                return await resp_data.json()

    @classmethod
    def get_conn(cls):
        address = '/var/run/docker.sock' if cls.address is None \
            else cls.address

        if URL_RE.match(address):
            raise NotImplementedError()
            # TODO should this be implemented?
            # return aiohttp.TCPConnector(address)

        return aiohttp.UnixConnector(path=address)

    @staticmethod
    def on_item(itm):
        return itm

    @classmethod
    def on_items(cls, itms):
        out = {}
        for i in itms:
            itm = cls.on_item(i)
            name = itm['name']
            out[name] = itm
        return out

    @classmethod
    def iterate_results(cls, data):
        if type(data) is not list:
            data = [data]

        itms = cls.on_items(data)
        state = {}
        state[cls.type_name] = itms
        return state