from typing import Iterable, Tuple, List, Optional
from lxml import etree
from page.elements.line import Line
from page.elements.region import Region, TextRegion
from page.elements.element import Element
from page.elements.reading_order import ReadingOrder
from page.constants import NsMap
from page.exceptions import PageXMLError
from dataclasses import dataclass, field


@dataclass
class Page(Element):
    image_size: Tuple[int, int]
    image_filename: str
    reading_order: Optional[ReadingOrder] = field(repr=False)
    regions: List[Region] = field(repr=False)

    @staticmethod
    def from_element(
        root_xml: etree.ElementBase, nsmap: NsMap
    ) -> "Page":
        try:
            width = int(root_xml.get("imageWidth"))
            height = int(root_xml.get("imageHeight"))
        except ValueError:
            raise PageXMLError(
                "invalid image width and/or height in Page element"
            )

        image_filename = root_xml.get("imageFilename")

        ro_xml = root_xml.find("./ReadingOrder", namespaces=nsmap)
        if ro_xml is None:
            reading_order = None
        else:
            reading_order = ReadingOrder.from_element(ro_xml, nsmap)

        regions: List[Region] = []

        for xml in root_xml.iterchildren():
            # try to parse every direct child element as a region
            region_xml: Optional[Region] = Region.try_from_element(xml, nsmap)
            if region_xml is not None:
                regions.append(region_xml)

        return Page((width, height), image_filename, reading_order, regions)

    def to_element(self, nsmap: NsMap) -> etree.ElementBase:
        root_xml = etree.Element("Page", nsmap=nsmap)

        width, height = self.image_size
        root_xml.set("imageWidth", str(width))
        root_xml.set("imageHeight", str(height))
        root_xml.set("imageFilename", self.image_filename)

        if self.reading_order is not None:
            root_xml.append(self.reading_order.to_element(nsmap))

        for region in self.regions:
            root_xml.append(region.to_element(nsmap))

        return root_xml

    def text_regions(self) -> Iterable[TextRegion]:
        for region in self.regions:
            if isinstance(region, TextRegion):
                yield region

    def lines(self) -> Iterable[Line]:
        return (
            line for region in self.text_regions() for line in region.lines
        )
