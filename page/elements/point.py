from typing import List
from dataclasses import dataclass
from page.exceptions import PageXMLError


@dataclass(repr=False, order=True)
class Point:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return self.__str__()


def parse_points(points_str: str) -> List[Point]:
    # PAGE XML spec defines the point string using the regular expression
    # ([0-9]+,[0-9]+ )+([0-9]+,[0-9]+)

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


def points_to_string(points: List[Point]) -> str:
    return ' '.join([f'{p.x},{p.y}' for p in points])
