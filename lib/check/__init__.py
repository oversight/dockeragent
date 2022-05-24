from .checkContainers import CheckContainers
from .checkImages import CheckImages
from .checkStats import CheckStats
from .checkSystem import CheckSystem


CHECKS = {
    'CheckContainers': CheckContainers,
    'CheckImages': CheckImages,
    'CheckStats': CheckStats,
    'CheckSystem': CheckSystem
}
