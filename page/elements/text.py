from dataclasses import dataclass, field
from typing import Optional
from page.exceptions import PageXMLError
from page.elements import Element
from page.constants import NsMap
from lxml import etree


@dataclass
class Text(Element):
    index: Optional[int]
    unicode: str
    plain_text: Optional[str] = field(default=None)
    conf: Optional[float] = field(default=None)

    def __post_init__(self):
        if self.conf is not None and not (0 < self.conf < 1):
            raise ValueError("conf must be strictly between 0 and 1")

    @staticmethod
    def from_element(textequiv_xml: etree.ElementBase, nsmap: NsMap) -> "Text":
        conf = textequiv_xml.get("conf")

        if conf is not None:
            try:
                conf = float(conf)
            except ValueError:
                raise PageXMLError(
                    f"confidence {conf} is not a valid float"
                )

            if not (0 < conf < 1):
                raise PageXMLError(
                    f"confidence {conf} is not strictly between 0 and 1"
                )

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
            text = Text(index, unicode_xml.text or "", None, conf)
        else:
            text = Text(
                index, unicode_xml.text or "", plaintext_xml.text, conf
            )

        return text

    def to_element(self, nsmap: NsMap) -> etree.ElementBase:
        textequiv_xml = etree.Element("TextEquiv", nsmap=nsmap)

        if self.conf is not None:
            textequiv_xml.set("conf", str(self.conf))

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
