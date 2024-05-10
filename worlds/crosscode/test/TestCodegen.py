from copy import copy, deepcopy
import os

from test.TestBase import TestBase

from . import CrossCodeTestBase
from ..codegen.util import get_json_object
from ..codegen.merge import merge

class TestMergeBasic(TestBase):
    auto_construct = False
    list1 = list(range(1, 5))
    list2 = list(range(5, 9))
    list3 = list(range(1, 9))

    dict1 = { f"key{idx}": f"value{idx}" for idx in range(1, 5) }
    dict2 = { f"key{idx}": f"value{idx}" for idx in range(5, 9) }
    dict3 = { f"key{idx}": f"value{idx}" for idx in range(1, 9) }

    def test_merge_list(self):
        original = copy(self.list1)
        addon = self.list2
        result = self.list3

        merge(original, addon)
        self.assertEqual(original, result)

    def test_merge_dict(self):
        original = copy(self.dict1)
        addon = self.dict2
        result = self.dict3

        merge(original, addon)
        self.assertEqual(original, result)

    def test_merge_dict_with_non_dict(self):
        original = copy(self.dict1)
        
        self.assertRaises(RuntimeError, merge, original, self.list2)
        self.assertRaises(RuntimeError, merge, original, "addon")
        self.assertRaises(RuntimeError, merge, original, 2)

    def test_merge_list_with_non_list(self):
        original = copy(self.list1)
        
        self.assertRaises(RuntimeError, merge, original, self.dict2)
        self.assertRaises(RuntimeError, merge, original, "addon")
        self.assertRaises(RuntimeError, merge, original, 2)

class TestMergeComplex(TestBase):
    auto_construct = False
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    original = get_json_object(os.path.join(data_dir, "original.json"))

    def test_addon_merge(self):
        original = deepcopy(self.original)
        addon = get_json_object(os.path.join(self.data_dir, "merge-mode.json"))
        result = get_json_object(os.path.join(self.data_dir, "merge-mode-result.json"))

        original = merge(original, addon)
        self.assertEqual(original, result)

    def test_addon_replace(self):
        original = deepcopy(self.original)
        addon = get_json_object(os.path.join(self.data_dir, "replace.json"))
        result = get_json_object(os.path.join(self.data_dir, "replace-result.json"))

        merge(original, addon)
        self.assertEqual(original, result)

    def test_addon_find(self):
        original = deepcopy(self.original)
        addon = get_json_object(os.path.join(self.data_dir, "find.json"))
        result = get_json_object(os.path.join(self.data_dir, "find-result.json"))

        merge(original, addon)
        self.assertEqual(original, result)
