import os

from .base import Base
from .utils import format_list


class CheckContainers(Base):
    # Query parameters
    # all (boolean; false):
    # Return all containers. By default, only running containers are shown.
    # size (boolean; false):
    # Return the size of container as fields SizeRw and SizeRootFs.
    api_call = '/containers/json?all=true'  # &size=true'
    interval = int(os.getenv('OSDA_CHECK_CONTAINERS_INTERVAL', '300'))

    @staticmethod
    def format_name(names: list):
        return names[0][1:]

    @staticmethod
    def format_port(port: dict):
        return (
            f"{port['IP']}:{port['PrivatePort']}"
            f"->{port['PublicPort']}/{port['Type']}"
        )

    @classmethod
    def on_item_containers(cls, itm: dict):
        resp_data = {
            'id': itm['Id'],
            'name': cls.format_name(itm['Names']),
            'names': format_list(itm['Names']),
            'image': itm['Image'],
            'imageId': itm['ImageID'],
            'command': itm['Command'],
            'created': itm['Created'],
            'state': itm['State'],
            'status': itm['Status'],
            'ports': format_list(
                [cls.format_port(port) for port in itm['Ports']])
        }

        network_mode = itm.get('HostConfig', {}).get('NetworkMode', None)
        if network_mode is not None:
            resp_data['networkMode'] = network_mode
        return resp_data

    @classmethod
    def on_item_networks(cls, itm: dict):
        network_data = {}
        container_name = cls.format_name(itm['Names'])
        for k, v in itm.get('NetworkSettings', {}).get('Networks', {}).items():
            name = f'{container_name}_{k}'
            network_data[name] = {
                'name': name,
                'networkId': v['NetworkID'],
                'endpointId': v['EndpointID'],
                'gateway': v['Gateway'],
                'ipAddress': v['IPAddress'],
                'ipPrefixLen': v['IPPrefixLen'],
                'ipv6Gateway': v['IPv6Gateway'],
                'globalIpv6Address': v['GlobalIPv6Address'],
                'MacAddress': v['MacAddress'],
                'driverOpts': v['DriverOpts'],
                'aliases': v['Aliases'],
                'links': v['Links'],
                'ipamConfig': v['IPAMConfig']
            }
        return network_data

    @classmethod
    def iterate_results(cls, data: list):
        out = {
            'containers': {},
            'networks': {},
        }
        for i in data:
            itm_c = cls.on_item_containers(i)
            name_c = itm_c['name']
            out['containers'][name_c] = itm_c

            itm_n = cls.on_item_networks(i)
            out['networks'] = {**out['networks'], **itm_n}

        return out
