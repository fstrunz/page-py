from abc import ABC, abstractmethod
from lxml import etree
from page.constants import NsMap


class Element(ABC):
    """Represents a node in the abstract syntax tree of the PAGE-XML document.
    For example, these could be regions, lines, text, etc.
    """

    @staticmethod
    @abstractmethod
    def from_element(xml: etree.ElementBase, nsmap: NsMap) -> "Element":
        """Parses an lxml tree element into an AST node.

        Parameters
        ----------
        xml : lxml.etree.ElementBase
            The xml element to parse.
        nsmap : page.constants.NsMap
            The namespace map to use, usually something like

                {
                    None: "http://schema.primaresearch.org/..."}
                }

            This is required when parsing PAGE-XML documents with
            a namespace (as will be the case for most)!

        Raises
        ------
        PageXMLError
            If the XML element is malformed and does not conform to the
            PAGE-XML specification.
        """

        pass

    @abstractmethod
    def to_element(self, nsmap: NsMap) -> etree.ElementBase:
        """Writes an Element into an lxml element.

        Parameters
        ----------
        nsmap : page.constants.NsMap
            The namespace map to use for writing the elements,
            see from_element.
        """

        pass
