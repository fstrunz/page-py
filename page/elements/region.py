from abc import ABC
from typing import List, Tuple
from enum import Enum
from page.elements.line import Line
from page.elements.point import Point, parse_points
from page.constants import NsMap
from page.exceptions import PageXMLError
from lxml import etree


class Region(ABC):
    def __init__(self, coords: List[Point], children: List["Region"]):
        self.coords = coords
        self.children = children

    @staticmethod
    def __parse_region(
        region_xml: etree.ElementBase, nsmap: NsMap
    ) -> Tuple[List[Point], List["Region"]]:
        coords_xml = region_xml.find("./Coords", nsmap)
        if coords_xml is None:
            raise PageXMLError("region is missing coordinates")

        points_str = coords_xml.get("points")
        if points_str is None:
            raise PageXMLError("Coords element is missing 'points' attribute")

        coords = parse_points(points_str)

        # TODO: Parse child regions.
        return coords, []


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
        self,
        coords: List[Point], children: List[Region],
        region_type: TextRegionType, lines: List[Line]
    ):
        super().__init__(coords, children)
        self.region_type = region_type
        self.lines = lines

    @staticmethod
    def from_element(region_xml: etree.ElementBase, nsmap: NsMap) -> Region:
        region_type_name = region_xml.get("type")

        try:
            region_type = TextRegionType(region_type_name)
        except ValueError:
            raise PageXMLError(f"region has invalid type '{region_type_name}'")

        coords, children = Region.__parse_region(region_xml, nsmap)

        # TODO: Parse lines!!
        return TextRegion(coords, children, region_type, [])
