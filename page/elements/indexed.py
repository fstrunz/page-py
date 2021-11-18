from abc import ABC
from typing import Callable, Hashable, TypeVar
from typing import Generic, Dict, Optional, List, Iterable

from page.exceptions import PageXMLError

IndexTy = TypeVar("IndexTy", bound=Hashable)
ObjectTy = TypeVar("ObjectTy")


class IndexedElement(Generic[IndexTy, ObjectTy], ABC):
    """Represents an element which can contain indexed subelements ("objects")
    of type ObjectTy, providing an efficient get_from_index(IndexTy) method.

    This class assumes that the inheriting subclasses are immutable."""

    def __init__(
        self, objects: List[ObjectTy],
        index_from_obj: Callable[[ObjectTy], Optional[IndexTy]]
    ):
        self.__index_from_obj: Callable[[ObjectTy], Optional[IndexTy]] = (
            index_from_obj
        )
        self.__index = self.__build_index(objects)

    def __build_index(
        self, objects: List[ObjectTy]
    ) -> Dict[IndexTy, ObjectTy]:
        index: Dict[IndexTy, ObjectTy] = {}

        for obj in objects:
            idx = self.__index_from_obj(obj)

            if idx is None:
                # This error occurs for example when an IndexedElement such as
                # a Line, Word or a Glyph contains multiple TextEquivs (or
                # analogous indexed object) without giving them indices.
                #
                # When no indices are present, such tags can only contain
                # at most one TextEquiv element.
                raise PageXMLError("IndexedElement object is missing an index")

            index[idx] = obj  # Allowed because IndexTy is Hashable.

        return index

    def objects(self) -> Iterable[ObjectTy]:
        return self.__index.values()

    def get_from_index(self, index: int) -> Optional[ObjectTy]:
        if index in self.__index:
            return self.__index[index]
        else:
            return None
