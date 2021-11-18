from page.elements.element import Element
from page.elements.coords import Coordinates
from page.elements.text import Text
from page.elements.indexed import IndexedElement
from page.constants import NsMap
from page.exceptions import PageXMLError
from typing import Iterable, List, Optional
from lxml import etree
from dataclasses import dataclass


@dataclass
class Glyph(Element):
    glyph_id: str
    coords: Coordinates
    text: Optional[Text]
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

        textequiv_xmls = glyph_xml.findall("./TextEquiv", namespaces=nsmap)
        textequiv_count = len(textequiv_xmls)

        if textequiv_count == 0:
            return Glyph(glyph_id, coords, None)
        elif textequiv_count == 1:
            text = Text.from_element(textequiv_xmls[0], nsmap)
            return Glyph(glyph_id, coords, text)
        else:
            texts = [Text.from_element(xml, nsmap) for xml in textequiv_xmls]
            return IndexedGlyph(glyph_id, coords, texts)

    def to_element(self, nsmap: NsMap) -> etree.ElementBase:
        glyph_xml = etree.Element("Glyph", nsmap=nsmap)
        glyph_xml.set("id", self.glyph_id)
        glyph_xml.append(self.coords.to_element(nsmap))

        if self.text is not None:
            glyph_xml.append(self.text.to_element(nsmap))

        return glyph_xml


class IndexedGlyph(Glyph, IndexedElement[int, Text]):
    def __init__(self, glyph_id: str, coords: Coordinates, texts: List[Text]):
        super().__init__(glyph_id, coords, None)
        super(Glyph, self).__init__(texts, lambda text: text.index)

    def texts(self) -> Iterable[Text]:
        return self.objects()

    def to_element(self, nsmap: NsMap) -> etree.ElementBase:
        glyph_xml = super().to_element(nsmap)

        for text in self.texts():
            glyph_xml.append(text.to_element(nsmap))

        return glyph_xml
