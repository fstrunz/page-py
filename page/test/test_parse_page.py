import unittest
from lxml import etree
from page.elements import Page, TextRegion
from page.exceptions import PageXMLError
import page.test.assert_utils as utils

EMPTY_PAGE = etree.XML(
    """<Page imageFilename="test.png" imageWidth="1024" imageHeight="768">
    </Page>"""
)

INVALID_PAGE_ATTRIBS = etree.XML(
    """<Page imageFilename="test.png" imageWidth="abc" imageHeight="768">
    </Page>"""
)

SIMPLE_PAGE = etree.XML(
    """<Page imageFilename="test.jpg" imageWidth="100" imageHeight="400">
        <TextRegion id="r0" type="paragraph">
            <Coords points="0,0 1,1 2,2" />
        </TextRegion>
    </Page>"""
)

COMPLEX_PAGE = etree.XML(
    """<Page imageFilename="test.tga" imageWidth="392" imageHeight="400">
        <ReadingOrder>
            <OrderedGroup id="g1">
                <RegionRefIndexed index="0" regionRef="r0" />
                <RegionRefIndexed index="1" regionRef="r1" />
                <RegionRefIndexed index="2" regionRef="r2" />
            </OrderedGroup>
        </ReadingOrder>
        <TextRegion id="r0" type="paragraph">
            <Coords points="0,0 1,1 2,2" />
            <TextRegion id="r01" type="paragraph">
                <Coords points="0,0 4,4 0,0" />
            </TextRegion>
        </TextRegion>
        <TextRegion id="r1" type="paragraph">
            <Coords points="2,2 1,1 0,1" />
        </TextRegion>
        <NotARegion id="r2">
            <Coords points="0,1 12,1 0,1" />
        </NotARegion>
    </Page>"""
)


class TestParsePage(unittest.TestCase):
    def test_parse_empty_page(self):
        page = Page.from_element(EMPTY_PAGE, {})
        self.assertEqual(page.image_filename, "test.png")
        self.assertEqual(page.image_size, (1024, 768))

    def test_parse_page_invalid_attribs(self):
        self.assertRaises(
            PageXMLError,
            lambda: Page.from_element(INVALID_PAGE_ATTRIBS, {})
        )

    def test_parse_simple_page(self):
        page = Page.from_element(SIMPLE_PAGE, {})
        self.assertEqual(page.image_filename, "test.jpg")
        self.assertEqual(page.image_size, (100, 400))
        self.assertEqual(len(page.regions), 1)
        self.assertEqual(page.regions[0].id, "r0")
        self.assertIsInstance(page.regions[0], TextRegion)

    def test_parse_complex_page(self):
        page = Page.from_element(COMPLEX_PAGE, {})
        self.assertEqual(page.image_filename, "test.tga")
        self.assertEqual(page.image_size, (392, 400))
        self.assertEqual(len(page.regions), 2)

        region_ids = {region.id for region in page.regions}
        self.assertIn("r0", region_ids)
        self.assertIn("r1", region_ids)
        self.assertNotIn("r2", region_ids)
        self.assertNotIn("r01", region_ids)

        for region in page.regions:
            self.assertIsInstance(region, TextRegion)

    def test_parse_page_invert(self):
        for xml in [EMPTY_PAGE, SIMPLE_PAGE]:
            utils.assert_same_descendant_tags(
                self,
                Page.from_element(xml, {}).to_element({}),
                xml
            )

        # we cannot use assert_same_descendant_tags for
        # COMPLEX_PAGE because from_element filters out non-regions
        # like NotARegion.
        #
        # instead, check if it contains all valid TextRegions

        page_xml = Page.from_element(COMPLEX_PAGE, {}).to_element({})
        region_ids = page_xml.xpath("./TextRegion/@id")

        self.assertIn("r0", region_ids)
        self.assertIn("r1", region_ids)
        self.assertNotIn("r2", region_ids)
        self.assertNotIn("g1", region_ids)
