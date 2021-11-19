import unittest
from lxml import etree

from page.elements.point import Point
from page.elements.word import IndexedWord, Word
from page.elements.text import Text
import page.test.assert_utils as utils

SIMPLE_WORD = etree.XML(
    """<Word id="w0">
        <Coords points="3421,2358 932,182 8345,3482 1392,4738" />
    </Word>"""
)

SIMPLE_WORD_WITH_TEXT = etree.XML(
    """<Word id="w1">
        <Coords points="3421,2358 932,182 8345,3482 1392,4738" />
        <TextEquiv>
            <PlainText>ae</PlainText>
            <Unicode>ä</Unicode>
        </TextEquiv>
    </Word>"""
)

WORD_WITH_GLYPHS = etree.XML(
    """<Word id="w2">
        <Coords points="3421,2358 932,182 8345,3482 1392,4738" />
        <Glyph id="w2g0">
            <Coords points="0,0 1,1" />
            <TextEquiv><Unicode>t</Unicode></TextEquiv>
        </Glyph>
        <Glyph id="w2g1">
            <Coords points="0,0 1,1" />
            <TextEquiv><Unicode>e</Unicode></TextEquiv>
        </Glyph>
        <Glyph id="w2g2">
            <Coords points="0,0 1,1" />
            <TextEquiv><Unicode>s</Unicode></TextEquiv>
        </Glyph>
        <Glyph id="w2g3">
            <Coords points="0,0 1,1" />
            <TextEquiv><Unicode>t</Unicode></TextEquiv>
        </Glyph>
        <TextEquiv>
            <Unicode>test</Unicode>
        </TextEquiv>
    </Word>"""
)

INDEXED_WORD_WITH_GLYPHS = etree.XML(
    """<Word id="w3">
        <Coords points="3421,2358 932,182 8345,3482 1392,4738" />
        <Glyph id="w3g0">
            <Coords points="0,0 1,1" />
            <TextEquiv index="0"><Unicode>a</Unicode></TextEquiv>
            <TextEquiv index="1"><Unicode>c</Unicode></TextEquiv>
        </Glyph>
        <Glyph id="w3g1">
            <Coords points="0,0 1,1" />
            <TextEquiv index="0"><Unicode>b</Unicode></TextEquiv>
            <TextEquiv index="1"><Unicode>b</Unicode></TextEquiv>
        </Glyph>
        <Glyph id="w3g2">
            <Coords points="0,0 1,1" />
            <TextEquiv index="0"><Unicode>c</Unicode></TextEquiv>
            <TextEquiv index="1"><Unicode>a</Unicode></TextEquiv>
        </Glyph>
        <TextEquiv index="0">
            <Unicode>abc</Unicode>
        </TextEquiv>
        <TextEquiv index="1">
            <Unicode>cba</Unicode>
        </TextEquiv>
    </Word>"""
)


class TestParseWord(unittest.TestCase):
    def test_parse_simple_word(self):
        word: Word = Word.from_element(SIMPLE_WORD, {})
        self.assertEqual(word.word_id, "w0")
        self.assertEqual(
            word.coords.points,
            [Point(3421, 2358), Point(932, 182),
             Point(8345, 3482), Point(1392, 4738)]
        )
        self.assertNotIsInstance(word, IndexedWord)
        self.assertIsNone(word.text)

    def test_parse_simple_word_with_text(self):
        word: Word = Word.from_element(SIMPLE_WORD_WITH_TEXT, {})
        self.assertEqual(word.word_id, "w1")
        self.assertEqual(
            word.coords.points,
            [Point(3421, 2358), Point(932, 182),
             Point(8345, 3482), Point(1392, 4738)]
        )
        self.assertNotIsInstance(word, IndexedWord)
        self.assertEqual(word.text, Text(None, "ä", "ae"))

    def test_parse_word_with_glyphs(self):
        word: Word = Word.from_element(WORD_WITH_GLYPHS, {})
        self.assertEqual(word.word_id, "w2")
        self.assertEqual(len(word.glyphs), 4)
        self.assertEqual(word.glyphs[0].text, Text(None, "t", None))
        self.assertEqual(word.glyphs[1].text, Text(None, "e", None))
        self.assertEqual(word.glyphs[2].text, Text(None, "s", None))
        self.assertEqual(word.glyphs[3].text, Text(None, "t", None))
        self.assertNotIsInstance(word, IndexedWord)
        self.assertEqual(word.text, Text(None, "test", None))

    def test_parse_indexed_word_with_glyphs(self):
        word: Word = Word.from_element(INDEXED_WORD_WITH_GLYPHS, {})
        self.assertEqual(word.word_id, "w3")
        self.assertEqual(len(word.glyphs), 3)
        self.assertIsInstance(word, IndexedWord)
        word: IndexedWord = word
        self.assertEqual(word.get_from_index(0), Text(0, "abc", None))
        self.assertEqual(word.get_from_index(1), Text(1, "cba", None))

    def test_parse_word_invert(self):
        for xml in [
            SIMPLE_WORD,
            SIMPLE_WORD_WITH_TEXT,
            WORD_WITH_GLYPHS,
            INDEXED_WORD_WITH_GLYPHS
        ]:
            utils.assert_same_descendant_tags(
                self,
                Word.from_element(xml, {}).to_element({}),
                xml
            )
