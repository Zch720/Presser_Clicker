import os
import sys
from typing import Callable, Any

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, 'resources', relative_path)


def getIndexInList(list: list[Any], compare: Callable[[Any], bool]):
    for index, data in enumerate(list):
        if compare(data):
            return index
    return -1


def moveListItemIndex(list: list[Any], origin: int, dist: int):
    item = list[origin]
    list.remove(item)
    list.insert(dist, item)
