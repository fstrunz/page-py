import unittest
from lxml import etree
from page.elements import Text
from page.exceptions import PageXMLError

SIMPLE_TEXT_EQUIV = etree.XML(
    """<TextEquiv>
        <PlainText>test</PlainText>
        <Unicode>𝓽𝓮𝓼𝓽</Unicode>
    </TextEquiv>"""
)

NO_UNICODE_TAG_TEXT_EQUIV = etree.XML(
    """<TextEquiv>
        <PlainText>test</PlainText>
    </TextEquiv>"""
)

INDEXED_TEXT_EQUIV = etree.XML(
    """<TextEquiv index="56">
        <PlainText>test</PlainText>
        <Unicode>𝓽𝓮𝓼𝓽</Unicode>
    </TextEquiv>"""
)

INVALID_INDEXED_TEXT_EQUIV = etree.XML(
    """<TextEquiv index="☢💙  𝐍𝕆ｔ 𝓐𝕟 ιη𝓓𝑒Ｘ  💙💥">
        <PlainText>test</PlainText>
        <Unicode>𝓽𝓮𝓼𝓽</Unicode>
    </TextEquiv>"""
)


class TestParseText(unittest.TestCase):
    def test_simple_text(self):
        text: Text = Text.from_element(SIMPLE_TEXT_EQUIV, {})
        self.assertEqual(text, Text(None, "𝓽𝓮𝓼𝓽", "test"))

    def test_indexed_text(self):
        text: Text = Text.from_element(INDEXED_TEXT_EQUIV, {})
        self.assertEqual(text, Text(56, "𝓽𝓮𝓼𝓽", "test"))

    def test_invalid_text(self):
        self.assertRaises(
            PageXMLError,
            lambda: Text.from_element(INVALID_INDEXED_TEXT_EQUIV, {})
        )

    def test_no_unicode_tag(self):
        self.assertRaises(
            PageXMLError,
            lambda: Text.from_element(NO_UNICODE_TAG_TEXT_EQUIV, {})
        )
