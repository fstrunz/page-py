import unittest
from lxml import etree


def assert_same_descendant_tags(
    test_case: unittest.TestCase,
    a: etree.ElementBase, b: etree.ElementBase
):
    a_descendants = {x.tag for x in a.iterdescendants()}
    b_descendants = {y.tag for y in b.iterdescendants()}
    test_case.assertEqual(a_descendants, b_descendants)
