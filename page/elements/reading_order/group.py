from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Tuple, Union
from lxml import etree

from page.elements import Element
from page.elements.region_ref import RegionRef
from page.constants import NsMap
from page.exceptions import PageXMLError


@dataclass
class Group(Element, ABC):
    """A group inside a ReadingOrder."""
    group_id: str
    children: List[Union["Group", RegionRef]]
    caption: Optional[str]

    def _from_element(
        group_xml: etree.ElementBase, tag_name: str
    ) -> Tuple[str, Optional[str]]:
        group_id = group_xml.get("id")
        if group_id is None:
            raise PageXMLError(f"{tag_name} is missing an id attribute")

        caption = group_xml.get("caption")
        return group_id, caption

    @staticmethod
    @abstractmethod
    def from_element(group_xml: etree.ElementBase, nsmap: NsMap) -> "Group":
        pass

    @abstractmethod
    def to_element(self, nsmap: NsMap) -> etree.ElementBase:
        pass


@dataclass
class GroupIndexed(Group, Element, ABC):
    """A subgroup which may appear inside an OrderedGroup."""
    index: int

    @staticmethod
    @abstractmethod
    def from_element(
        group_xml: etree.ElementBase, nsmap: NsMap
    ) -> "GroupIndexed":
        pass

    @abstractmethod
    def to_element(self, nsmap: NsMap) -> etree.ElementBase:
        pass
