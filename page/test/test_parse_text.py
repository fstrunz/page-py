import unittest
from lxml import etree
from page.elements import Text
from page.exceptions import PageXMLError
import page.test.assert_utils as utils

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

EMPTY_UNICODE_TAG_TEXT_EQUIV = etree.XML(
    """<TextEquiv>
        <Unicode />
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

TEXT_EQUIV_WITH_CONFIDENCE = etree.XML(
    """<TextEquiv conf="0.5">
        <Unicode>test</Unicode>
    </TextEquiv>"""
)

TEST_EQUIV_WITH_INVALID_CONFIDENCE = etree.XML(
    """<TextEquiv conf="1.0">
        <Unicode>invalid</Unicode>
    </TextEquiv>"""
)


class TestParseText(unittest.TestCase):
    def test_simple_text(self):
        text: Text = Text.from_element(SIMPLE_TEXT_EQUIV, {})
        self.assertEqual(text, Text(None, "𝓽𝓮𝓼𝓽", "test"))

    def test_indexed_text(self):
        text: Text = Text.from_element(INDEXED_TEXT_EQUIV, {})
        self.assertEqual(text, Text(56, "𝓽𝓮𝓼𝓽", "test"))

    def test_empty_unicode_tag(self):
        text: Text = Text.from_element(EMPTY_UNICODE_TAG_TEXT_EQUIV, {})
        self.assertEqual(text, Text(None, "", None))

    def test_text_equiv_with_confidence(self):
        text: Text = Text.from_element(TEXT_EQUIV_WITH_CONFIDENCE, {})
        self.assertAlmostEqual(text.conf, 0.5)

    def test_text_equiv_with_invalid_confidence(self):
        self.assertRaises(
            PageXMLError,
            lambda: Text.from_element(TEST_EQUIV_WITH_INVALID_CONFIDENCE, {})
        )

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

    def test_parse_text_invert(self):
        for xml in [
            SIMPLE_TEXT_EQUIV,
            INDEXED_TEXT_EQUIV,
            TEXT_EQUIV_WITH_CONFIDENCE
        ]:
            utils.assert_same_descendant_tags(
                self,
                Text.from_element(xml, {}).to_element({}),
                xml
            )
