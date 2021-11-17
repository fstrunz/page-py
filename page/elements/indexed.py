from abc import ABC
from typing import TypeVar, Generic, Dict, Optional

ObjectTy = TypeVar("ObjectTy")


class IndexedElement(Generic[ObjectTy], ABC):
    """Represents an element which can contain indexed subelements
    of type ObjectTy, providing an efficient get_from_index method.

    This class assumes that the inheriting subclasses are immutable!"""

    def __init__(self, index: Dict[int, ObjectTy]):
        self.__index = index.copy()

    def get_from_index(self, index: int) -> Optional[ObjectTy]:
        if index in self.__index:
            return self.__index[index]
        else:
            return None
