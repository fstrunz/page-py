from typing import Dict, TextIO
from lxml import etree
from page.elements import Metadata, Region
from page.constants import DEFAULT_NAMESPACE_MAP, NsMap


class Page:
    def __init__(
        self, metadata: Metadata, regions: Dict[str, Region],
        nsmap: NsMap = DEFAULT_NAMESPACE_MAP
    ):
        self.metadata = metadata
        self.regions = regions
        self.nsmap = nsmap

    @staticmethod
    def from_element(
        root: etree.ElementBase, nsmap: NsMap
    ) -> "Page":
        metadata_xml = root.find("./Metadata", namespaces=nsmap)
        metadata = Metadata.from_element(metadata_xml, nsmap)
        regions = {}  # TODO: Parse regions.

        return Page(metadata, regions, nsmap)

    @staticmethod
    def from_file(file: TextIO) -> "Page":
        tree = etree.parse(file)
        root = tree.getroot()
        return Page.from_element(root, root.nsmap)
