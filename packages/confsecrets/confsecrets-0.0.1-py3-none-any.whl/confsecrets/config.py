"""
Implements Configuration of confsecrets
"""
from enum import Enum

__all__ = (
    'Config',
)


class Config(Enum):
    """
    Things that may appear in environment or settings
    """
    SALT = 'CONFSECRETS_SALT'
    KEY = 'CONFSECRETS_KEY'
    PATH = 'CONFSECRETS_PATH'
