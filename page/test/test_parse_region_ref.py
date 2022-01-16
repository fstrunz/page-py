import unittest
from lxml import etree

from page.elements import RegionRef, RegionRefIndexed
from page.exceptions import PageXMLError
import page.test.assert_utils as utils


SIMPLE_REGION_REF = etree.XML(
    """<RegionRef regionRef="r0" />"""
)

SIMPLE_INDEXED_REGION_REF = etree.XML(
    """<RegionRefIndexed regionRef="r1" index="0" />"""
)

INDEXED_REGION_REF_WITHOUT_INDEX = etree.XML(
    """<RegionRefIndexed regionRef="r2" />"""
)

INDEXED_REGION_REF_INVALID_INDEX = etree.XML(
    """<RegionRefIndexed regionRef="r1" index="h" />"""
)

EMPTY_REGION_REF = etree.XML(
    """<RegionRef />"""
)

EMPTY_INDEXED_REGION_REF = etree.XML(
    """<RegionRefIndexed />"""
)


class TestParseRegionRef(unittest.TestCase):
    def test_parse_simple_region_ref(self):
        region_ref = RegionRef.from_element(SIMPLE_REGION_REF, {})
        self.assertEqual(region_ref.ref, "r0")

    def test_parse_simple_indexed_region_ref(self):
        region_ref = RegionRefIndexed.from_element(
            SIMPLE_INDEXED_REGION_REF, {}
        )
        self.assertEqual(region_ref.ref, "r1")
        self.assertEqual(region_ref.index, 0)

    def test_parse_invalid_indexed_region_refs(self):
        for xml in [
            INDEXED_REGION_REF_WITHOUT_INDEX,
            INDEXED_REGION_REF_INVALID_INDEX,
            EMPTY_INDEXED_REGION_REF
        ]:
            self.assertRaises(
                PageXMLError,
                lambda: RegionRefIndexed.from_element(xml, {})
            )

    def test_parse_empty_region_ref(self):
        self.assertRaises(
            PageXMLError,
            lambda: RegionRef.from_element(EMPTY_REGION_REF, {})
        )

    def test_parse_region_ref_invert(self):
        utils.assert_same_descendant_tags(
            self,
            RegionRef.from_element(SIMPLE_REGION_REF, {}).to_element({}),
            SIMPLE_INDEXED_REGION_REF
        )

        utils.assert_same_descendant_tags(
            self,
            RegionRef.from_element(
                SIMPLE_INDEXED_REGION_REF, {}
            ).to_element({}),
            SIMPLE_INDEXED_REGION_REF
        )
