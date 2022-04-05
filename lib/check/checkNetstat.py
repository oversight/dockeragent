import asyncio
import os

from .base import Base


class CheckNetstat(Base):
    interval = int(os.getenv('OSDA_CHECK_NETSTAT_INTERVAL', 300))
    type_name = 'netstat'
    api_call = '/containers/json'

    @staticmethod
    def on_item(itm):
        return {
            'name': itm['Id']
        }
