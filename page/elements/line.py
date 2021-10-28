from page.elements.point import Point, parse_points
from page.elements.text import Text
from page.exceptions import PageXMLError
from page.constants import NsMap
from lxml import etree
from typing import List


class Line:
    def __init__(self, line_id: str, coords: List[Point], texts: List[Text]):
        self.id = line_id
        self.coords = coords
        self.texts = texts

    @staticmethod
    def from_element(line_xml: etree.ElementBase, nsmap: NsMap) -> "Line":
        line_id = line_xml.get("id")
        if line_id is None:
            raise PageXMLError("TextLine is missing an id")

        coords_xml = line_xml.find("./Coords", nsmap)
        if coords_xml is None:
            raise PageXMLError("TextLine is missing Coords")

        points_str = coords_xml.get("points")
        if points_str is None:
            raise PageXMLError(
                "Coords element of TextLine has no points attribute"
            )

        coords: List[Point] = parse_points(points_str)
        textequiv_xmls = line_xml.findall("./TextEquiv", nsmap)
        texts: List[Text] = [
            Text.from_element(xml, nsmap) for xml in textequiv_xmls
        ]

        return Line(line_id, coords, texts)
