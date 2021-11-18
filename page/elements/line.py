from page.elements.element import Element
from page.elements.coords import Coordinates
from page.elements.text import Text
from page.elements.indexed import IndexedElement
from page.exceptions import PageXMLError
from page.constants import NsMap
from lxml import etree
from typing import Iterable, List, Optional
from dataclasses import dataclass


@dataclass
class Line(Element):
    line_id: str
    coords: Coordinates
    text: Optional[Text]

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
        textequiv_count = len(textequiv_xmls)

        if textequiv_count == 0:
            return Line(line_id, coords, None)
        elif textequiv_count == 1:
            text = Text.from_element(textequiv_xmls[0], nsmap)
            return Line(line_id, coords, text)
        else:
            texts = [Text.from_element(xml, nsmap) for xml in textequiv_xmls]
            return IndexedLine(line_id, coords, texts)

    def to_element(self, nsmap: NsMap) -> etree.ElementBase:
        line_xml = etree.Element(
            "TextLine", attrib={"id": self.line_id}, nsmap=nsmap
        )
        line_xml.append(self.coords.to_element(nsmap))

        if self.text is not None:
            line_xml.append(self.text.to_element(nsmap))

        return line_xml


class IndexedLine(Line, IndexedElement[int, Text]):
    def __init__(self, line_id: str, coords: Coordinates, texts: List[Text]):
        super().__init__(line_id, coords, None)
        super(Line, self).__init__(texts, lambda text: text.index)

    def texts(self) -> Iterable[Text]:
        return self.objects()

    def to_element(self, nsmap: NsMap) -> etree.ElementBase:
        line_xml = super().to_element(nsmap)

        for text in self.texts():
            line_xml.append(text.to_element(nsmap))

        return line_xml
