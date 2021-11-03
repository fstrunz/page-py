from typing import TextIO, Optional, List, Tuple
from lxml import etree
from page.elements import Metadata, Region
from page.constants import NsMap
from page.exceptions import PageXMLError


class Page:
    def __init__(
        self, metadata: Metadata,
        image_size: Tuple[int, int], image_filename: str,
        regions: List[Region]
    ):
        self.metadata = metadata
        self.image_size = image_size
        self.image_filename = image_filename
        self.regions = regions

    @staticmethod
    def from_element(
        root_xml: etree.ElementBase, nsmap: NsMap
    ) -> "Page":
        metadata_xml = root_xml.find("./Metadata", namespaces=nsmap)
        if metadata_xml is None:
            raise PageXMLError(
                "page is missing required Metadata tag"
            )

        metadata = Metadata.from_element(metadata_xml, nsmap)

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

        return Page(metadata, (width, height), image_filename, regions)

    def to_element(self, nsmap: NsMap) -> etree.ElementBase:
        root_xml = etree.Element("Page", nsmap=nsmap)

        metadata_xml = self.metadata.to_element(nsmap)
        root_xml.append(metadata_xml)

        width, height = self.image_size
        root_xml.set("imageWidth", str(width))
        root_xml.set("imageHeight", str(height))
        root_xml.set("imageFilename", self.image_filename)

        for region in self.regions:
            root_xml.append(region.to_element(nsmap))

        return root_xml

    @staticmethod
    def from_file(file: TextIO) -> "Page":
        tree = etree.parse(file)
        root = tree.getroot()
        return Page.from_element(root, root.nsmap)


__all__ = [
    "Page"
]
