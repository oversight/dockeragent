import os

from .base import Base


class CheckContainers(Base):
    api_call = '/containers/json?all=true,size=true'
    interval = int(os.getenv('OSDA_CHECK_CONTAINERS_INTERVAL', 300))
    type_name = 'netio'

    @staticmethod
    def on_item(itm):
        return {
            'name': itm['Id']
        }
