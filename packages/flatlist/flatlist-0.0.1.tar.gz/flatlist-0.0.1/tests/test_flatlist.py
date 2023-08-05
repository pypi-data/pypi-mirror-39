import unittest
from flatlist import flatten_list


class Testflatlist(unittest.TestCase):
    def test_no_nested(self):
        inp = [1, 2, 3, 4, 5]
        self.assertListEqual(
            flatten_list(inp),
            inp,
        )

    def test_empty(self):
        self.assertListEqual(
            flatten_list([]),
            []
        )

    def test_nested_empty(self):
        inp = [[[], [], [[], []]]]
        self.assertListEqual(
            flatten_list(inp),
            []
        )

    def test_multilevel(self):
        inp = [1, [2, 3], 4]
        self.assertListEqual(
            flatten_list(inp),
            [1, 2, 3, 4]
        )

    def test_5depth(self):
        inp = [1, [2, [3, [4, [5]]]]]
        self.assertListEqual(
            flatten_list(inp),
            [1, 2, 3, 4, 5]
        )

    def test_different_nested_various_types(self):
        inp = [1, 2, ['pupa', 3.14], b'hey', ['ho', {'nope?': 'nope.'}]]
        self.assertListEqual(
            flatten_list(inp),
            [1, 2, 'pupa', 3.14, b'hey', 'ho', {'nope?': 'nope.'}]
        )
