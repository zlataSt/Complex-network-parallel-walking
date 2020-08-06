""" Global values."""

from cache import LRUCache
from typing import List

# Объявление списка траекторий
TRAJECTORIES: List = []

# Обычный кэш
CACHE = LRUCache(1000)

# Хвостовой кэш
TAIL_CACHE = LRUCache(500)

HANDLERS: List = []

COUNT_EXCHANGED = 0
COUNT_MERGES = 0
COUNT_CREATED_HANDLERS =0
