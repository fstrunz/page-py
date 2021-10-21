import unittest
from page import Page

EXAMPLE_SIMPLE = "page/test/files/simple.xml"
EXAMPLE_NO_COMMENT = "page/test/files/no_comment.xml"
EXAMPLE_MALFORMED_DATE = "page/test/files/malformed_date.xml"
EXAMPLE_EMPTY_CREATOR = "page/test/files/empty_creator.xml"


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


if __name__ == "__main__":
    unittest.main()
