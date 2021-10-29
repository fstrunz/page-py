from page.elements.point import Point, parse_points, points_to_string
from page.elements.text import Text
from page.exceptions import PageXMLError
from page.constants import NsMap
from lxml import etree
from typing import List, Dict, Optional


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

        texts: List[Text] = []
        index_dict: Dict[int, Text] = {}

        for xml in textequiv_xmls:
            text = Text.from_element(xml, nsmap)
            if text.index is not None:
                index_dict[text.index] = text
            texts.append(text)

        if index_dict:
            return IndexedLine(line_id, coords, texts, index_dict)
        else:
            return Line(line_id, coords, texts)

    def to_element(self, nsmap: NsMap) -> etree.ElementBase:
        line_xml = etree.Element(
            "TextLine", attrib={"id": self.id}, nsmap=nsmap
        )

        coords_xml = etree.SubElement(line_xml, "Coords", nsmap=nsmap)
        coords_xml.set("points", points_to_string(self.coords))

        for text in self.texts:
            line_xml.append(text.to_element(nsmap))

        return line_xml


class IndexedLine(Line):
    def __init__(
        self, line_id: str, coords: List[Point],
        texts: List[Text], index_dict: Dict[int, Text]
    ):
        super().__init__(line_id, coords, texts)
        self.__index_dict = index_dict

    def get_text_from_index(self, index: int) -> Optional[Text]:
        if index in self.__index_dict:
            return self.__index_dict[index]
        else:
            return None
