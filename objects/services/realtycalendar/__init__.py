__version__ = '1.0.0'
__author__ = 'EdvardKenua'

from . import models
from . import viewmodels

__all__ = [
    "models", "viewmodels"
]



import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
logger.info("Инициализация пакета %s v%s", __name__, __version__)