from page.constants import NsMap
from page.exceptions import PageXMLError
from page.elements.element import Element
from page.elements.reading_order.group import Group, GroupIndexed
from page.elements.reading_order.unordered_group import (
    UnorderedGroup, UnorderedGroupIndexed
)
from page.elements.reading_order.ordered_group import (
    OrderedGroup, OrderedGroupIndexed
)

from dataclasses import dataclass
from typing import Union
from lxml import etree


@dataclass
class ReadingOrder(Element):
    root: Union[OrderedGroup, UnorderedGroup]

    @staticmethod
    def from_element(
        ro_xml: etree.ElementBase, nsmap: NsMap
    ) -> "ReadingOrder":
        og_xml = ro_xml.find("./OrderedGroup", namespaces=nsmap)
        ug_xml = ro_xml.find("./UnorderedGroup", namespaces=nsmap)

        if og_xml is not None:
            return ReadingOrder(OrderedGroup.from_element(og_xml, nsmap))
        elif ug_xml is not None:
            return ReadingOrder(UnorderedGroup.from_element(ug_xml, nsmap))
        else:
            raise PageXMLError("ReadingOrder does not contain a group")

    def to_element(self, nsmap: NsMap) -> etree.ElementBase:
        ro_xml = etree.Element("ReadingOrder", nsmap=nsmap)
        ro_xml.append(self.root.to_element(nsmap))
        return ro_xml


__all__ = [
    "Group", "GroupIndexed",
    "OrderedGroup", "OrderedGroupIndexed",
    "UnorderedGroup", "UnorderedGroupIndexed",
    "ReadingOrder"
]
