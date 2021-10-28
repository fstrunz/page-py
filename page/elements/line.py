from typing import List, Dict, Optional
from dataclasses import dataclass
from page.elements.point import Point, parse_points
from page.exceptions import PageXMLError
from page.constants import NsMap
from lxml import etree


@dataclass
class Text:
    index: Optional[int]
    unicode: str
    plain_text: Optional[str]


class Line:
    def __init__(self, coords: List[Point], texts: List[Text]):
        self.coords = coords
        self.texts = texts

    @staticmethod
    def from_element(region_xml: etree.ElementBase, nsmap: NsMap) -> "Line":
        coords_xml = region_xml.find("./Coords", nsmap)
        if coords_xml is None:
            raise PageXMLError("TextLine is missing Coords")

        coords: List[Point] = parse_points(coords_xml)

        textequiv_xmls = region_xml.findall("./TextEquiv", nsmap)
        texts: List[Text] = []

        for textequiv_xml in textequiv_xmls:
            plaintext_xml = textequiv_xml.find("./PlainText", nsmap)
            unicode_xml = textequiv_xml.find("./Unicode", nsmap)

            index = textequiv_xml.get("index")

            if index is not None:
                try:
                    index = int(index)
                except ValueError:
                    raise PageXMLError(f"TextEquiv has invalid index {index}")

            if unicode_xml is None:
                raise PageXMLError("TextEquiv is missing Unicode tag")

            if plaintext_xml is None:
                text = Text(index, unicode_xml.text, None)
            else:
                text = Text(index, unicode_xml.text, plaintext_xml.text)

            texts.append(text)

        return Line(coords, texts)