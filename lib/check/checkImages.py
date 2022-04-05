import os

from .base import Base


class CheckImages(Base):
    api_call = '/images/json?all=false'
    interval = int(os.getenv('OSDA_CHECK_IMAGES_INTERVAL', 300))
    type_name = 'images'

    @staticmethod
    def on_item(itm):
        return {
            'name': itm['Id']
        }
