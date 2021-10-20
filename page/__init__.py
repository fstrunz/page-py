from typing import Dict, TextIO, Optional
from lxml import etree
from page.elements import Region
from page.elements.metadata import Metadata

NsMap = Dict[Optional[str], str]
DEFAULT_XML_NAMESPACE = (
    "http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15"
)
DEFAULT_NAMESPACE_MAP: NsMap = {None: DEFAULT_XML_NAMESPACE}


class Page:
    def __init__(
        self, metadata: Metadata, regions: Dict[str, Region],
        nsmap: NsMap = DEFAULT_NAMESPACE_MAP
    ):
        self.regions = regions
        self.nsmap = nsmap

    @staticmethod
    def from_element(
        root: etree.ElementBase, nsmap: NsMap
    ) -> "Page":
        metadata_xml = root.find("./Metadata", namespaces=nsmap)
        metadata = Metadata.from_element(metadata_xml)
        regions = {}  # TODO: Parse regions.

        return Page(metadata, regions, nsmap)

    @staticmethod
    def from_file(file: TextIO) -> "Page":
        tree = etree.parse(file)
        root = tree.getroot()
        return Page.from_root_element(root, root.nsmap)
