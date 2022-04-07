import os

from .base import Base
from .utils import get_ts_from_time_str


class CheckSystem(Base):
    api_call = '/info'
    interval = int(os.getenv('OSDA_CHECK_SYSTEM_INTERVAL', 300))
    type_name = 'system'

    @staticmethod
    def on_item(itm):
        return {
            'id': itm['ID'],
            'containers': itm['Containers'],
            'containersRunning': itm['ContainersRunning'],
            'containersPaused': itm['ContainersPaused'],
            'containersStopped': itm['ContainersStopped'],
            'images': itm['Images'],
            'driver': itm['Driver'],
            'systemStatus': str(itm['SystemStatus']),
            'memoryLimit': itm['MemoryLimit'],
            'swapLimit': itm['SwapLimit'],
            'kernelMemory': itm['KernelMemory'],
            'kernelMemoryTCP': itm['KernelMemoryTCP'],
            'cpuCfsPeriod': itm['CpuCfsPeriod'],
            'cpuCfsQuota': itm['CpuCfsQuota'],
            'cpuShares': itm['CPUShares'],
            'cpuSet': itm['CPUSet'],
            'pidsLimit': itm['PidsLimit'],
            'ipv4Forwarding': itm['IPv4Forwarding'],
            'bridgeNfIptables': itm['BridgeNfIptables'],
            'bridgeNfIp6tables': itm['BridgeNfIp6tables'],
            'debug': itm['Debug'],
            'oomKillDisable': itm['OomKillDisable'],
            'nGoroutines': itm['NGoroutines'],
            'systemTime': get_ts_from_time_str(itm['SystemTime']),
            'loggingDriver': itm['LoggingDriver'],
            'nEventsListener': itm['NEventsListener'],
            'kernelVersion': itm['KernelVersion'],
            'operatingSystem': itm['OperatingSystem'],
            'osType': itm['OSType'],
            'architecture': itm['Architecture'],
            'indexServerAddress': itm['IndexServerAddress'],
            'nCpu': itm['NCPU'],
            'memTotal': itm['MemTotal'],
            'genericResources': str(itm['GenericResources']),
            'dockerRootDir': itm['DockerRootDir'],
            'httpProxy': itm['HttpProxy'],
            'httpsProxy': itm['HttpsProxy'],
            'noProxy': itm['NoProxy'],
            'name': itm['Name'],
            'experimentalBuild': itm['ExperimentalBuild'],
            'serverVersion': itm['ServerVersion'],
            'clusterStore': itm['ClusterStore'],
            'clusterAdvertise': itm['ClusterAdvertise'],
            'defaultRuntime': itm['DefaultRuntime'],
            'liveRestoreEnabled': itm['LiveRestoreEnabled'],
            'isolation': itm['Isolation'],
            'initBinary': itm['InitBinary'],
            # TODO check '-character needs to be removed from string:
            # "['Warning1', 'Warning2']"
            'warnings': str(itm['Warnings'])  # .replace('\'', ''),
        }
