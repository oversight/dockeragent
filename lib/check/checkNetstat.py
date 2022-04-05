import os

from .base import Base


class CheckNetstat(Base):
    api_call = '/containers/json'
    interval = int(os.getenv('OSDA_CHECK_NETSTAT_INTERVAL', 300))
    type_name = 'netstat'

    @staticmethod
    def on_item(itm):
        return {
            'name': itm['Id']
        }
