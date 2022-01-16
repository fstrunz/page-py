from typing import List, Union, Optional
from lxml import etree

from page.elements.indexed import IndexedElement
from page.elements.reading_order.group import Group, GroupIndexed
from page.elements.region_ref import RegionRefIndexed
from page.constants import NsMap
from page.exceptions import PageXMLError
import page.elements.reading_order.unordered_group as ug


class OrderedGroup(
    Group, IndexedElement[int, Union[GroupIndexed, RegionRefIndexed]]
):
    def __init__(
        self, group_id: str,
        children: List[Union[GroupIndexed, RegionRefIndexed]],
        caption: Optional[str] = None
    ):
        super(Group, self).__init__(
            children, lambda group_or_ref: group_or_ref.index
        )
        super().__init__(group_id, children, caption)

    @staticmethod
    def from_element(
        group_xml: etree.ElementBase, nsmap: NsMap
    ) -> "OrderedGroup":
        group_id, caption = super()._from_element(group_xml, "OrderedGroup")
        children: List[Union[GroupIndexed, RegionRefIndexed]] = []

        for ogi_xml in group_xml.findall(
            "./OrderedGroupIndexed", namespaces=nsmap
        ):
            children.append(OrderedGroupIndexed.from_element(ogi_xml, nsmap))

        for ugi_xml in group_xml.findall(
            "./UnorderedGroupIndexed", namespaces=nsmap
        ):
            children.append(
                ug.UnorderedGroupIndexed.from_element(ugi_xml, nsmap)
            )

        for rri_xml in group_xml.findall(
            "./RegionRefIndexed", namespaces=nsmap
        ):
            children.append(RegionRefIndexed.from_element(rri_xml, nsmap))

        return OrderedGroup(group_id, children, caption)

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
        self, group_id: str,
        children: List[Union[GroupIndexed, RegionRefIndexed]],
        index: int, caption: Optional[str] = None
    ):
        super(OrderedGroup, self).__init__(index)
        super().__init__(group_id, children, caption)

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
            og.group_id, og.children, index, og.caption
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
