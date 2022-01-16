from typing import List, Union, Optional
from lxml import etree

from page.elements.region_ref import RegionRef
from page.elements.reading_order.group import Group, GroupIndexed
from page.constants import NsMap
from page.exceptions import PageXMLError
import page.elements.reading_order.ordered_group as og


class UnorderedGroup(Group):
    def __init__(
        self, group_id: str, children: List[Union[Group, RegionRef]],
        caption: Optional[str] = None
    ):
        super().__init__(group_id, children, caption)

    @staticmethod
    def from_element(
        group_xml: etree.ElementBase, nsmap: NsMap
    ) -> "UnorderedGroup":
        group_id, caption = Group._from_element(group_xml, "UnorderedGroup")
        children: List[Union[Group, RegionRef]] = []

        for og_xml in group_xml.findall("./OrderedGroup", namespaces=nsmap):
            children.append(og.OrderedGroup.from_element(og_xml, nsmap))

        for ug_xml in group_xml.findall("./UnorderedGroup", namespaces=nsmap):
            children.append(UnorderedGroup.from_element(ug_xml, nsmap))

        for rr_xml in group_xml.findall("./RegionRef", namespaces=nsmap):
            children.append(RegionRef.from_element(rr_xml, nsmap))

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
        GroupIndexed.__init__(self, index)
        UnorderedGroup.__init__(self, group_id, children, refs, caption)

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
