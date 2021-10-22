import unittest
from page import Page
from page.exceptions import PageXMLError

EXAMPLE_SIMPLE = "page/test/files/metadata/simple.xml"
EXAMPLE_NO_COMMENT = "page/test/files/metadata/no_comment.xml"
EXAMPLE_MALFORMED_DATE = "page/test/files/metadata/malformed_date.xml"
EXAMPLE_EMPTY_CREATOR = "page/test/files/metadata/empty_creator.xml"
EXAMPLE_EMPTY_COMMENT = "page/test/files/metadata/empty_comment.xml"


class TestParseMetadata(unittest.TestCase):
    def test_simple(self):
        with open(EXAMPLE_SIMPLE, "r") as file:
            page = Page.from_file(file)
            meta = page.metadata

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
        with open(EXAMPLE_EMPTY_CREATOR, "r") as file:
            page = Page.from_file(file)
            meta = page.metadata
            self.assertEqual(meta.creator, "")

    def test_no_comment(self):
        with open(EXAMPLE_NO_COMMENT, "r") as file:
            page = Page.from_file(file)
            meta = page.metadata
            self.assertEqual(meta.comments, None)

    def test_empty_comment(self):
        with open(EXAMPLE_EMPTY_COMMENT, "r") as file:
            page = Page.from_file(file)
            meta = page.metadata
            self.assertEqual(meta.comments, "")

    def test_malformed_date(self):
        with open(EXAMPLE_MALFORMED_DATE, "r") as file:
            self.assertRaises(PageXMLError, lambda: Page.from_file(file))


if __name__ == "__main__":
    unittest.main()
