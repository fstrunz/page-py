from page.elements.element import Element
from page.elements.coords import Coordinates
from page.elements.text import Text
from page.exceptions import PageXMLError
from page.constants import NsMap
from lxml import etree
from typing import List, Dict, Optional


class Line(Element):
    def __init__(self, line_id: str, coords: Coordinates, texts: List[Text]):
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

        coords: Coordinates = Coordinates.from_element(coords_xml, nsmap)
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
        line_xml.append(self.coords.to_element(nsmap))

        for text in self.texts:
            line_xml.append(text.to_element(nsmap))

        return line_xml


class IndexedLine(Line):
    def __init__(
        self, line_id: str, coords: Coordinates,
        texts: List[Text], index_dict: Dict[int, Text]
    ):
        super().__init__(line_id, coords, texts)
        self.__index_dict = index_dict

    def get_text_from_index(self, index: int) -> Optional[Text]:
        if index in self.__index_dict:
            return self.__index_dict[index]
        else:
            return None
