from .checkContainers import CheckContainers
from .checkImages import CheckImages
from .checkNetstat import CheckNetstat
from .checkSystem import CheckSystem


CHECKS = {
    'CheckContainers': CheckContainers,
    'CheckImages': CheckImages,
    'CheckNetstat': CheckNetstat,
    'CheckSystem': CheckSystem
}
