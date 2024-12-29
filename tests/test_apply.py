import unittest

from Patche.model import File, Line
from Patche.utils.parse import parse_patch
from Patche.utils.resolve import apply_change


def _apply(text: list[Line], diff: str) -> list[Line]:
    patch = parse_patch(diff)

    return apply_change(patch.diff[0].hunks, text).new_line_list


def _apply_r(text: list[Line], diff: str) -> list[Line]:
    patch = parse_patch(diff)

    return apply_change(patch.diff[0].hunks, text, reverse=True).new_line_list


def list_line_to_str(line_list: list[Line]) -> list[str]:
    return [line.content for line in line_list]


class ApplyTest(unittest.TestCase):

    def setUp(self) -> None:
        self.lao = File("tests/cases/lao").line_list
        self.tzu = File("tests/cases/tzu").line_list
        self.abc = File("tests/cases/abc").line_list
        self.efg = File("tests/cases/efg").line_list

        # with open("tests/cases/tzu") as f:
        #     self.tzu = f.read().splitlines()

        # with open("tests/cases/abc") as f:
        #     self.abc = f.read().splitlines()

        # with open("tests/cases/efg") as f:
        #     self.efg = f.read().splitlines()

    def test_truth(self) -> None:
        self.assertEqual(type(self.lao), list)
        self.assertEqual(type(self.tzu), list)
        self.assertEqual(len(self.lao), 11)
        self.assertEqual(len(self.tzu), 13)

    # def test_diff_unified(self) -> None:
    #     with open("tests/cases/diff-unified.diff") as f:
    #         diff_text = f.read()

    #     self.assertEqual(list_line_to_str(_apply(self.lao, diff_text)), list_line_to_str(self.tzu))
    #     self.assertEqual(list_line_to_str(_apply_r(self.tzu, diff_text)), list_line_to_str(self.lao))

    def test_diff_unified2(self) -> None:
        with open("tests/cases/diff-unified2.diff") as f:
            diff_text = f.read()

        self.assertEqual(
            list_line_to_str(_apply(self.abc, diff_text)), list_line_to_str(self.efg)
        )
        self.assertEqual(
            list_line_to_str(_apply_r(self.efg, diff_text)), list_line_to_str(self.abc)
        )
