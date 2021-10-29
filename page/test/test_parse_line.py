import unittest
from lxml import etree
from page.elements import Line, IndexedLine, Text, Point

SIMPLE_TEXT_LINE = etree.XML(
    """<TextLine id="l0">
        <Coords points="0,0 1,1 2,2" />
        <TextEquiv>
            <Unicode>test</Unicode>
        </TextEquiv>
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


class TestParseLine(unittest.TestCase):
    def test_simple_line(self):
        line: Line = Line.from_element(SIMPLE_TEXT_LINE, {})

        self.assertNotIsInstance(line, IndexedLine)
        self.assertEqual(line.id, "l0")
        self.assertEqual(line.texts, [Text(None, "test", None)])
        self.assertEqual(line.coords, [Point(0, 0), Point(1, 1), Point(2, 2)])

    def test_indexed_line(self):
        line: Line = Line.from_element(INDEXED_TEXT_LINE, {})

        self.assertEqual(line.id, "l0")
        self.assertEqual(len(line.texts), 2)

        text0 = Text(0, "text alternative 1", None)
        text1 = Text(1, "text alternative 2", None)

        self.assertIn(text0, line.texts)
        self.assertIn(text1, line.texts)

        self.assertIsInstance(line, IndexedLine)

        indexed_line: IndexedLine = line
        self.assertEqual(indexed_line.get_text_from_index(0), text0)
        self.assertEqual(indexed_line.get_text_from_index(1), text1)
