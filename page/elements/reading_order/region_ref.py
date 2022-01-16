from dataclasses import dataclass
from lxml import etree

from page.elements import Element
from page.constants import NsMap
from page.exceptions import PageXMLError


@dataclass
class RegionRef(Element):
    ref: str

    @staticmethod
    def from_element(
        ref_xml: etree.ElementBase, nsmap: NsMap
    ) -> "RegionRef":
        ref = ref_xml.get("regionRef")
        if ref is None:
            raise PageXMLError("RegionRef is missing a regionRef attribute!")

        return RegionRef(ref)

    def to_element(self, nsmap: NsMap) -> etree.ElementBase:
        ref_xml = etree.Element("RegionRef", nsmap=nsmap)
        ref_xml.set("regionRef", self.ref)
        return ref_xml


@dataclass
class RegionRefIndexed(RegionRef):
    index: int

    @staticmethod
    def from_element(
        ref_xml: etree.ElementBase, nsmap: NsMap
    ) -> "RegionRefIndexed":
        region_ref = super().from_element(ref_xml, nsmap)
        index = ref_xml.get("index")
        if index is None:
            raise PageXMLError(
                "RegionRefIndexed is missing an index attribute!"
            )

        try:
            index = int(index)
        except ValueError:
            raise PageXMLError(
                "RegionRefIndexed has invalid index attribute"
            )

        return RegionRefIndexed(region_ref, index)

    def to_element(self, nsmap: NsMap) -> etree.ElementBase:
        ref_xml = etree.Element("RegionRefIndexed", nsmap=nsmap)
        ref_xml.set("regionRef", self.ref)
        ref_xml.set("index", str(self.index))
        return ref_xml
