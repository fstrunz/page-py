import unittest
from lxml import etree
from page.elements import Line, IndexedLine, Text, Point
from page.exceptions import PageXMLError
import page.test.assert_utils as utils

SIMPLE_TEXT_LINE = etree.XML(
    """<TextLine id="l0">
        <Coords points="0,0 1,1 2,2" />
        <TextEquiv>
            <Unicode>test</Unicode>
        </TextEquiv>
    </TextLine>"""
)

EMPTY_TEXT_LINE = etree.XML(
    """<TextLine id="l3">
        <Coords points="0,0 1,1 2,2" />
    </TextLine>"""
)

INDEXED_TEXT_LINE = etree.XML(
    """<TextLine id="l0">
        <Coords points="0,0 1,1 2,2" />
        <TextEquiv index="0">
            <Unicode>text alternative 1</Unicode>
        </TextEquiv>
        <TextEquiv index="1">
            <Unicode>text alternative 2</Unicode>
        </TextEquiv>
    </TextLine>"""
)

# This is not allowed, either we have multiple indexed elements,
# or at most one unindexed element.
MIXED_INDEXED_NOT_INDEXED = etree.XML(
    """<TextLine id="l1">
        <Coords points="0,0 1,1 2,2" />
        <TextEquiv>
            <Unicode>text alternative 1</Unicode>
        </TextEquiv>
        <TextEquiv index="1">
            <Unicode>text alternative 2</Unicode>
        </TextEquiv>
    </TextLine>"""
)


class TestParseLine(unittest.TestCase):
    def test_simple_line(self):
        line: Line = Line.from_element(SIMPLE_TEXT_LINE, {})

        self.assertNotIsInstance(line, IndexedLine)
        self.assertEqual(line.line_id, "l0")
        self.assertEqual(line.text, Text(None, "test", None))
        self.assertEqual(
            line.coords.points,
            [Point(0, 0), Point(1, 1), Point(2, 2)]
        )

    def test_empty_line(self):
        line: Line = Line.from_element(EMPTY_TEXT_LINE, {})

        self.assertNotIsInstance(line, IndexedLine)
        self.assertEqual(line.line_id, "l3")
        self.assertIsNone(line.text)
        self.assertEqual(
            line.coords.points,
            [Point(0, 0), Point(1, 1), Point(2, 2)]
        )

    def test_indexed_line(self):
        line: Line = Line.from_element(INDEXED_TEXT_LINE, {})
        self.assertEqual(line.text, Text(0, "text alternative 1", None))
        self.assertIsInstance(line, IndexedLine)
        line: IndexedLine = line

        self.assertEqual(line.line_id, "l0")
        self.assertEqual(len(line.texts()), 2)

        text0 = Text(0, "text alternative 1", None)
        text1 = Text(1, "text alternative 2", None)

        self.assertIn(text0, line.texts())
        self.assertIn(text1, line.texts())

        self.assertEqual(line.get_from_index(0), text0)
        self.assertEqual(line.get_from_index(1), text1)

    def test_mixed_indexed_not_indexed_line(self):
        self.assertRaises(
            PageXMLError,
            lambda: Line.from_element(MIXED_INDEXED_NOT_INDEXED, {})
        )

    def test_parse_line_invert(self):
        for xml in [
            SIMPLE_TEXT_LINE,
            INDEXED_TEXT_LINE
        ]:
            utils.assert_same_descendant_tags(
                self,
                Line.from_element(xml, {}).to_element({}),
                xml
            )
