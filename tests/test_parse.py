import unittest
from pprint import pprint as print

from Patche.model import Change, Diff, File, Header, Hunk, Line, Patch
from Patche.utils.parse import changes_to_hunks, parse_patch, parse_unified_diff


class ParseTest(unittest.TestCase):
    def setUp(self) -> None:
        self.lao = File("tests/cases/lao").line_list
        self.tzu = File("tests/cases/tzu").line_list
        self.abc = File("tests/cases/abc").line_list
        self.efg = File("tests/cases/efg").line_list

        with open("tests/cases/diff-unified.diff", "r") as f:
            self.diff_unified = f.read()

        with open("tests/cases/diff-unified2.diff", "r") as f:
            self.diff_unified_2 = f.read()

    def test_truth(self) -> None:
        self.assertEqual(type(self.lao), list)
        self.assertEqual(type(self.tzu), list)
        self.assertEqual(len(self.lao), 11)
        self.assertEqual(len(self.tzu), 13)

    def test_file(self) -> None:

        expected_lao_line_list = [
            Line(
                index=0, content="The Way that can be told of is not the eternal Way;"
            ),
            Line(
                index=1, content="The name that can be named is not the eternal name."
            ),
            Line(index=2, content="The Nameless is the origin of Heaven and Earth;"),
            Line(index=3, content="The Named is the mother of all things."),
            Line(index=4, content="Therefore let there always be non-being,"),
            Line(index=5, content="  so we may see their subtlety,"),
            Line(index=6, content="And let there always be being,"),
            Line(index=7, content="  so we may see their outcome."),
            Line(index=8, content="The two are the same,"),
            Line(index=9, content="But after they are produced,"),
            Line(index=10, content="  they have different names."),
        ]

        expected_tzu_line_list = [
            Line(index=0, content="The Nameless is the origin of Heaven and Earth;"),
            Line(index=1, content="The named is the mother of all things."),
            Line(index=2, content=""),
            Line(index=3, content="Therefore let there always be non-being,"),
            Line(index=4, content="  so we may see their subtlety,"),
            Line(index=5, content="And let there always be being,"),
            Line(index=6, content="  so we may see their outcome."),
            Line(index=7, content="The two are the same,"),
            Line(index=8, content="But after they are produced,"),
            Line(index=9, content="  they have different names."),
            Line(index=10, content="They both may be called deep and profound."),
            Line(index=11, content="Deeper and more profound,"),
            Line(index=12, content="The door of all subtleties!"),
        ]

        expected_abc_line_list = [
            Line(index=0, content="The Nameless is the origin of Heaven and Earth;"),
        ]

        expected_efg_line_list = [
            Line(index=0, content="The Nameless is the origin of Heaven and Earth;"),
            Line(index=1, content="The named is the mother of all things."),
        ]

        for current, expected in zip(self.lao, expected_lao_line_list):
            self.assertEqual(current.index, expected.index)
            self.assertEqual(current.content, expected.content)

        for current, expected in zip(self.tzu, expected_tzu_line_list):
            self.assertEqual(current.index, expected.index)
            self.assertEqual(current.content, expected.content)

        for current, expected in zip(self.abc, expected_abc_line_list):
            self.assertEqual(current.index, expected.index)
            self.assertEqual(current.content, expected.content)

        for current, expected in zip(self.efg, expected_efg_line_list):
            self.assertEqual(current.index, expected.index)
            self.assertEqual(current.content, expected.content)

    def test_parse_unified__diff(self) -> None:

        diff_unified_patch = parse_unified_diff(self.diff_unified)
        expected_diff_unified_patch = [
            Diff(
                header=Header(
                    index_path=None,
                    old_path="lao",
                    old_version="2013-01-05 16:56:19.000000000 -0600",
                    new_path="tzu",
                    new_version="2013-01-05 16:56:35.000000000 -0600",
                ),
                changes=[
                    Change(
                        old=1,
                        new=None,
                        line="The Way that can be told of is not the eternal Way;",
                        hunk=1,
                    ),
                    Change(
                        old=2,
                        new=None,
                        line="The name that can be named is not the eternal name.",
                        hunk=1,
                    ),
                    Change(
                        old=3,
                        new=1,
                        line="The Nameless is the origin of Heaven and Earth;",
                        hunk=1,
                    ),
                    Change(
                        old=4,
                        new=None,
                        line="The Named is the mother of all things.",
                        hunk=1,
                    ),
                    Change(
                        old=None,
                        new=2,
                        line="The named is the mother of all things.",
                        hunk=1,
                    ),
                    Change(old=None, new=3, line="", hunk=1),
                    Change(
                        old=5,
                        new=4,
                        line="Therefore let there always be non-being,",
                        hunk=1,
                    ),
                    Change(
                        old=6, new=5, line="  so we may see their subtlety,", hunk=1
                    ),
                    Change(old=7, new=6, line="And let there always be being,", hunk=1),
                    Change(old=9, new=8, line="The two are the same,", hunk=2),
                    Change(old=10, new=9, line="But after they are produced,", hunk=2),
                    Change(old=11, new=10, line="  they have different names.", hunk=2),
                    Change(
                        old=None,
                        new=11,
                        line="They both may be called deep and profound.",
                        hunk=2,
                    ),
                    Change(old=None, new=12, line="Deeper and more profound,", hunk=2),
                    Change(
                        old=None, new=13, line="The door of all subtleties!", hunk=2
                    ),
                ],
                text="",
                hunks=[
                    Hunk(
                        index=1,
                        context=[],
                        middle=[
                            Change(
                                old=1,
                                new=None,
                                line="The Way that can be told of is not the eternal Way;",
                                hunk=1,
                            ),
                            Change(
                                old=2,
                                new=None,
                                line="The name that can be named is not the eternal name.",
                                hunk=1,
                            ),
                            Change(
                                old=3,
                                new=1,
                                line="The Nameless is the origin of Heaven and Earth;",
                                hunk=1,
                            ),
                            Change(
                                old=4,
                                new=None,
                                line="The Named is the mother of all things.",
                                hunk=1,
                            ),
                            Change(
                                old=None,
                                new=2,
                                line="The named is the mother of all things.",
                                hunk=1,
                            ),
                            Change(old=None, new=3, line="", hunk=1),
                        ],
                        post=[
                            Change(
                                old=5,
                                new=4,
                                line="Therefore let there always be non-being,",
                                hunk=1,
                            ),
                            Change(
                                old=6,
                                new=5,
                                line="  so we may see their subtlety,",
                                hunk=1,
                            ),
                            Change(
                                old=7,
                                new=6,
                                line="And let there always be being,",
                                hunk=1,
                            ),
                        ],
                        all_=[
                            Change(
                                old=1,
                                new=None,
                                line="The Way that can be told of is not the eternal Way;",
                                hunk=1,
                            ),
                            Change(
                                old=2,
                                new=None,
                                line="The name that can be named is not the eternal name.",
                                hunk=1,
                            ),
                            Change(
                                old=3,
                                new=1,
                                line="The Nameless is the origin of Heaven and Earth;",
                                hunk=1,
                            ),
                            Change(
                                old=4,
                                new=None,
                                line="The Named is the mother of all things.",
                                hunk=1,
                            ),
                            Change(
                                old=None,
                                new=2,
                                line="The named is the mother of all things.",
                                hunk=1,
                            ),
                            Change(old=None, new=3, line="", hunk=1),
                            Change(
                                old=5,
                                new=4,
                                line="Therefore let there always be non-being,",
                                hunk=1,
                            ),
                            Change(
                                old=6,
                                new=5,
                                line="  so we may see their subtlety,",
                                hunk=1,
                            ),
                            Change(
                                old=7,
                                new=6,
                                line="And let there always be being,",
                                hunk=1,
                            ),
                        ],
                    ),
                    Hunk(
                        index=2,
                        context=[
                            Change(old=9, new=8, line="The two are the same,", hunk=2),
                            Change(
                                old=10,
                                new=9,
                                line="But after they are produced,",
                                hunk=2,
                            ),
                            Change(
                                old=11,
                                new=10,
                                line="  they have different names.",
                                hunk=2,
                            ),
                        ],
                        middle=[
                            Change(
                                old=None,
                                new=11,
                                line="They both may be called deep and profound.",
                                hunk=2,
                            ),
                            Change(
                                old=None,
                                new=12,
                                line="Deeper and more profound,",
                                hunk=2,
                            ),
                            Change(
                                old=None,
                                new=13,
                                line="The door of all subtleties!",
                                hunk=2,
                            ),
                        ],
                        post=[],
                        all_=[
                            Change(old=9, new=8, line="The two are the same,", hunk=2),
                            Change(
                                old=10,
                                new=9,
                                line="But after they are produced,",
                                hunk=2,
                            ),
                            Change(
                                old=11,
                                new=10,
                                line="  they have different names.",
                                hunk=2,
                            ),
                            Change(
                                old=None,
                                new=11,
                                line="They both may be called deep and profound.",
                                hunk=2,
                            ),
                            Change(
                                old=None,
                                new=12,
                                line="Deeper and more profound,",
                                hunk=2,
                            ),
                            Change(
                                old=None,
                                new=13,
                                line="The door of all subtleties!",
                                hunk=2,
                            ),
                        ],
                    ),
                ],
            ),
        ]
        for diff, diff_expected in zip(diff_unified_patch, expected_diff_unified_patch):
            assert isinstance(diff, Diff)

            assert diff.header == diff_expected.header
            assert diff.changes == diff_expected.changes
            # assert diff.text == diff_expected.text
            assert diff.hunks == diff_expected.hunks

        expected_diff_unified_patch_2 = [
            Diff(
                header=Header(
                    index_path=None,
                    old_path="abc",
                    old_version="2013-01-05 16:56:19.000000000 -0600",
                    new_path="efg",
                    new_version="2013-01-05 16:56:35.000000000 -0600",
                ),
                changes=[
                    Change(
                        old=1,
                        new=1,
                        line="The Nameless is the origin of Heaven and Earth;",
                        hunk=1,
                    ),
                    Change(
                        old=None,
                        new=2,
                        line="The named is the mother of all things.",
                        hunk=1,
                    ),
                ],
                text="",
                hunks=[
                    Hunk(
                        index=1,
                        context=[
                            Change(
                                old=1,
                                new=1,
                                line="The Nameless is the origin of Heaven and Earth;",
                                hunk=1,
                            )
                        ],
                        middle=[
                            Change(
                                old=None,
                                new=2,
                                line="The named is the mother of all things.",
                                hunk=1,
                            )
                        ],
                        post=[],
                        all_=[
                            Change(
                                old=1,
                                new=1,
                                line="The Nameless is the origin of Heaven and Earth;",
                                hunk=1,
                            ),
                            Change(
                                old=None,
                                new=2,
                                line="The named is the mother of all things.",
                                hunk=1,
                            ),
                        ],
                    )
                ],
            )
        ]
        diff_unified_2_patch = parse_unified_diff(self.diff_unified_2)
        for diff, diff_expected in zip(
            diff_unified_2_patch, expected_diff_unified_patch_2
        ):
            assert isinstance(diff, Diff)

            assert diff.header == diff_expected.header
            assert diff.changes == diff_expected.changes
            # assert diff.text == diff_expected.text
            assert diff.hunks == diff_expected.hunks

    def test_parse_email_patch(self) -> None:
        with open("tests/cases/904d88-email.patch", "r") as f:
            email_patch_text = f.read()

        email_patch = parse_patch(email_patch_text)
        expected_email_patch = Patch(
            sha="904d88d743b0c94092c5117955eab695df8109e8",
            author="Bjørn Mork <bjorn@mork.no>",
            date="Mon, 24 Jun 2019 18:45:11 +0200",
            subject="qmi_wwan: Fix out-of-bounds read",
            message='From 904d88d743b0c94092c5117955eab695df8109e8 Mon Sep 17 00:00:00 2001\nFrom: Bjørn Mork <bjorn@mork.no>\nDate: Mon, 24 Jun 2019 18:45:11 +0200\nSubject: qmi_wwan: Fix out-of-bounds read\nMIME-Version: 1.0\nContent-Type: text/plain; charset=UTF-8\nContent-Transfer-Encoding: 8bit\n\nThe syzbot reported\n\n Call Trace:\n  __dump_stack lib/dump_stack.c:77 [inline]\n  dump_stack+0xca/0x13e lib/dump_stack.c:113\n  print_address_description+0x67/0x231 mm/kasan/report.c:188\n  __kasan_report.cold+0x1a/0x32 mm/kasan/report.c:317\n  kasan_report+0xe/0x20 mm/kasan/common.c:614\n  qmi_wwan_probe+0x342/0x360 drivers/net/usb/qmi_wwan.c:1417\n  usb_probe_interface+0x305/0x7a0 drivers/usb/core/driver.c:361\n  really_probe+0x281/0x660 drivers/base/dd.c:509\n  driver_probe_device+0x104/0x210 drivers/base/dd.c:670\n  __device_attach_driver+0x1c2/0x220 drivers/base/dd.c:777\n  bus_for_each_drv+0x15c/0x1e0 drivers/base/bus.c:454\n\nCaused by too many confusing indirections and casts.\nid->driver_info is a pointer stored in a long.  We want the\npointer here, not the address of it.\n\nThanks-to: Hillf Danton <hdanton@sina.com>\nReported-by: syzbot+b68605d7fadd21510de1@syzkaller.appspotmail.com\nCc: Kristian Evensen <kristian.evensen@gmail.com>\nFixes: e4bf63482c30 ("qmi_wwan: Add quirk for Quectel dynamic config")\nSigned-off-by: Bjørn Mork <bjorn@mork.no>\nSigned-off-by: David S. Miller <davem@davemloft.net>',
            diff=[
                Diff(
                    header=Header(
                        index_path=None,
                        old_path="drivers/net/usb/qmi_wwan.c",
                        old_version="d080f8048e522d",
                        new_path="drivers/net/usb/qmi_wwan.c",
                        new_version="8b4ad10cf9402a",
                    ),
                    changes=[
                        Change(
                            old=1482,
                            new=1482,
                            line="\t * different. Ignore the current interface if the number of endpoints",
                            hunk=1,
                        ),
                        Change(
                            old=1483,
                            new=1483,
                            line="\t * equals the number for the diag interface (two).",
                            hunk=1,
                        ),
                        Change(old=1484, new=1484, line="\t */", hunk=1),
                        Change(
                            old=1485,
                            new=None,
                            line="\tinfo = (void *)&id->driver_info;",
                            hunk=1,
                        ),
                        Change(
                            old=None,
                            new=1485,
                            line="\tinfo = (void *)id->driver_info;",
                            hunk=1,
                        ),
                        Change(old=1486, new=1486, line="", hunk=1),
                        Change(
                            old=1487,
                            new=1487,
                            line="\tif (info->data & QMI_WWAN_QUIRK_QUECTEL_DYNCFG) {",
                            hunk=1,
                        ),
                        Change(
                            old=1488,
                            new=1488,
                            line="\t\tif (desc->bNumEndpoints == 2)",
                            hunk=1,
                        ),
                    ],
                    text="diff --git a/drivers/net/usb/qmi_wwan.c b/drivers/net/usb/qmi_wwan.c\nindex d080f8048e522d..8b4ad10cf9402a 100644\n--- a/drivers/net/usb/qmi_wwan.c\n+++ b/drivers/net/usb/qmi_wwan.c\n@@ -1482,7 +1482,7 @@ static int qmi_wwan_probe(struct usb_interface *intf,\n \t * different. Ignore the current interface if the number of endpoints\n \t * equals the number for the diag interface (two).\n \t */\n-\tinfo = (void *)&id->driver_info;\n+\tinfo = (void *)id->driver_info;\n \n \tif (info->data & QMI_WWAN_QUIRK_QUECTEL_DYNCFG) {\n \t\tif (desc->bNumEndpoints == 2)\n-- \ncgit 1.2.3-korg\n\n",
                    hunks=[
                        Hunk(
                            index=1,
                            context=[
                                Change(
                                    old=1482,
                                    new=1482,
                                    line="\t * different. Ignore the current interface if the number of endpoints",
                                    hunk=1,
                                ),
                                Change(
                                    old=1483,
                                    new=1483,
                                    line="\t * equals the number for the diag interface (two).",
                                    hunk=1,
                                ),
                                Change(old=1484, new=1484, line="\t */", hunk=1),
                            ],
                            middle=[
                                Change(
                                    old=1485,
                                    new=None,
                                    line="\tinfo = (void *)&id->driver_info;",
                                    hunk=1,
                                ),
                                Change(
                                    old=None,
                                    new=1485,
                                    line="\tinfo = (void *)id->driver_info;",
                                    hunk=1,
                                ),
                            ],
                            post=[
                                Change(old=1486, new=1486, line="", hunk=1),
                                Change(
                                    old=1487,
                                    new=1487,
                                    line="\tif (info->data & QMI_WWAN_QUIRK_QUECTEL_DYNCFG) {",
                                    hunk=1,
                                ),
                                Change(
                                    old=1488,
                                    new=1488,
                                    line="\t\tif (desc->bNumEndpoints == 2)",
                                    hunk=1,
                                ),
                            ],
                            all_=[
                                Change(
                                    old=1482,
                                    new=1482,
                                    line="\t * different. Ignore the current interface if the number of endpoints",
                                    hunk=1,
                                ),
                                Change(
                                    old=1483,
                                    new=1483,
                                    line="\t * equals the number for the diag interface (two).",
                                    hunk=1,
                                ),
                                Change(old=1484, new=1484, line="\t */", hunk=1),
                                Change(
                                    old=1485,
                                    new=None,
                                    line="\tinfo = (void *)&id->driver_info;",
                                    hunk=1,
                                ),
                                Change(
                                    old=None,
                                    new=1485,
                                    line="\tinfo = (void *)id->driver_info;",
                                    hunk=1,
                                ),
                                Change(old=1486, new=1486, line="", hunk=1),
                                Change(
                                    old=1487,
                                    new=1487,
                                    line="\tif (info->data & QMI_WWAN_QUIRK_QUECTEL_DYNCFG) {",
                                    hunk=1,
                                ),
                                Change(
                                    old=1488,
                                    new=1488,
                                    line="\t\tif (desc->bNumEndpoints == 2)",
                                    hunk=1,
                                ),
                            ],
                        )
                    ],
                )
            ],
        )
        assert expected_email_patch == email_patch

    def test_parse_git_patch(self) -> None:
        with open("tests/cases/904d88-git.patch", "r") as f:
            git_patch_text = f.read()

        git_patch = parse_patch(git_patch_text)
        expected_git_patch = Patch(
            sha="904d88d743b0c94092c5117955eab695df8109e8",
            author="Bjørn Mork <bjorn@mork.no>",
            date="Mon Jun 24 18:45:11 2019 +0200",
            subject="qmi_wwan: Fix out-of-bounds read",
            message='commit 904d88d743b0c94092c5117955eab695df8109e8\nAuthor: Bjørn Mork <bjorn@mork.no>\nDate:   Mon Jun 24 18:45:11 2019 +0200\n\n    qmi_wwan: Fix out-of-bounds read\n    \n    The syzbot reported\n    \n     Call Trace:\n      __dump_stack lib/dump_stack.c:77 [inline]\n      dump_stack+0xca/0x13e lib/dump_stack.c:113\n      print_address_description+0x67/0x231 mm/kasan/report.c:188\n      __kasan_report.cold+0x1a/0x32 mm/kasan/report.c:317\n      kasan_report+0xe/0x20 mm/kasan/common.c:614\n      qmi_wwan_probe+0x342/0x360 drivers/net/usb/qmi_wwan.c:1417\n      usb_probe_interface+0x305/0x7a0 drivers/usb/core/driver.c:361\n      really_probe+0x281/0x660 drivers/base/dd.c:509\n      driver_probe_device+0x104/0x210 drivers/base/dd.c:670\n      __device_attach_driver+0x1c2/0x220 drivers/base/dd.c:777\n      bus_for_each_drv+0x15c/0x1e0 drivers/base/bus.c:454\n    \n    Caused by too many confusing indirections and casts.\n    id->driver_info is a pointer stored in a long.  We want the\n    pointer here, not the address of it.\n    \n    Thanks-to: Hillf Danton <hdanton@sina.com>\n    Reported-by: syzbot+b68605d7fadd21510de1@syzkaller.appspotmail.com\n    Cc: Kristian Evensen <kristian.evensen@gmail.com>\n    Fixes: e4bf63482c30 ("qmi_wwan: Add quirk for Quectel dynamic config")\n    Signed-off-by: Bjørn Mork <bjorn@mork.no>\n    Signed-off-by: David S. Miller <davem@davemloft.net>\n',
            diff=[
                Diff(
                    header=Header(
                        index_path=None,
                        old_path="drivers/net/usb/qmi_wwan.c",
                        old_version="d080f8048e52",
                        new_path="drivers/net/usb/qmi_wwan.c",
                        new_version="8b4ad10cf940",
                    ),
                    changes=[
                        Change(
                            old=1482,
                            new=1482,
                            line="\t * different. Ignore the current interface if the number of endpoints",
                            hunk=1,
                        ),
                        Change(
                            old=1483,
                            new=1483,
                            line="\t * equals the number for the diag interface (two).",
                            hunk=1,
                        ),
                        Change(old=1484, new=1484, line="\t */", hunk=1),
                        Change(
                            old=1485,
                            new=None,
                            line="\tinfo = (void *)&id->driver_info;",
                            hunk=1,
                        ),
                        Change(
                            old=None,
                            new=1485,
                            line="\tinfo = (void *)id->driver_info;",
                            hunk=1,
                        ),
                        Change(old=1486, new=1486, line="", hunk=1),
                        Change(
                            old=1487,
                            new=1487,
                            line="\tif (info->data & QMI_WWAN_QUIRK_QUECTEL_DYNCFG) {",
                            hunk=1,
                        ),
                        Change(
                            old=1488,
                            new=1488,
                            line="\t\tif (desc->bNumEndpoints == 2)",
                            hunk=1,
                        ),
                    ],
                    text="diff --git a/drivers/net/usb/qmi_wwan.c b/drivers/net/usb/qmi_wwan.c\nindex d080f8048e52..8b4ad10cf940 100644\n--- a/drivers/net/usb/qmi_wwan.c\n+++ b/drivers/net/usb/qmi_wwan.c\n@@ -1482,7 +1482,7 @@ static int qmi_wwan_probe(struct usb_interface *intf,\n \t * different. Ignore the current interface if the number of endpoints\n \t * equals the number for the diag interface (two).\n \t */\n-\tinfo = (void *)&id->driver_info;\n+\tinfo = (void *)id->driver_info;\n \n \tif (info->data & QMI_WWAN_QUIRK_QUECTEL_DYNCFG) {\n \t\tif (desc->bNumEndpoints == 2)\n",
                    hunks=[
                        Hunk(
                            index=1,
                            context=[
                                Change(
                                    old=1482,
                                    new=1482,
                                    line="\t * different. Ignore the current interface if the number of endpoints",
                                    hunk=1,
                                ),
                                Change(
                                    old=1483,
                                    new=1483,
                                    line="\t * equals the number for the diag interface (two).",
                                    hunk=1,
                                ),
                                Change(old=1484, new=1484, line="\t */", hunk=1),
                            ],
                            middle=[
                                Change(
                                    old=1485,
                                    new=None,
                                    line="\tinfo = (void *)&id->driver_info;",
                                    hunk=1,
                                ),
                                Change(
                                    old=None,
                                    new=1485,
                                    line="\tinfo = (void *)id->driver_info;",
                                    hunk=1,
                                ),
                            ],
                            post=[
                                Change(old=1486, new=1486, line="", hunk=1),
                                Change(
                                    old=1487,
                                    new=1487,
                                    line="\tif (info->data & QMI_WWAN_QUIRK_QUECTEL_DYNCFG) {",
                                    hunk=1,
                                ),
                                Change(
                                    old=1488,
                                    new=1488,
                                    line="\t\tif (desc->bNumEndpoints == 2)",
                                    hunk=1,
                                ),
                            ],
                            all_=[
                                Change(
                                    old=1482,
                                    new=1482,
                                    line="\t * different. Ignore the current interface if the number of endpoints",
                                    hunk=1,
                                ),
                                Change(
                                    old=1483,
                                    new=1483,
                                    line="\t * equals the number for the diag interface (two).",
                                    hunk=1,
                                ),
                                Change(old=1484, new=1484, line="\t */", hunk=1),
                                Change(
                                    old=1485,
                                    new=None,
                                    line="\tinfo = (void *)&id->driver_info;",
                                    hunk=1,
                                ),
                                Change(
                                    old=None,
                                    new=1485,
                                    line="\tinfo = (void *)id->driver_info;",
                                    hunk=1,
                                ),
                                Change(old=1486, new=1486, line="", hunk=1),
                                Change(
                                    old=1487,
                                    new=1487,
                                    line="\tif (info->data & QMI_WWAN_QUIRK_QUECTEL_DYNCFG) {",
                                    hunk=1,
                                ),
                                Change(
                                    old=1488,
                                    new=1488,
                                    line="\t\tif (desc->bNumEndpoints == 2)",
                                    hunk=1,
                                ),
                            ],
                        )
                    ],
                )
            ],
        )

        assert expected_git_patch == git_patch

    def test_changes_to_hunks(self) -> None:

        # Test convert changes to hunk
        # use test/cases/923936.patch as input
        changes = [
            Change(
                old=79, new=79, line=" #define IOMAP_F_ATOMIC_BIO\t(1U << 8)", hunk=1
            ),
            Change(old=80, new=80, line=" ", hunk=1),
            Change(old=81, new=81, line=" /*", hunk=1),
            Change(
                old=None,
                new=82,
                line="  * Flag reserved for file system specific usage",
                hunk=1,
            ),
            Change(old=None, new=83, line="  */", hunk=1),
            Change(
                old=None, new=84, line=" #define IOMAP_F_PRIVATE\t\t(1U << 12)", hunk=1
            ),
            Change(old=None, new=85, line=" ", hunk=1),
            Change(old=None, new=86, line=" /*", hunk=1),
            Change(
                old=82,
                new=87,
                line="  * Flags set by the core iomap code during operations:",
                hunk=1,
            ),
            Change(old=83, new=88, line="  *", hunk=1),
            Change(
                old=84,
                new=89,
                line="  * IOMAP_F_SIZE_CHANGED indicates to the iomap_end method that the file size",
                hunk=1,
            ),
            Change(
                old=88,
                new=93,
                line="  * range it covers needs to be remapped by the high level before the operation",
                hunk=2,
            ),
            Change(old=89, new=94, line="  * can proceed.", hunk=2),
            Change(old=90, new=95, line="  */", hunk=2),
            Change(
                old=91,
                new=None,
                line=" #define IOMAP_F_SIZE_CHANGED\t(1U << 8)",
                hunk=2,
            ),
            Change(
                old=92, new=None, line=" #define IOMAP_F_STALE\t\t(1U << 9)", hunk=2
            ),
            Change(old=93, new=None, line=" ", hunk=2),
            Change(old=94, new=None, line=" /*", hunk=2),
            Change(
                old=95,
                new=None,
                line="  * Flags from 0x1000 up are for file system specific usage:",
                hunk=2,
            ),
            Change(old=96, new=None, line="  */", hunk=2),
            Change(
                old=97, new=None, line=" #define IOMAP_F_PRIVATE\t\t(1U << 12)", hunk=2
            ),
            Change(old=98, new=None, line=" ", hunk=2),
            Change(
                old=None,
                new=96,
                line=" #define IOMAP_F_SIZE_CHANGED\t(1U << 14)",
                hunk=2,
            ),
            Change(
                old=None, new=97, line=" #define IOMAP_F_STALE\t\t(1U << 15)", hunk=2
            ),
            Change(old=99, new=98, line=" ", hunk=2),
            Change(old=100, new=99, line=" /*", hunk=2),
            Change(old=101, new=100, line="  * Magic value for addr:", hunk=2),
        ]

        expected_hunks = [
            Hunk(
                index=1,
                context=[
                    Change(
                        old=79,
                        new=79,
                        line=" #define IOMAP_F_ATOMIC_BIO\t(1U << 8)",
                        hunk=1,
                    ),
                    Change(old=80, new=80, line=" ", hunk=1),
                    Change(old=81, new=81, line=" /*", hunk=1),
                ],
                middle=[
                    Change(
                        old=None,
                        new=82,
                        line="  * Flag reserved for file system specific usage",
                        hunk=1,
                    ),
                    Change(old=None, new=83, line="  */", hunk=1),
                    Change(
                        old=None,
                        new=84,
                        line=" #define IOMAP_F_PRIVATE\t\t(1U << 12)",
                        hunk=1,
                    ),
                    Change(old=None, new=85, line=" ", hunk=1),
                    Change(old=None, new=86, line=" /*", hunk=1),
                ],
                post=[
                    Change(
                        old=82,
                        new=87,
                        line="  * Flags set by the core iomap code during operations:",
                        hunk=1,
                    ),
                    Change(old=83, new=88, line="  *", hunk=1),
                    Change(
                        old=84,
                        new=89,
                        line="  * IOMAP_F_SIZE_CHANGED indicates to the iomap_end method that the file size",
                        hunk=1,
                    ),
                ],
                all_=[
                    Change(
                        old=79,
                        new=79,
                        line=" #define IOMAP_F_ATOMIC_BIO\t(1U << 8)",
                        hunk=1,
                    ),
                    Change(old=80, new=80, line=" ", hunk=1),
                    Change(old=81, new=81, line=" /*", hunk=1),
                    Change(
                        old=None,
                        new=82,
                        line="  * Flag reserved for file system specific usage",
                        hunk=1,
                    ),
                    Change(old=None, new=83, line="  */", hunk=1),
                    Change(
                        old=None,
                        new=84,
                        line=" #define IOMAP_F_PRIVATE\t\t(1U << 12)",
                        hunk=1,
                    ),
                    Change(old=None, new=85, line=" ", hunk=1),
                    Change(old=None, new=86, line=" /*", hunk=1),
                    Change(
                        old=82,
                        new=87,
                        line="  * Flags set by the core iomap code during operations:",
                        hunk=1,
                    ),
                    Change(old=83, new=88, line="  *", hunk=1),
                    Change(
                        old=84,
                        new=89,
                        line="  * IOMAP_F_SIZE_CHANGED indicates to the iomap_end method that the file size",
                        hunk=1,
                    ),
                ],
            ),
            Hunk(
                index=2,
                context=[
                    Change(
                        old=88,
                        new=93,
                        line="  * range it covers needs to be remapped by the high level before the operation",
                        hunk=2,
                    ),
                    Change(old=89, new=94, line="  * can proceed.", hunk=2),
                    Change(old=90, new=95, line="  */", hunk=2),
                ],
                middle=[
                    Change(
                        old=91,
                        new=None,
                        line=" #define IOMAP_F_SIZE_CHANGED\t(1U << 8)",
                        hunk=2,
                    ),
                    Change(
                        old=92,
                        new=None,
                        line=" #define IOMAP_F_STALE\t\t(1U << 9)",
                        hunk=2,
                    ),
                    Change(old=93, new=None, line=" ", hunk=2),
                    Change(old=94, new=None, line=" /*", hunk=2),
                    Change(
                        old=95,
                        new=None,
                        line="  * Flags from 0x1000 up are for file system specific usage:",
                        hunk=2,
                    ),
                    Change(old=96, new=None, line="  */", hunk=2),
                    Change(
                        old=97,
                        new=None,
                        line=" #define IOMAP_F_PRIVATE\t\t(1U << 12)",
                        hunk=2,
                    ),
                    Change(old=98, new=None, line=" ", hunk=2),
                    Change(
                        old=None,
                        new=96,
                        line=" #define IOMAP_F_SIZE_CHANGED\t(1U << 14)",
                        hunk=2,
                    ),
                    Change(
                        old=None,
                        new=97,
                        line=" #define IOMAP_F_STALE\t\t(1U << 15)",
                        hunk=2,
                    ),
                ],
                post=[
                    Change(old=99, new=98, line=" ", hunk=2),
                    Change(old=100, new=99, line=" /*", hunk=2),
                    Change(old=101, new=100, line="  * Magic value for addr:", hunk=2),
                ],
                all_=[
                    Change(
                        old=88,
                        new=93,
                        line="  * range it covers needs to be remapped by the high level before the operation",
                        hunk=2,
                    ),
                    Change(old=89, new=94, line="  * can proceed.", hunk=2),
                    Change(old=90, new=95, line="  */", hunk=2),
                    Change(
                        old=91,
                        new=None,
                        line=" #define IOMAP_F_SIZE_CHANGED\t(1U << 8)",
                        hunk=2,
                    ),
                    Change(
                        old=92,
                        new=None,
                        line=" #define IOMAP_F_STALE\t\t(1U << 9)",
                        hunk=2,
                    ),
                    Change(old=93, new=None, line=" ", hunk=2),
                    Change(old=94, new=None, line=" /*", hunk=2),
                    Change(
                        old=95,
                        new=None,
                        line="  * Flags from 0x1000 up are for file system specific usage:",
                        hunk=2,
                    ),
                    Change(old=96, new=None, line="  */", hunk=2),
                    Change(
                        old=97,
                        new=None,
                        line=" #define IOMAP_F_PRIVATE\t\t(1U << 12)",
                        hunk=2,
                    ),
                    Change(old=98, new=None, line=" ", hunk=2),
                    Change(
                        old=None,
                        new=96,
                        line=" #define IOMAP_F_SIZE_CHANGED\t(1U << 14)",
                        hunk=2,
                    ),
                    Change(
                        old=None,
                        new=97,
                        line=" #define IOMAP_F_STALE\t\t(1U << 15)",
                        hunk=2,
                    ),
                    Change(old=99, new=98, line=" ", hunk=2),
                    Change(old=100, new=99, line=" /*", hunk=2),
                    Change(old=101, new=100, line="  * Magic value for addr:", hunk=2),
                ],
            ),
        ]

        assert changes_to_hunks(changes) == expected_hunks
