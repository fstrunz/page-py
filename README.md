# page-py
Python library for dealing with PageXML files.

## Example

```python3
from typing import List
from page.elements import PcGts, Page, Region, Text

# Currently, only pagecontent files are supported via PcGts.
pcgts = PcGts.from_file("example.gt.xml")
page: Page = pcgts.page
regions: List[Region] = page.regions

# Accumulate the TextEquiv tags of all TextLines in the document.
texts: List[Text] = [
    line.text for region in regions for line in region.lines
]

# Print all of their unicode representations.
for text in texts:
    print(text.unicode)
```