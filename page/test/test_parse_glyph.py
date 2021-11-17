import unittest
from lxml import etree
from page.elements.glyph import Glyph
from page.elements.point import Point

SIMPLE_GLYPH = etree.XML(
    """<Glyph id="w0g0">
        <Coords points="0,1 2,3 4,5" />
    </Glyph>"""
)

GLYPH_WITH_TEXT = etree.XML(
    """<Glyph id="w0g1">
        <Coords points="5,4 3,2 1,0" />
        <TextEquiv index="3">
            <Unicode>ü</Unicode>
        </TextEquiv>
    </Glyph>"""
)

GLYPH_WITHOUT_ID = etree.XML(
    """<Glyph>
        <Coords points="5,4 3,2 1,0" />
    </Glyph>"""
)

GLYPH_WITHOUT_COORDS = etree.XML(
    """<Glyph id="w0g2"></Glyph>"""
)


class TestParseGlyph(unittest.TestCase):
    def test_parse_simple_glyph(self):
        glyph: Glyph = Glyph.from_element(SIMPLE_GLYPH, {})
        self.assertEqual(glyph.glyph_id, "w0g0")
        self.assertEqual(
            glyph.coords.points,
            [Point(0, 1), Point(2, 3), Point(4, 5)]
        )

    def test_parse_glyph_with_text(self):
        glyph: Glyph = Glyph.from_element(GLYPH_WITH_TEXT, {})
        self.assertEqual(glyph.glyph_id, "w0g1")
        self.assertIsNotNone(glyph.text)
