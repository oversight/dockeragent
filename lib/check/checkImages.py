import asyncio
import os

from .base import Base


class CheckImages(Base):
    interval = int(os.getenv('OSDA_CHECK_IMAGES_INTERVAL', 300))
    type_name = 'images'
    api_call = '/images/json?all=false'

    @staticmethod
    def on_item(itm):
        return {
            'name': itm['Id']
        }
