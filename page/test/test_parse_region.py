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

NESTED_TEXT_REGIONS = etree.XML(
    """<TextRegion id="r0" type="caption">
        <Coords points="0,0 300,400 800,600 100,200" />
        <TextRegion id="r01" type="heading">
            <Coords points="100,200 600,200 400,500 300,900" />
        </TextRegion>
        <TextRegion id="r02" type="paragraph">
            <Coords points="100,500 600,200 100,200 300,900" />
        </TextRegion>
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
        self.assertNotEqual(region, None)
        self.assertIsInstance(region, TextRegion)
        self.assertEqual(region.id, "r0")

    def test_nested_text_regions(self):
        region: Optional[TextRegion] = Region.from_element(
            NESTED_TEXT_REGIONS, {}
        )
        self.assertNotEqual(region, None)
        self.assertIsInstance(region, TextRegion)
        self.assertEqual(region.id, "r0")
        self.assertEqual(region.region_type, TextRegionType.CAPTION)
        self.assertEqual(len(region.children), 2)
        self.assertEqual(
            region.coords,
            [Point(0, 0), Point(300, 400), Point(800, 600), Point(100, 200)]
        )

        child1, child2 = region.children[0], region.children[1]
        self.assertNotEqual(child1, None)
        self.assertNotEqual(child2, None)
        self.assertIsInstance(child1, TextRegion)
        self.assertIsInstance(child2, TextRegion)

        self.assertEqual(child1.id, "r01")
        self.assertEqual(child1.region_type, TextRegionType.HEADING)
        self.assertEqual(
            child1.coords,
            [Point(100, 200), Point(600, 200), Point(400, 500), Point(300, 900)]
        )

        self.assertEqual(child2.id, "r02")
        self.assertEqual(child2.region_type, TextRegionType.PARAGRAPH)
        self.assertEqual(
            child2.coords,
            [Point(100, 500), Point(600, 200), Point(100, 200), Point(300, 900)]
        )
