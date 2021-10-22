import unittest
import rstr
import re
import random
from page.elements.point import Point, parse_points, points_to_string


class TestParsePoints(unittest.TestCase):
    def test_parse_left_inverse(self):
        for i in range(100):
            n = random.randrange(2, 100)
            points = []

            for j in range(n):
                x = random.randrange(-1000, 1000)
                y = random.randrange(-1000, 1000)
                points.append(Point(x, y))

            self.assertEqual(
                parse_points(points_to_string(points)),
                points
            )

    def test_parse_right_inverse(self):
        pattern = re.compile(
            r'([1-9][0-9]*,[1-9][0-9]* )+([1-9][0-9]*,[1-9][0-9]*)'
        )
        for i in range(100):
            random_str = rstr.xeger(pattern)
            self.assertEqual(
                points_to_string(parse_points(random_str)),
                random_str
            )
