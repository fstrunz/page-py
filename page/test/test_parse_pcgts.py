import unittest
import page.test.assert_utils as utils
from page.elements import PcGts
from lxml import etree

SIMPLE_PCGTS = etree.XML(
    """<PcGts>
        <Metadata>
            <Creator>Test Creator</Creator>
            <Created>2021-10-21T18:37:36</Created>
            <LastChange>1970-01-01T00:00:00</LastChange>
            <Comments>Test Comment</Comments>
        </Metadata>
        <Page
            imageFilename="test.png"
            imageWidth="1024"
            imageHeight="768"></Page>
    </PcGts>"""
)


SIMPLE_PCGTS_WITH_ID = etree.XML(
    """<PcGts pcGtsId="gt4">
        <Metadata>
            <Creator>Test Creator</Creator>
            <Created>2021-10-21T18:37:36</Created>
            <LastChange>1970-01-01T00:00:00</LastChange>
            <Comments>Test Comment</Comments>
        </Metadata>
        <Page imageFilename="test.png" imageWidth="1024" imageHeight="768">
        </Page>
    </PcGts>"""
)


class TestParsePcGts(unittest.TestCase):
    def test_parse_simple_pcgts(self):
        pcgts_xml = PcGts.from_element(SIMPLE_PCGTS, {})
        self.assertIsNone(pcgts_xml.pc_gts_id)
        self.assertIsNotNone(pcgts_xml.page)
        self.assertIsNotNone(pcgts_xml.metadata)

    def test_parse_pcgts_with_id(self):
        pcgts_xml = PcGts.from_element(SIMPLE_PCGTS_WITH_ID, {})
        self.assertEqual(pcgts_xml.pc_gts_id, "gt4")
        self.assertIsNotNone(pcgts_xml.page)
        self.assertIsNotNone(pcgts_xml.metadata)

    def test_parse_pcgts_invert(self):
        for xml in [SIMPLE_PCGTS, SIMPLE_PCGTS_WITH_ID]:
            utils.assert_same_descendant_tags(
                self,
                PcGts.from_element(xml, {}).to_element({}),
                xml
            )
