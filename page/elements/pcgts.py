from typing import Optional, TextIO
from page.elements.metadata import Metadata
from page.elements.page import Page
from page.elements.element import Element
from page.exceptions import PageXMLError
from page.constants import NsMap
from lxml import etree


class PcGts(Element):
    def __init__(
        self, pc_gts_id: Optional[str], metadata: Metadata, page: Page
    ):
        self.pc_gts_id = pc_gts_id
        self.metadata = metadata
        self.page = page

    @staticmethod
    def from_element(pcgts_xml: etree.ElementBase, nsmap: NsMap) -> "PcGts":
        pc_gts_id = pcgts_xml.get("pcGtsId")

        metadata_xml = pcgts_xml.find("./Metadata", namespaces=nsmap)
        if metadata_xml is None:
            raise PageXMLError("PcGts tag is missing Metadata tag")

        page_xml = pcgts_xml.find("./Page", namespaces=nsmap)
        if page_xml is None:
            raise PageXMLError("PcGts tag does not contain a Page")

        return PcGts(
            pc_gts_id,
            Metadata.from_element(metadata_xml, nsmap),
            Page.from_element(page_xml, nsmap)
        )

    def to_element(self, nsmap: NsMap) -> etree.ElementBase:
        pcgts_xml = etree.Element("PcGts", nsmap=nsmap)
        if self.pc_gts_id is not None:
            pcgts_xml.set("pcGtsId", self.pc_gts_id)

        pcgts_xml.append(self.metadata.to_element(nsmap))
        pcgts_xml.append(self.page.to_element(nsmap))
        return pcgts_xml

    def from_file(file: TextIO) -> Optional["PcGts"]:
        tree = etree.parse(file)
        root_xml = tree.getroot()
        root_tag: str = etree.QName(root_xml.tag).localname

        if root_tag != "PcGts":
            # this is not a pagecontent file
            return None

        return PcGts.from_element(root_xml, root_xml.nsmap)
