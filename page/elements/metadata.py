from typing import Optional
from datetime import datetime
from dateutil import parser as dateparser
from lxml import etree
from page.exceptions import PageXMLError
from page.constants import NsMap


class Metadata:
    def __init__(
        self,
        creator: str,
        created: datetime,
        last_change: datetime,
        comments: Optional[str],
    ):
        self.creator = creator
        self.comments = comments
        self.created = created
        self.last_change = last_change

    @staticmethod
    def from_element(metadata: etree.ElementBase, nsmap: NsMap) -> "Metadata":
        creator_xml = metadata.find("./Creator", namespaces=nsmap)
        created_xml = metadata.find("./Created", namespaces=nsmap)
        last_change_xml = metadata.find("./LastChange", namespaces=nsmap)
        comments_xml = metadata.find("./Comments", namespaces=nsmap)

        creator = creator_xml.text or ""

        try:
            created = dateparser.parse(created_xml.text)
            last_change = dateparser.parse(last_change_xml.text)
        except (ValueError, OverflowError):
            raise PageXMLError("Metadata tag contains invalid date(s)!")

        # All subelements are mandatory except comments.
        if comments_xml is None:
            comments = None
        else:
            comments = comments_xml.text

        return Metadata(creator, created, last_change, comments)
