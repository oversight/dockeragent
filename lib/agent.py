import asyncio
import logging
import os

import aiohttp


class Agent:

    def __init__(
        self,
        probe_name: str,
        version: str,
        checks: dict,
    ):
        self._loop = asyncio.get_event_loop()
        self._probe_name = probe_name
        self._probe_version = version
        self._checks = checks
        self._required_services = [
            c.__name__
            for c in checks.values()
            if getattr(c, 'required', False)
        ]

        self.token = os.getenv('OSDA_TOKEN', None)
        self.environment_uuid = int(os.getenv('OSDA_ENVIRONMENT_UUID', '0'))
        self.host_uuid = int(os.getenv('OSDA_HOST_UUID', '0'))
        self.api_uri = os.getenv('OSDA_API_URI', 'https://oversig.ht/api')

    async def send_data(self, check_name, check_data):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

        url = os.path.join(self.api_uri, '/data/insert')
        data = {
            "environmentUuid": self.environment_uuid,
            "hostUuid": self.host_uuid,
            "probe": self._probe_name,
            "check": check_name,
            "data": check_data
        }
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.post(url, json=data) as r:
                    if r.status != 200:
                        logging.warning(
                            'Got unexpected response status from ' +
                            f'{self.api_uri} {self._probe_name}.{check_name}' +
                            f': {r.status}')
        except aiohttp.ClientConnectorError as e:
            logging.warning(
               f'Failed to send data of {self._probe_name}.{check_name} ' +
               f'to {self.api_uri}: `{e}`')

    async def run_agent(self):
        if None in (self.token, self.api_uri) or \
                0 in (self.environment_uuid, self.host_uuid):
            logging.error('invalid check configuration')
            return

        checks = [self.on_run_check_loop(c) for c in self._checks.values()]
        await asyncio.wait(checks)

    async def on_run_check_loop(self, check):
        while 1:
            try:
                check_data = await check.run()
                await self.send_data(check.__name__, check_data)
            except Exception as err:
                logging.error(
                    f'Check error: {err.__class__.__name__}: {err}')
            finally:
                await asyncio.sleep(check.interval)
