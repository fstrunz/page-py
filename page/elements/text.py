from dataclasses import dataclass
from typing import Optional
from page.exceptions import PageXMLError
from page.constants import NsMap
from lxml import etree


@dataclass
class Text:
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
