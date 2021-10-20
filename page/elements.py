from typing import List, Optional, Dict

class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

# TODO: Words, Glyphs

class Line:
    def __init__(self, coords: List[Point], texts: Dict[int, str]):
        self.coords = coords
        self.texts = texts

class Region:
    def __init__(self, coords: List[Point]):
        self.coords = coords

class TextRegion(Region):
    def __init__(self, lines: List[Line]):
        self.lines = lines