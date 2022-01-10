from abc import ABC
from dataclasses import dataclass
from typing import List, Optional

from page.elements.indexed import IndexedElement


@dataclass
class Group(ABC):
    """A group inside a ReadingOrder."""
    group_id: str
    children: List["Group"]
    caption: Optional[str]


@dataclass
class GroupIndexed(Group):
    """A subgroup which may appear inside an OrderedGroup."""
    index: int


class OrderedGroup(Group, IndexedElement[int, GroupIndexed]):
    def __init__(
        self, group_id: str, children: List[GroupIndexed],
        caption: Optional[str] = None
    ):
        super(Group, self).__init__(children, lambda group: group.index)
        super().__init__(group_id, caption)


class OrderedGroupIndexed(OrderedGroup, GroupIndexed):
    def __init__(
        self, group_id: str, children: List[GroupIndexed],
        index: int, caption: Optional[str] = None
    ):
        super(OrderedGroup, self).__init__(index)
        super().__init__(group_id, children, caption=caption)


class UnorderedGroup(Group):
    def __init__(
        self, group_id: str, children: List[Group],
        caption: Optional[str] = None
    ):
        super().__init__(group_id, children, caption)


class UnorderedGroupIndexed(UnorderedGroup, GroupIndexed):
    def __init__(
        self, group_id: str, children: List[Group],
        index: int, caption: Optional[str] = None
    ):
        super(UnorderedGroup, self).__init__(index)
        super().__init__(group_id, children, caption)


@dataclass
class RegionRef(Group):
    region_ref: str

    def __init__(
        self, group_id: str, region_ref: str
    ):
        super().__init__(group_id, [], None)
        self.region_ref = region_ref


class RegionRefIndexed(RegionRef, GroupIndexed):
    def __init__(
        self, group_id: str, index: int, region_ref: str
    ):
        super(RegionRef, self).__init__(index)
        super().__init__(group_id, region_ref)
