from typing import Tuple, List, Optional
from lxml import etree
from page.elements import Region
from page.constants import NsMap
from page.exceptions import PageXMLError


class Page:
    def __init__(
        self,
        image_size: Tuple[int, int], image_filename: str,
        regions: List[Region]
    ):
        self.image_size = image_size
        self.image_filename = image_filename
        self.regions = regions

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
        regions: List[Region] = []

        for xml in root_xml.iterchildren():
            # try to parse every direct child element as a region
            region_xml: Optional[Region] = Region.from_element(xml, nsmap)
            if region_xml is not None:
                regions.append(region_xml)

        return Page((width, height), image_filename, regions)

    def to_element(self, nsmap: NsMap) -> etree.ElementBase:
        root_xml = etree.Element("Page", nsmap=nsmap)

        width, height = self.image_size
        root_xml.set("imageWidth", str(width))
        root_xml.set("imageHeight", str(height))
        root_xml.set("imageFilename", self.image_filename)

        for region in self.regions:
            root_xml.append(region.to_element(nsmap))

        return root_xml
