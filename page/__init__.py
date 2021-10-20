from typing import Dict
from page.elements import Region

class Page:
    def __init__(self, regions: Dict[str, Region]):
        self.regions = regions