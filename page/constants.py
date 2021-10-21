from typing import Dict, Optional

NsMap = Dict[Optional[str], str]
DEFAULT_XML_NAMESPACE = (
    "http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15"
)
DEFAULT_NAMESPACE_MAP: NsMap = {None: DEFAULT_XML_NAMESPACE}
