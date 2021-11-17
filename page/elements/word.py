from page.elements.element import Element
from page.elements.coords import Coordinates
from page.elements.glyph import Glyph
from page.elements.text import Text
from page.constants import NsMap
from page.exceptions import PageXMLError
from typing import List
from lxml import etree
from dataclasses import dataclass


@dataclass
class Word(Element):
    word_id: str
    coords: Coordinates
    glyphs: List[Glyph]
    texts: List[Text]

    @staticmethod
    def from_element(word_xml: etree.ElementBase, nsmap: NsMap) -> "Word":
        word_id = word_xml.get("id")
        if word_id is None:
            raise PageXMLError("Word is missing an id attribute")

        coords_xml = word_xml.find("./Coords", namespaces=nsmap)
        if coords_xml is None:
            raise PageXMLError("Word is missing Coords element")

        coords = Coordinates.from_element(coords_xml, nsmap)

        textequiv_xmls = word_xml.findall("./TextEquiv", namespaces=nsmap)
        texts: List[Text] = [
            Text.from_element(xml, nsmap) for xml in textequiv_xmls
        ]
        return Word(word_id, coords, texts)

    def to_element(self, nsmap: NsMap) -> etree.ElementBase:
        word_xml = etree.Element("Word", nsmap=nsmap)
        word_xml.set("id", self.word_id)
        word_xml.append(self.coords.to_element(nsmap))

        for glyph in self.glyphs:
            word_xml.append(glyph.to_element(nsmap))

        if self.text is not None:
            word_xml.append(self.text.to_element(nsmap))
