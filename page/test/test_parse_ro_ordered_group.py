import unittest
from lxml import etree

from page.elements import RegionRefIndexed
from page.elements.reading_order import (
    OrderedGroup, OrderedGroupIndexed, UnorderedGroupIndexed
)
from page.elements.region_ref import RegionRef
import page.test.assert_utils as utils

SIMPLE_ORDERED_GROUP = etree.XML(
    """<OrderedGroup id="ro1" caption="Region reading order">
        <RegionRefIndexed index="0" regionRef="r0" />
        <RegionRefIndexed index="1" regionRef="r1" />
        <RegionRefIndexed index="2" regionRef="r2" />
        <RegionRefIndexed index="3" regionRef="r3" />
    </OrderedGroup>"""
)

NESTED_ORDERED_GROUPS = etree.XML(
    """<OrderedGroup id="ro2" caption="Region reading order with subgroup">
        <RegionRefIndexed index="0" regionRef="r0" />
        <OrderedGroupIndexed id="ro2_1" index="1">
            <RegionRefIndexed index="0" regionRef="r1" />
            <RegionRefIndexed index="1" regionRef="r2" />
        </OrderedGroupIndexed>
        <RegionRefIndexed index="2" regionRef="r3" />
    </OrderedGroup>"""
)

NESTED_MIXED_GROUPS = etree.XML(
    """<OrderedGroup id="ro3" caption="Mixed group types">
        <RegionRefIndexed index="0" regionRef="r0" />
        <UnorderedGroupIndexed id="ro3_1" index="1">
            <RegionRef regionRef="r1" />
            <RegionRef regionRef="r2" />
            <RegionRef regionRef="r3" />
        </UnorderedGroupIndexed>
        <RegionRefIndexed index="2" regionRef="r4" />
        <OrderedGroupIndexed id="ro3_2" index="3">
            <RegionRefIndexed index="0" regionRef="r5" />
            <RegionRefIndexed index="1" regionRef="r6" />
        </OrderedGroupIndexed>
    </OrderedGroup>"""
)


class TestParseOrderedGroup(unittest.TestCase):
    def test_parse_simple_ordered_group(self):
        group = OrderedGroup.from_element(SIMPLE_ORDERED_GROUP, {})
        self.assertEqual(group.group_id, "ro1")
        self.assertEqual(group.caption, "Region reading order")
        self.assertEqual(len(group.children), 4)

        self.assertEqual(group.get_from_index(0), RegionRefIndexed("r0", 0))
        self.assertEqual(group.get_from_index(1), RegionRefIndexed("r1", 1))
        self.assertEqual(group.get_from_index(2), RegionRefIndexed("r2", 2))
        self.assertEqual(group.get_from_index(3), RegionRefIndexed("r3", 3))

    def test_parse_nested_ordered_groups(self):
        group = OrderedGroup.from_element(NESTED_ORDERED_GROUPS, {})
        self.assertEqual(group.group_id, "ro2")
        self.assertEqual(group.caption, "Region reading order with subgroup")
        self.assertEqual(
            list(group.region_refs()),
            [RegionRefIndexed("r0", 0), RegionRefIndexed("r3", 2)]
        )

        subgroups = list(group.subgroups())
        self.assertEqual(len(subgroups), 1)

        subgroup = subgroups[0]
        self.assertEqual(subgroup.group_id, "ro2_1")
        self.assertEqual(subgroup.index, 1)

        self.assertEqual(
            list(subgroup.region_refs()),
            [RegionRefIndexed("r1", 0), RegionRefIndexed("r2", 1)]
        )

    def test_parse_nested_mixed_groups(self):
        group = OrderedGroup.from_element(NESTED_MIXED_GROUPS, {})
        self.assertEqual(group.group_id, "ro3")
        self.assertEqual(group.caption, "Mixed group types")
        self.assertEqual(group.get_from_index(0), RegionRefIndexed("r0", 0))

        ro3_1 = group.get_from_index(1)
        self.assertIsInstance(ro3_1, UnorderedGroupIndexed)
        self.assertEqual(ro3_1.group_id, "ro3_1")
        self.assertEqual(ro3_1.index, 1)
        self.assertEqual(len(ro3_1.children), 3)
        self.assertEqual(ro3_1.children, [
            RegionRef("r1"), RegionRef("r2"), RegionRef("r3")
        ])

        self.assertEqual(group.get_from_index(2), RegionRefIndexed("r4", 2))

        ro3_2 = group.get_from_index(3)
        self.assertIsInstance(ro3_2, OrderedGroupIndexed)
        self.assertEqual(ro3_2.group_id, "ro3_2")
        self.assertEqual(ro3_2.index, 3)
        self.assertEqual(len(ro3_2.children), 2)
        self.assertEqual(ro3_2.children, [
            RegionRefIndexed("r5", 0),
            RegionRefIndexed("r6", 1)
        ])

    def test_parse_ordered_group_invert(self):
        for test_xml in [
            SIMPLE_ORDERED_GROUP,
            NESTED_ORDERED_GROUPS,
            NESTED_MIXED_GROUPS
        ]:
            utils.assert_same_descendant_tags(
                self,
                OrderedGroup.from_element(test_xml, {}).to_element({}),
                test_xml
            )
