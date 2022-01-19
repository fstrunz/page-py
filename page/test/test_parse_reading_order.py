import unittest
from lxml import etree

from page.elements.reading_order import (
    ReadingOrder, OrderedGroup, UnorderedGroup
)
from page.exceptions import PageXMLError
import page.test.assert_utils as utils

READING_ORDER_ORDERED = etree.XML(
    """<ReadingOrder>
        <OrderedGroup id="g0">
        </OrderedGroup>
    </ReadingOrder>"""
)

READING_ORDER_UNORDERED = etree.XML(
    """<ReadingOrder>
        <UnorderedGroup id="u0">
        </UnorderedGroup>
    </ReadingOrder>"""
)

READING_ORDER_EMPTY = etree.XML(
    """<ReadingOrder></ReadingOrder>"""
)


class TestParseReadingOrder(unittest.TestCase):
    def test_parse_reading_order_ordered(self):
        ro = ReadingOrder.from_element(READING_ORDER_ORDERED, {})
        self.assertIsInstance(ro.root, OrderedGroup)

    def test_parse_reading_order_unordered(self):
        ro = ReadingOrder.from_element(READING_ORDER_UNORDERED, {})
        self.assertIsInstance(ro.root, UnorderedGroup)

    def test_parse_reading_order_empty(self):
        self.assertRaises(
            PageXMLError,
            lambda: ReadingOrder.from_element(READING_ORDER_EMPTY, {})
        )

    def test_parse_reading_order_invert(self):
        for xml in [READING_ORDER_ORDERED, READING_ORDER_UNORDERED]:
            utils.assert_same_descendant_tags(
                self,
                ReadingOrder.from_element(xml, {}).to_element({}),
                xml
            )
