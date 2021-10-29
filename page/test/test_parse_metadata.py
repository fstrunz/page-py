import unittest
from page.exceptions import PageXMLError
from page.elements import Metadata
from lxml import etree

SIMPLE_METADATA = etree.XML(
    """<Metadata>
        <Creator>Test Creator</Creator>
        <Created>2021-10-21T18:37:36</Created>
        <LastChange>1970-01-01T00:00:00</LastChange>
        <Comments>Test Comment</Comments>
    </Metadata>"""
)

NO_COMMENT_METADATA = etree.XML(
    """<Metadata>
        <Creator>Test Creator</Creator>
        <Created>2021-10-21T18:37:36</Created>
        <LastChange>1970-01-01T00:00:00</LastChange>
    </Metadata>"""
)

MALFORMED_DATE_METADATA = etree.XML(
    """<Metadata>
        <Creator>Test Creator</Creator>
        <Created>invalid date</Created>
        <LastChange>ᓰᘉᐺᗩᒪᓰᕲ ᕲᗩᖶᘿ</LastChange>
        <Comments>Test Comment</Comments>
    </Metadata>"""
)

EMPTY_CREATOR_METADATA = etree.XML(
    """<Metadata>
        <Creator/>
        <Created>2021-10-21T18:37:36</Created>
        <LastChange>1970-01-01T00:00:00</LastChange>
        <Comments>Test Comment</Comments>
    </Metadata>"""
)

EMPTY_COMMENT_METADATA = etree.XML(
    """<Metadata>
        <Creator>Test Creator</Creator>
        <Created>2021-10-21T18:37:36</Created>
        <LastChange>1970-01-01T00:00:00</LastChange>
        <Comments></Comments>
    </Metadata>
    """
)


class TestParseMetadata(unittest.TestCase):
    def test_simple(self):
        meta = Metadata.from_element(SIMPLE_METADATA, {})

        self.assertEqual(meta.creator, "Test Creator")
        self.assertEqual(meta.comments, "Test Comment")

        created = (
            meta.created.year,
            meta.created.month,
            meta.created.day
        )
        self.assertEqual(created, (2021, 10, 21))

        last_change = (
            meta.last_change.year,
            meta.last_change.month,
            meta.last_change.day
        )
        self.assertEqual(last_change, (1970, 1, 1))

    def test_empty_creator(self):
        meta = Metadata.from_element(EMPTY_CREATOR_METADATA, {})
        self.assertEqual(meta.creator, "")

    def test_no_comment(self):
        meta = Metadata.from_element(NO_COMMENT_METADATA, {})
        self.assertEqual(meta.comments, None)

    def test_empty_comment(self):
        meta = Metadata.from_element(EMPTY_COMMENT_METADATA, {})
        self.assertEqual(meta.comments, "")

    def test_malformed_date(self):
        self.assertRaises(
            PageXMLError,
            lambda: Metadata.from_element(MALFORMED_DATE_METADATA, {})
        )
