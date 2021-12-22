from page.elements import Element
from page.elements.point import Point, parse_points, points_to_string
from page.constants import NsMap
from page.exceptions import PageXMLError
from typing import List
from lxml import etree
from dataclasses import dataclass


@dataclass
class Coordinates(Element):
    points: List[Point]

    @staticmethod
    def _from_element(
        coords_xml: etree.ElementBase, nsmap: NsMap
    ) -> List[Point]:
        points_str = coords_xml.get("points")
        if points_str is None:
            raise PageXMLError("Coords element is missing points attribute")

        return parse_points(points_str)

    @staticmethod
    def from_element(
        coords_xml: etree.ElementBase, nsmap: NsMap
    ) -> "Coordinates":
        return Coordinates(Coordinates._from_element(coords_xml, nsmap))

    def _to_element(self, nsmap: NsMap, tag_name: str) -> etree.ElementBase:
        coords_xml = etree.Element(tag_name, nsmap=nsmap)
        coords_xml.set("points", points_to_string(self.points))
        return coords_xml

    def to_element(self, nsmap: NsMap) -> etree.ElementBase:
        return self._to_element(nsmap, "Coords")


@dataclass
class Baseline(Coordinates):
    @staticmethod
    def from_element(
        coords_xml: etree.ElementBase, nsmap: NsMap
    ) -> "Baseline":
        return Baseline(Coordinates._from_element(coords_xml, nsmap))

    def to_element(self, nsmap: NsMap) -> etree.ElementBase:
        return self._to_element(nsmap, "Baseline")
