import os

from .base import Base
from .utils import format_list_to_str


class CheckImages(Base):
    api_call = '/images/json?all=false'
    interval = int(os.getenv('OSDA_CHECK_IMAGES_INTERVAL', '300'))
    type_name = 'images'

    @classmethod
    def on_item(itm: dict):
        resp_data = {
            'created': itm['Created'],
            'name': itm['Id'],
            'parentId': itm['ParentId'],
            'repoDigests': format_list_to_str(itm['RepoDigests']),
            'repoTags': format_list_to_str(itm['RepoTags']),
            'size': itm['Size'],
            'virtualSize': itm['VirtualSize'],
        }

        containers = itm['Containers']
        shared_size = itm['SharedSize']

        if containers != -1:
            resp_data['containers'] = containers
        if shared_size != -1:
            resp_data['sharedSize'] = shared_size

        return resp_data
