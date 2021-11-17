from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from enum import Enum
from page.elements.element import Element
from page.elements.coords import Coordinates
from page.elements.line import Line
from page.constants import NsMap
from page.exceptions import PageXMLError
from lxml import etree
from dataclasses import dataclass


@dataclass
class Region(Element, ABC):
    region_id: str
    coords: Coordinates
    children: List["Region"]

    @staticmethod
    def _parse_region(
        region_xml: etree.ElementBase, nsmap: NsMap
    ) -> Tuple[str, Coordinates, List["Region"]]:
        region_id = region_xml.get("id")

        coords_xml = region_xml.find("./Coords", nsmap)
        if coords_xml is None:
            raise PageXMLError("region is missing coordinates")

        coords = Coordinates.from_element(coords_xml, nsmap)
        child_regions = []

        for child_xml in region_xml.iterchildren():
            if child_xml.tag.endswith("Region"):
                # try to parse this region
                region: Optional[Region] = Region.try_from_element(
                    child_xml, nsmap
                )

                if region is not None:
                    child_regions.append(region)

        return region_id, coords, child_regions

    def _create_region_base_element(
        self, tag: str, nsmap: NsMap
    ) -> etree.ElementBase:
        region_xml = etree.Element(
            tag, attrib={"id": self.region_id}, nsmap=nsmap
        )
        region_xml.append(self.coords.to_element(nsmap))

        for child in self.children:
            region_xml.append(child.to_element(nsmap))

        return region_xml

    @staticmethod
    def try_from_element(
        region_xml: etree.ElementBase, nsmap: NsMap
    ) -> Optional["Region"]:
        region_tag: str = etree.QName(region_xml.tag).localname

        # TODO: Implement other region tags
        if region_tag == "TextRegion":
            return TextRegion.from_element(region_xml, nsmap)
        else:
            return None

    @staticmethod
    def from_element(region_xml: etree.ElementBase, nsmap: NsMap) -> "Region":
        region = Region.try_from_element(region_xml, nsmap)
        if region is None:
            raise PageXMLError(f"Tag {region_xml.tag} is not a region tag")
        return region

    @abstractmethod
    def to_element(nsmap: NsMap) -> etree.ElementBase:
        return


class TextRegionType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CAPTION = "caption"
    HEADER = "header"
    FOOTER = "footer"
    PAGE_NUMBER = "page-number"
    DROP_CAPITAL = "drop-capital"
    CREDIT = "credit"
    FLOATING = "floating"
    SIGNATURE_MARK = "signature-mark"
    CATCH_WORD = "catch-word"
    MARGINALIA = "marginalia"
    FOOTNOTE = "footnote"
    FOOTNOTE_CONTINUED = "footnote-continued"
    ENDNOTE = "endnote"
    TOC_ENTRY = "TOC-entry"
    OTHER = "other"


class TextRegion(Region):
    def __init__(
        self, region_id: str,
        coords: Coordinates, children: List[Region],
        region_type: TextRegionType, lines: List[Line]
    ):
        super().__init__(region_id, coords, children)
        self.region_type = region_type
        self.lines = lines
        # TODO: TextRegion can contain its own TextEquiv (and TextStyle)

    @staticmethod
    def from_element(
        region_xml: etree.ElementBase, nsmap: NsMap
    ) -> "TextRegion":
        region_type_name = region_xml.get("type")

        if region_type_name is None:
            raise PageXMLError("region is missing a type attribute")

        try:
            region_type = TextRegionType(region_type_name)
        except ValueError:
            raise PageXMLError(f"region has invalid type '{region_type_name}'")

        region_id, coords, children = Region._parse_region(region_xml, nsmap)

        line_xmls = region_xml.findall("./TextLine", nsmap)
        lines: List[Line] = [
            Line.from_element(line_xml, nsmap) for line_xml in line_xmls
        ]

        return TextRegion(region_id, coords, children, region_type, lines)

    def to_element(self, nsmap: NsMap) -> etree.ElementBase:
        region_xml = self._create_region_base_element("TextRegion", nsmap)

        for line in self.lines:
            region_xml.append(line.to_element(nsmap))

        return region_xml
