from .checkContainers import CheckContainers
from .checkImages import CheckImages
from .checkSystem import CheckSystem


CHECKS = {
    'CheckContainers': CheckContainers,
    'CheckImages': CheckImages,
    'CheckSystem': CheckSystem
}
