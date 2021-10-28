import unittest
from lxml import etree
from page.elements.line import Line
from page.elements.text import Text
from page.elements.point import Point

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

        self.assertEqual(line.id, "l0")
        self.assertEqual(line.texts, [Text(None, "test", None)])
        self.assertEqual(line.coords, [Point(0, 0), Point(1, 1), Point(2, 2)])

    def test_indexed_line(self):
        line: Line = Line.from_element(INDEXED_TEXT_LINE, {})

        self.assertEqual(line.id, "l0")
        self.assertEqual(len(line.texts), 2)

        self.assertIn(Text(0, "text alternative 1", None), line.texts)
        self.assertIn(Text(1, "text alternative 2", None), line.texts)
