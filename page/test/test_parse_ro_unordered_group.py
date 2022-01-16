import unittest
from lxml import etree

from page.elements.reading_order import UnorderedGroup
from page.elements.region_ref import RegionRef
import page.test.assert_utils as utils

SIMPLE_UNORDERED_GROUP = etree.XML(
    """<UnorderedGroup id="uog1" caption="Unordered group 1">
        <RegionRef regionRef="r0" />
        <RegionRef regionRef="r1" />
        <RegionRef regionRef="r2" />
        <RegionRef regionRef="r3" />
    </UnorderedGroup>"""
)

NESTED_UNORDERED_GROUPS = etree.XML(
    """<UnorderedGroup id="uog2" caption="Unordered group 2">
        <RegionRef regionRef="r0" />
        <UnorderedGroup id="uog2_1" caption="Unordered group 2 subgroup">
            <RegionRef regionRef="r1" />
            <RegionRef regionRef="r2" />
        </UnorderedGroup>
        <RegionRef regionRef="r3" />
    </UnorderedGroup>"""
)


class TestParseUnorderedGroup(unittest.TestCase):
    def test_parse_simple_unordered_group(self):
        group = UnorderedGroup.from_element(SIMPLE_UNORDERED_GROUP, {})
        self.assertEqual(group.group_id, "uog1")
        self.assertEqual(group.caption, "Unordered group 1")
        self.assertEqual(len(group.children), 4)
        self.assertEqual(group.children, [
            RegionRef("r0"), RegionRef("r1"), RegionRef("r2"), RegionRef("r3")
        ])

    def test_parse_nested_unordered_groups(self):
        group = UnorderedGroup.from_element(NESTED_UNORDERED_GROUPS, {})
        self.assertEqual(group.group_id, "uog2")
        self.assertEqual(group.caption, "Unordered group 2")
        self.assertEqual(group.children, [
            UnorderedGroup("uog2_1", [
                RegionRef("r1"), RegionRef("r2")
            ], "Unordered group 2 subgroup"),
            RegionRef("r0"),
            RegionRef("r3")
        ])

    def test_parse_unordered_group_invert(self):
        for test_xml in [
            SIMPLE_UNORDERED_GROUP,
            NESTED_UNORDERED_GROUPS
        ]:
            utils.assert_same_descendant_tags(
                self,
                UnorderedGroup.from_element(test_xml, {}).to_element({}),
                test_xml
            )
