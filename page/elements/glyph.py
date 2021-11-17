from page.elements.element import Element
from page.elements.coords import Coordinates
from page.elements.text import Text
from page.constants import NsMap
from page.exceptions import PageXMLError
from typing import Optional
from lxml import etree


class Glyph(Element):
    def __init__(
        self, glyph_id: str,
        coords: Coordinates, text: Optional[Text]
    ):
        self.glyph_id = glyph_id
        self.coords = coords
        self.text = text
        # TODO: Glyph attributes (e.g. ligature, symbol, ...)

    @staticmethod
    def from_element(glyph_xml: etree.ElementBase, nsmap: NsMap) -> "Glyph":
        glyph_id = glyph_xml.get("id")
        if glyph_id is None:
            raise PageXMLError("Glyph is missing an id attribute")

        coords_xml = glyph_xml.find("./Coords", namespaces=nsmap)
        if coords_xml is None:
            raise PageXMLError("Glyph is missing Coords element")

        coords = Coordinates.from_element(coords_xml, nsmap)

        textequiv_xml = glyph_xml.find("./TextEquiv", namespaces=nsmap)
        if textequiv_xml is None:
            text = None
        else:
            text = Text.from_element(textequiv_xml, nsmap)

        return Glyph(glyph_id, coords, text)

    def to_element(self, nsmap: NsMap) -> etree.ElementBase:
        glyph_xml = etree.Element("Glyph", nsmap=nsmap)
        glyph_xml.set("id", self.glyph_id)
        glyph_xml.append(self.coords.to_element(nsmap))

        if self.text is not None:
            glyph_xml.append(self.text.to_element(nsmap))
