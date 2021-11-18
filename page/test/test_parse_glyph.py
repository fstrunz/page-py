import unittest
from lxml import etree
from page.elements.glyph import Glyph, IndexedGlyph
from page.elements.point import Point
from page.elements.text import Text
from page.exceptions import PageXMLError
import page.test.assert_utils as utils

SIMPLE_GLYPH = etree.XML(
    """<Glyph id="w0g0">
        <Coords points="0,1 2,3 4,5" />
    </Glyph>"""
)

GLYPH_WITH_TEXT = etree.XML(
    """<Glyph id="w0g1">
        <Coords points="5,4 3,2 1,0" />
        <TextEquiv>
            <PlainText>ue</PlainText>
            <Unicode>ü</Unicode>
        </TextEquiv>
    </Glyph>"""
)

GLYPH_WITHOUT_TEXT = etree.XML(
    """<Glyph id="w0g2">
        <Coords points="5,4 3,2 1,0" />
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

GLYPH_WITH_INDEXED_TEXT = etree.XML(
    """<Glyph id="w0g3">
        <Coords points="5,4 3,2 1,0" />
        <TextEquiv index="0">
            <Unicode>ü</Unicode>
        </TextEquiv>
        <TextEquiv index="45">
            <Unicode>ä</Unicode>
        </TextEquiv>
    </Glyph>"""
)

GLYPH_WITH_INDEXED_AND_UNINDEXED_TEXT = etree.XML(
    """<Glyph id="w0g3">
        <Coords points="5,4 3,2 1,0" />
        <TextEquiv index="0">
            <Unicode>ü</Unicode>
        </TextEquiv>
        <TextEquiv>
            <Unicode>ä</Unicode>
        </TextEquiv>
    </Glyph>"""
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
        self.assertEqual(glyph.text, Text(None, "ü", "ue"))

    def test_parse_glyph_without_text(self):
        glyph: Glyph = Glyph.from_element(GLYPH_WITHOUT_TEXT, {})
        self.assertEqual(glyph.glyph_id, "w0g2")
        self.assertIsNone(glyph.text)

    def test_parse_glyph_without_id(self):
        self.assertRaises(
            PageXMLError,
            lambda: Glyph.from_element(GLYPH_WITHOUT_ID, {})
        )

    def test_parse_glyph_without_coords(self):
        self.assertRaises(
            PageXMLError,
            lambda: Glyph.from_element(GLYPH_WITHOUT_COORDS, {})
        )

    def test_parse_glyph_indexed_text(self):
        glyph: Glyph = Glyph.from_element(GLYPH_WITH_INDEXED_TEXT, {})
        self.assertEqual(glyph.glyph_id, "w0g3")
        self.assertIsInstance(glyph, IndexedGlyph)

        glyph: IndexedGlyph = glyph
        self.assertEqual(len(glyph.texts()), 2)
        self.assertEqual(glyph.get_from_index(0), Text(0, "ü", None))
        self.assertEqual(glyph.get_from_index(45), Text(45, "ä", None))

    def test_parse_glyph_indexed_unindexed_text(self):
        self.assertRaises(
            PageXMLError,
            lambda: Glyph.from_element(
                GLYPH_WITH_INDEXED_AND_UNINDEXED_TEXT, {}
            )
        )

    def test_parse_glyph_invert(self):
        for xml in [
            SIMPLE_GLYPH,
            GLYPH_WITH_TEXT,
            GLYPH_WITH_INDEXED_TEXT
        ]:
            utils.assert_same_descendant_tags(
                self,
                Glyph.from_element(xml, {}).to_element({}),
                xml
            )
