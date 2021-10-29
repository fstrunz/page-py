import unittest
import rstr
import re
import random
from page.elements import Point, parse_points, points_to_string
from page.exceptions import PageXMLError


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

    def test_parse_too_short(self):
        for i in range(100):
            x = random.randrange(-1000, 1000)
            y = random.randrange(-1000, 1000)
            points_str = f"{int(x)},{int(y)}"
            self.assertRaises(PageXMLError, lambda: parse_points(points_str))

    def test_parse_coord_too_long(self):
        for i in range(100):
            x1 = random.randrange(-1000, 1000)
            y1 = random.randrange(-1000, 1000)
            z1 = random.randrange(-1000, 1000)

            x2 = random.randrange(-1000, 1000)
            y2 = random.randrange(-1000, 1000)
            z2 = random.randrange(-1000, 1000)

            points_str = (
                f"{int(x1)},{int(y1)},{int(z1)} {int(x2)},{int(y2)},{int(z2)}"
            )

            self.assertRaises(PageXMLError, lambda: parse_points(points_str))

    def test_parse_coord_too_short(self):
        for i in range(100):
            n = random.randrange(2, 100)
            points_str = ' '.join(
                str(random.randrange(-1000, 1000)) for _ in range(n)
            )
            self.assertRaises(PageXMLError, lambda: parse_points(points_str))

    def test_point_order_refl_antisymm(self):
        for i in range(100):
            x = random.randrange(-1000, 1000)
            y = random.randrange(-1000, 1000)

            p = Point(x, y)

            # Reflexivity (a <= a for all a)
            self.assertLessEqual(p, p)
            # Antisymmetry (a <= b and a >= b -> a = b for all a, b)
            self.assertEqual(p, p)
