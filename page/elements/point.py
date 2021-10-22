from typing import List
from page.exceptions import PageXMLError


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


def parse_points(points_str: str) -> List[Point]:
    # PAGE XML spec defines the point string using the regular expression
    # ([0-9]+,[0.9]+ )+([0-9]+,[0-9]+)

    points: List[Point] = []

    for point_str in points_str.split(" "):
        coords = point_str.split(",")

        if len(coords) != 2:
            raise PageXMLError(
                f"point '{point_str}' must contain exactly 2 coordinates"
            )

        try:
            x, y = int(coords[0]), int(coords[1])
        except ValueError:
            raise PageXMLError(f"invalid coordinates in point '{point_str}'")

        points.append(Point(x, y))

    if len(points) < 2:
        raise PageXMLError(
            f"points string {points_str} must contain at least 2 coordinates"
        )

    return points
