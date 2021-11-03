import unittest
from lxml import etree
from page import Page
from page.elements.region import TextRegion
from page.exceptions import PageXMLError
import page.test.assert_utils as utils

NO_METADATA = etree.XML(
    """<Page imageFilename="test.png" imageWidth="1024" imageHeight="768">
    </Page>"""
)

EMPTY_PAGE = etree.XML(
    """<Page imageFilename="test.png" imageWidth="1024" imageHeight="768">
        <Metadata>
            <Creator>Test Creator</Creator>
            <Created>2021-10-21T18:37:36</Created>
            <LastChange>1970-01-01T00:00:00</LastChange>
            <Comments>Test Comment</Comments>
        </Metadata>
    </Page>"""
)

INVALID_PAGE_ATTRIBS = etree.XML(
    """<Page imageFilename="test.png" imageWidth="abc" imageHeight="768">
        <Metadata>
            <Creator>Test Creator</Creator>
            <Created>2021-10-21T18:37:36</Created>
            <LastChange>1970-01-01T00:00:00</LastChange>
            <Comments>Test Comment</Comments>
        </Metadata>
    </Page>"""
)

SIMPLE_PAGE = etree.XML(
    """<Page imageFilename="test.jpg" imageWidth="100" imageHeight="400">
        <Metadata>
            <Creator>Test Creator</Creator>
            <Created>2021-10-21T18:37:36</Created>
            <LastChange>1970-01-01T00:00:00</LastChange>
            <Comments>Test Comment</Comments>
        </Metadata>
        <TextRegion id="r0" type="paragraph">
            <Coords points="0,0 1,1 2,2" />
        </TextRegion>
    </Page>"""
)

COMPLEX_PAGE = etree.XML(
    """<Page imageFilename="test.tga" imageWidth="392" imageHeight="400">
        <Metadata>
            <Creator>Test Creator</Creator>
            <Created>2021-10-21T18:37:36</Created>
            <LastChange>1970-01-01T00:00:00</LastChange>
            <Comments>Test Comment</Comments>
        </Metadata>
        <TextRegion id="r0" type="paragraph">
            <Coords points="0,0 1,1 2,2" />
            <TextRegion id="r01" type="paragraph">
                <Coords points="0,0 4,4 0,0" />
            </TextRegion>
        </TextRegion>
        <TextRegion id="r1" type="paragraph">
            <Coords points="2,2 1,1 0,1" />
        </TextRegion>
    </Page>
    """
)


class TestParsePage(unittest.TestCase):
    def test_parse_page_no_metadata(self):
        self.assertRaises(
            PageXMLError,
            lambda: Page.from_element(NO_METADATA, {})
        )

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
        self.assertNotIn("r01", region_ids)

        for region in page.regions:
            self.assertIsInstance(region, TextRegion)

    def test_parse_page_invert(self):
        for xml in [EMPTY_PAGE, SIMPLE_PAGE, COMPLEX_PAGE]:
            utils.assert_same_descendant_tags(
                self,
                Page.from_element(xml, {}).to_element({}),
                xml
            )
