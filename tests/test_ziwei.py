"""紫微斗数桥接测试：依赖 Node + vendor/iztro，缺失时自动跳过（不阻塞 CI）。"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import unittest
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import ziwei  # noqa: E402

HAS_NODE = shutil.which("node") is not None and (ROOT / "vendor" / "iztro" / "node_modules" / "iztro").is_dir()


def run_cli(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-X", "utf8", *args],
        capture_output=True, text=True, encoding="utf-8", cwd=str(ROOT),
    )


class TimeIndexTest(unittest.TestCase):
    def test_time_index_mapping(self):
        self.assertEqual(ziwei.time_index(datetime(2020, 1, 1, 0, 30)), 0)   # 早子
        self.assertEqual(ziwei.time_index(datetime(2020, 1, 1, 1, 0)), 1)    # 丑
        self.assertEqual(ziwei.time_index(datetime(2020, 1, 1, 7, 30)), 4)   # 辰
        self.assertEqual(ziwei.time_index(datetime(2020, 1, 1, 14, 30)), 7)  # 未
        self.assertEqual(ziwei.time_index(datetime(2020, 1, 1, 23, 30)), 12) # 晚子


@unittest.skipUnless(HAS_NODE, "需要 Node.js 18+ 与 vendor/iztro")
class ZiweiChartTest(unittest.TestCase):
    def test_chart_contract(self):
        data = ziwei.chart(datetime(1995, 8, 17, 14, 30), "male", 120.155)
        self.assertEqual(data["schema"], "suanming.ziwei.v1")
        self.assertEqual(len(data["palaces"]), 12)
        names = {p["name"] for p in data["palaces"]}
        self.assertIn("命宫", names)
        self.assertTrue(data["astrolabe"]["five_elements_class"].endswith("局"))
        self.assertEqual(data["astrolabe"]["zodiac"], "猪")
        self.assertEqual(data["time_correction"]["shichen"], "未")
        self.assertIn("disclaimer", data)
        self.assertIn("engine", data)

    def test_palaces_have_stars(self):
        data = ziwei.chart(datetime(1995, 8, 17, 14, 30), "male", 120.155)
        total = sum(len(p["major_stars"]) for p in data["palaces"])
        self.assertEqual(total, 14, "十四主星应各出现一次")
        for p in data["palaces"]:
            self.assertIn("decadal", p)

    def test_late_zi_warning(self):
        data = ziwei.chart(datetime(1995, 8, 17, 23, 30), "male", 120.155)
        self.assertTrue(any("晚子时" in w for w in data["warnings"]))
        self.assertEqual(data["time_correction"]["time_index"], 0)  # next_day 转早子

    def test_dst_warning(self):
        data = ziwei.chart(datetime(1990, 6, 15, 9, 10), "male", 121.474)
        self.assertTrue(any("夏令时" in w for w in data["warnings"]))

    def test_cli_brief(self):
        r = run_cli([str(ROOT / "scripts" / "ziwei.py"), "--birth", "1995-08-17 14:30",
                     "--gender", "male", "--city", "杭州", "--year", "2026", "--format", "brief"])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("紫微盘", r.stdout)
        self.assertIn("命宫", r.stdout)

    def test_cli_json(self):
        r = run_cli([str(ROOT / "scripts" / "ziwei.py"), "--birth", "1996-03-08 09:15",
                     "--gender", "female", "--city", "北京"])
        self.assertEqual(r.returncode, 0, r.stderr)
        data = json.loads(r.stdout)
        self.assertEqual(len(data["palaces"]), 12)


class ZiweiArgTest(unittest.TestCase):
    def test_bad_birth(self):
        r = run_cli([str(ROOT / "scripts" / "ziwei.py"), "--birth", "1995/13/40",
                     "--gender", "male", "--city", "杭州"])
        self.assertEqual(r.returncode, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
