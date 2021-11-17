from page.elements.element import Element
from page.elements.coords import Coordinates
from page.elements.glyph import Glyph
from page.elements.text import Text
from page.constants import NsMap
from typing import Optional, List
from lxml import etree


class Word(Element):
    def __init__(
        self, coords: Coordinates, glyphs: List[Glyph], text: Optional[Text]
    ):
        self.coords = coords
        self.text = text
        self.glyphs = glyphs

    @staticmethod
    def from_element(word_xml: etree.ElementBase, nsmap: NsMap) -> "Word":
        coords_xml = word_xml.find("./Coords", namespaces=nsmap)
        coords = Coordinates.from_element(coords_xml, nsmap)

        textequiv_xml = word_xml.find("./TextEquiv", namespaces=nsmap)
        if textequiv_xml is None:
            text = None
        else:
            text = Text.from_element(textequiv_xml, nsmap)

        return Word(coords, text)

    def to_element(self, nsmap: NsMap) -> etree.ElementBase:
        word_xml = etree.Element("Word", nsmap=nsmap)
        word_xml.append(self.coords.to_element(nsmap))

        for glyph in self.glyphs:
            word_xml.append(glyph.to_element(nsmap))

        if self.text is not None:
            word_xml.append(self.text.to_element(nsmap))
