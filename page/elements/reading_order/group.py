from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Tuple
from lxml import etree

from page.elements import Element
from page.elements.indexed import IndexedElement
from page.constants import NsMap
from page.exceptions import PageXMLError
from page.elements.reading_order import RegionRef, RegionRefIndexed


@dataclass
class Group(Element, ABC):
    """A group inside a ReadingOrder."""
    group_id: str
    children: List["Group"]
    refs: List[RegionRef]
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


class OrderedGroup(Group, IndexedElement[int, GroupIndexed]):
    def __init__(
        self, group_id: str, children: List[GroupIndexed],
        refs: List[RegionRefIndexed], caption: Optional[str] = None
    ):
        # TODO: Make the RegionRefs indexed too.
        super(Group, self).__init__(children, lambda group: group.index)
        super().__init__(group_id, refs, caption)

    @staticmethod
    def from_element(
        group_xml: etree.ElementBase, nsmap: NsMap
    ) -> "OrderedGroup":
        group_id, caption = super()._from_element(group_xml, "OrderedGroup")
        children: List[GroupIndexed] = []

        for ogi_xml in group_xml.findall(
            "./OrderedGroupIndexed", namespaces=nsmap
        ):
            children.append(OrderedGroupIndexed.from_element(ogi_xml, nsmap))

        for ugi_xml in group_xml.findall(
            "./UnorderedGroupIndexed", namespaces=nsmap
        ):
            children.append(UnorderedGroupIndexed.from_element(ugi_xml, nsmap))

        # TODO: Read refs.

        return OrderedGroup(group_id, children, [], caption)

    def to_element(self, nsmap: NsMap) -> etree.ElementBase:
        og_xml = etree.Element("OrderedGroup", nsmap=nsmap)
        og_xml.set("id", str(self.group_id))

        if self.caption is not None:
            og_xml.set("caption", self.caption)

        for child in self.children:
            child_xml = child.to_element(nsmap)
            og_xml.append(child_xml)

        return og_xml


class OrderedGroupIndexed(OrderedGroup, GroupIndexed):
    def __init__(
        self, group_id: str, children: List[GroupIndexed],
        refs: List[RegionRefIndexed], index: int,
        caption: Optional[str] = None
    ):
        super(OrderedGroup, self).__init__(index)
        super().__init__(group_id, children, refs, caption)

    @staticmethod
    def from_element(
        group_xml: etree.ElementBase, nsmap: NsMap
    ) -> "OrderedGroupIndexed":
        index = group_xml.get("index")
        if index is None:
            raise PageXMLError(
                "OrderedGroupIndexed is missing an index attribute"
            )

        try:
            index = int(index)
        except ValueError:
            raise PageXMLError(
                "OrderedGroupIndexed has invalid index attribute"
            )

        og = super().from_element(group_xml, nsmap)

        return OrderedGroupIndexed(
            og.group_id, og.children, og.refs, index, og.caption
        )

    def to_element(self, nsmap: NsMap) -> etree.ElementBase:
        ogi_xml = etree.Element("OrderedGroupIndexed", nsmap=nsmap)
        ogi_xml.set("id", str(self.group_id))
        ogi_xml.set("index", str(self.index))

        if self.caption is not None:
            ogi_xml.set("caption", self.caption)

        for child in self.children:
            child_xml = child.to_element(nsmap)
            ogi_xml.append(child_xml)

        return ogi_xml


class UnorderedGroup(Group):
    def __init__(
        self, group_id: str, children: List[Group],
        refs: List[RegionRef], caption: Optional[str] = None
    ):
        super().__init__(group_id, children, refs, caption)

    @staticmethod
    def from_element(
        group_xml: etree.ElementBase, nsmap: NsMap
    ) -> "UnorderedGroup":
        group_id, caption = super()._from_element(group_xml, "UnorderedGroup")
        children: List[Group] = []

        for og_xml in group_xml.findall("./OrderedGroup", namespaces=nsmap):
            children.append(OrderedGroup.from_element(og_xml, nsmap))

        for ug_xml in group_xml.findall("./UnorderedGroup", namespaces=nsmap):
            children.append(OrderedGroup.from_element(ug_xml, nsmap))

        # TODO: Read refs.

        return UnorderedGroup(group_id, children, caption)

    def to_element(self, nsmap: NsMap) -> etree.ElementBase:
        ug_xml = etree.Element("UnorderedGroup", nsmap=nsmap)
        ug_xml.set("id", str(self.group_id))

        if self.caption is not None:
            ug_xml.set("caption", self.caption)

        for child in self.children:
            child_xml = child.to_element(nsmap)
            ug_xml.append(child_xml)

        return ug_xml


class UnorderedGroupIndexed(UnorderedGroup, GroupIndexed):
    def __init__(
        self, group_id: str, children: List[Group],
        refs: List[RegionRef], index: int, caption: Optional[str] = None
    ):
        super(UnorderedGroup, self).__init__(index)
        super().__init__(group_id, children, refs, caption)

    @staticmethod
    def from_element(
        group_xml: etree.ElementBase, nsmap: NsMap
    ) -> "UnorderedGroupIndexed":
        index = group_xml.get("index")
        if index is None:
            raise PageXMLError(
                "UnorderedGroupIndexed is missing an index attribute"
            )

        try:
            index = int(index)
        except ValueError:
            raise PageXMLError(
                "UnorderedGroupIndexed has invalid index attribute"
            )

        ug = super().from_element(group_xml, nsmap)

        return UnorderedGroupIndexed(
            ug.group_id, ug.children, index, ug.caption
        )

    def to_element(self, nsmap: NsMap) -> etree.ElementBase:
        ugi_xml = etree.Element("UnorderedGroupIndexed", nsmap=nsmap)
        ugi_xml.set("id", str(self.group_id))
        ugi_xml.set("index", str(self.index))

        if self.caption is not None:
            ugi_xml.set("caption", self.caption)

        for child in self.children:
            child_xml = child.to_element(nsmap)
            ugi_xml.append(child_xml)

        return ugi_xml
