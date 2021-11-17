import unittest
from typing import Optional
from lxml import etree
from page.elements import Region, TextRegion, TextRegionType, Point
from page.exceptions import PageXMLError
import page.test.assert_utils as utils

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

NO_COORDS_TEXT_REGION_1 = etree.XML(
    """<TextRegion id="r0" type="caption">
        <TextRegion id="r01" type="heading">
            <Coords points="100,200 600,200 400,500 300,900" />
        </TextRegion>
        <TextRegion id="r02" type="paragraph">
            <Coords points="100,500 600,200 100,200 300,900" />
        </TextRegion>
    </TextRegion>"""
)

NO_COORDS_TEXT_REGION_2 = etree.XML(
    """<TextRegion id="r0" type="caption">
        <Coords points="0,0 300,400 800,600 100,200" />
        <TextRegion id="r01" type="heading">
            <Coords points="100,200 600,200 400,500 300,900" />
        </TextRegion>
        <TextRegion id="r02" type="paragraph"></TextRegion>
    </TextRegion>"""
)

NO_COORDS_TEXT_REGION_3 = etree.XML(
    """<TextRegion id="r0" type="caption">
        <Coords />
    </TextRegion>"""
)

REGION_INVALID_TYPE_1 = etree.XML(
    """<TextRegion id="r0">
        <Coords points="0,0 300,400 800,600 100,200" />
    </TextRegion>"""
)

REGION_INVALID_TYPE_2 = etree.XML(
    """<TextRegion id="r0" type="𝐧𝐨𝐭 𝐚 𝐭𝐲𝐩𝐞">
        <Coords points="0,0 300,400 800,600 100,200" />
    </TextRegion>"""
)

TRAVERSE_CHILDREN = etree.XML(
    """<TextRegion id="r8" type="floating">
        <Coords points="0,0 300,400 800,600 100,200" />
        <TextRegion id="r3" type="heading">
            <Coords points="100,200 600,200 400,500 300,900" />
        </TextRegion>
        <NotARegion id="r1">
            <Coords points="100,500 600,200 100,200 300,900" />
        </NotARegion>
        <TextRegion id="r4" type="paragraph">
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
            text_region.coords.points,
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
            region.coords.points,
            [
                Point(0, 0), Point(300, 400),
                Point(800, 600), Point(100, 200)
            ]
        )

        child1, child2 = region.children[0], region.children[1]
        self.assertNotEqual(child1, None)
        self.assertNotEqual(child2, None)
        self.assertIsInstance(child1, TextRegion)
        self.assertIsInstance(child2, TextRegion)

        self.assertEqual(child1.id, "r01")
        self.assertEqual(child1.region_type, TextRegionType.HEADING)
        self.assertEqual(
            child1.coords.points,
            [
                Point(100, 200), Point(600, 200),
                Point(400, 500), Point(300, 900)
            ]
        )

    def test_region_no_coords(self):
        for test_xml in [
            NO_COORDS_TEXT_REGION_1,
            NO_COORDS_TEXT_REGION_2,
            NO_COORDS_TEXT_REGION_3
        ]:
            self.assertRaises(
                PageXMLError, lambda: TextRegion.from_element(test_xml, {})
            )

    def test_region_invalid_type(self):
        for test_xml in [
            REGION_INVALID_TYPE_1,
            REGION_INVALID_TYPE_2
        ]:
            self.assertRaises(
                PageXMLError,
                lambda: TextRegion.from_element(test_xml, {})
            )

    def test_region_traverse_children(self):
        region: TextRegion = TextRegion.from_element(TRAVERSE_CHILDREN, {})
        region_ids = [child.id for child in region.children]
        self.assertIn("r3", region_ids)
        self.assertIn("r4", region_ids)
        self.assertNotIn("r8", region_ids)  # invalid region
        self.assertNotIn("r1", region_ids)  # parent

    def test_parse_text_region_invert(self):
        for test_xml in [
            SIMPLE_TEXT_REGION,
            NESTED_TEXT_REGIONS
        ]:
            utils.assert_same_descendant_tags(
                self,
                TextRegion.from_element(test_xml, {}).to_element({}),
                test_xml
            )
