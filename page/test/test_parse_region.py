import unittest
from typing import Optional
from lxml import etree
from page.elements.region import Region, TextRegion, TextRegionType
from page.elements.point import Point


SIMPLE_TEXT_REGION = etree.XML(
    """<TextRegion id="r0" type="paragraph">
        <Coords points="0,0 300,400 800,600 100,200" />
    </TextRegion>"""
)


class TestParseRegion(unittest.TestCase):
    def test_text_region(self):
        text_region: TextRegion = TextRegion.from_element(
            SIMPLE_TEXT_REGION, {}
        )

        self.assertEqual(text_region.id, "r0")
        self.assertEqual(text_region.children, [])
        self.assertEqual(text_region.region_type, TextRegionType.PARAGRAPH)
        self.assertEqual(
            text_region.coords,
            [Point(0, 0), Point(300, 400), Point(800, 600), Point(100, 200)]
        )

    def test_simple_region(self):
        region: Optional[Region] = Region.from_element(SIMPLE_TEXT_REGION, {})

        # check that from_element recognised this as a text region
        self.assertIsInstance(region, TextRegion)
        self.assertEqual(region.id, "r0")
