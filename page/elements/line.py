from typing import List, Dict
from page.elements import Point


class Line:
    def __init__(self, coords: List[Point], texts: Dict[int, str]):
        self.coords = coords
        self.texts = texts
