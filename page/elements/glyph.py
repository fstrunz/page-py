from page.elements.element import Element
from page.elements.coords import Coordinates
from page.elements.text import Text
from page.constants import NsMap
from typing import Optional
from lxml import etree


class Glyph(Element):
    def __init__(self, coords: Coordinates, text: Optional[Text]):
        # TODO: Glyph attributes (e.g. ligature, symbol, ...)
        self.coords = coords
        self.text = text

    @staticmethod
    def from_element(glyph_xml: etree.ElementBase, nsmap: NsMap) -> "Glyph":
        coords_xml = glyph_xml.find("./Coords", namespaces=nsmap)
        coords = Coordinates.from_element(coords_xml, nsmap)

        textequiv_xml = glyph_xml.find("./TextEquiv", namespaces=nsmap)
        if textequiv_xml is None:
            text = None
        else:
            text = Text.from_element(textequiv_xml, nsmap)

        return Glyph(coords, text)

    def to_element(self, nsmap: NsMap) -> etree.ElementBase:
        glyph_xml = etree.Element("Glyph", nsmap=nsmap)
        glyph_xml.append(self.coords.to_element(nsmap))

        if self.text is not None:
            glyph_xml.append(self.text.to_element(nsmap))
