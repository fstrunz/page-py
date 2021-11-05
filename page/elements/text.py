from dataclasses import dataclass
from typing import Optional
from page.exceptions import PageXMLError
from page.elements import Element
from page.constants import NsMap
from lxml import etree


@dataclass
class Text(Element):
    index: Optional[int]
    unicode: str
    plain_text: Optional[str]

    @staticmethod
    def from_element(textequiv_xml: etree.ElementBase, nsmap: NsMap) -> "Text":
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

        return text

    def to_element(self, nsmap: NsMap) -> etree.ElementBase:
        textequiv_xml = etree.Element("TextEquiv", nsmap=nsmap)

        if self.index is not None:
            textequiv_xml.set("index", str(self.index))

        unicode_xml = etree.SubElement(textequiv_xml, "Unicode", nsmap=nsmap)
        unicode_xml.text = self.unicode

        if self.plain_text is not None:
            plaintext_xml = etree.SubElement(
                textequiv_xml, "PlainText", nsmap=nsmap
            )
            plaintext_xml.text = self.plain_text

        return textequiv_xml
