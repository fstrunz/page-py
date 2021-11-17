from page.elements import Element
from page.elements.point import Point, parse_points, points_to_string
from page.constants import NsMap
from page.exceptions import PageXMLError
from typing import List
from lxml import etree


class Coordinates(Element):
    def __init__(self, points: List[Point]):
        self.points = points

    @staticmethod
    def from_element(
        coords_xml: etree.ElementBase, nsmap: NsMap
    ) -> "Coordinates":
        points_str = coords_xml.get("points")
        if points_str is None:
            raise PageXMLError("Coords element is missing points attribute")

        points: List[Point] = parse_points(points_str)
        return Coordinates(points)

    def to_element(self, nsmap: NsMap) -> etree.ElementBase:
        coords_xml = etree.Element("Coords", nsmap=nsmap)
        coords_xml.set("points", points_to_string(self.points))
        return coords_xml
