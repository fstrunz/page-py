import unittest
from page.elements.coords import Baseline, Coordinates
from page.elements.point import Point
from page.exceptions import PageXMLError
import page.test.assert_utils as utils
from lxml import etree

SIMPLE_COORDS = etree.XML(
    """<Coords points="0,0 1,1 2,2" />"""
)

NO_POINTS_ATTRIB = etree.XML(
    """<Coords />"""
)

SIMPLE_BASELINE = etree.XML(
    """<Baseline points="2,2 1,1 0,0" />"""
)


class TestParseCoords(unittest.TestCase):
    def test_parse_simple_coords(self):
        coords = Coordinates.from_element(SIMPLE_COORDS, {})
        self.assertEqual(coords.points, [
            Point(0, 0), Point(1, 1), Point(2, 2)
        ])

    def test_parse_coords_missing_points(self):
        self.assertRaises(
            PageXMLError,
            lambda: Coordinates.from_element(NO_POINTS_ATTRIB, {})
        )

    def test_parse_coords_invert(self):
        utils.assert_same_descendant_tags(
            self,
            Coordinates.from_element(SIMPLE_COORDS, {}).to_element({}),
            SIMPLE_COORDS
        )

    def test_parse_baseline(self):
        baseline = Baseline.from_element(SIMPLE_BASELINE, {})
        self.assertEqual(baseline.points, [
            Point(2, 2), Point(1, 1), Point(0, 0)
        ])
