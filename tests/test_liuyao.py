"""六爻规则表校验：八宫卦序、64 卦唯一、纳甲、世应、六亲、六神、变卦。

六爻是纯规则表实现的，表错一处整盘就错；这些测试把公开的传统规则逐条锁住。
参考：京房八宫卦序、《卜筮正宗》纳甲世应、《增删卜易》月建日辰旬空（均为公有领域规则）。
"""

from __future__ import annotations

import sys
import unittest
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import liuyao  # noqa: E402

KNOWN_PALACES = {
    "乾": ["乾为天", "天风姤", "天山遁", "天地否", "风地观", "山地剥", "火地晋", "火天大有"],
    "坎": ["坎为水", "水泽节", "水雷屯", "水火既济", "泽火革", "雷火丰", "地火明夷", "地水师"],
    "艮": ["艮为山", "山火贲", "山天大畜", "山泽损", "火泽睽", "天泽履", "风泽中孚", "风山渐"],
    "震": ["震为雷", "雷地豫", "雷水解", "雷风恒", "地风升", "水风井", "泽风大过", "泽雷随"],
    "巽": ["巽为风", "风天小畜", "风火家人", "风雷益", "天雷无妄", "火雷噬嗑", "山雷颐", "山风蛊"],
    "离": ["离为火", "火山旅", "火风鼎", "火水未济", "山水蒙", "风水涣", "天水讼", "天火同人"],
    "坤": ["坤为地", "地雷复", "地泽临", "地天泰", "雷天大壮", "泽天夬", "水天需", "水地比"],
    "兑": ["兑为泽", "泽水困", "泽地萃", "泽山咸", "水山蹇", "地山谦", "雷山小过", "雷泽归妹"],
}


class TableTest(unittest.TestCase):
    def test_64_hexagrams_unique(self):
        names = list(liuyao.HEXAGRAM_NAMES.values())
        self.assertEqual(len(liuyao.HEXAGRAM_NAMES), 64)
        self.assertEqual(len(set(names)), 64, "64 卦名有重复")

    def test_every_trigram_pair_covered(self):
        for upper in liuyao.TRIGRAMS:
            for lower in liuyao.TRIGRAMS:
                self.assertIn((upper, lower), liuyao.HEXAGRAM_NAMES)

    def test_eight_palaces_sequences(self):
        for palace, expected in KNOWN_PALACES.items():
            got = [liuyao.hexagram_name(u, l) for u, l in liuyao.palace_sequence(palace)]
            self.assertEqual(got, expected, f"{palace}宫卦序不符")

    def test_shi_ying_positions(self):
        seen = set()
        for palace in liuyao.PALACE_ELEMENT:
            for stage, (u, l) in zip(liuyao.PALACE_STAGE_NAMES, liuyao.palace_sequence(palace)):
                p, s, shi = liuyao.palace_of(u, l)
                self.assertEqual(p, palace)
                self.assertEqual(s, stage)
                ying = shi + 3 if shi <= 3 else shi - 3
                self.assertTrue(1 <= shi <= 6 and 1 <= ying <= 6)
                self.assertNotEqual(shi, ying)
                seen.add(stage)
        self.assertEqual(seen, set(liuyao.PALACE_STAGE_NAMES))

    def test_najia_known_charts(self):
        qian = liuyao.build([7, 7, 7, 7, 7, 7], "shake", datetime(2026, 10, 31, 12, 0))
        self.assertEqual([r["najia"] for r in qian["hexagram"]["lines"]],
                         ["甲子", "甲寅", "甲辰", "壬午", "壬申", "壬戌"])
        kun = liuyao.build([8, 8, 8, 8, 8, 8], "shake", datetime(2026, 10, 31, 12, 0))
        self.assertEqual([r["najia"] for r in kun["hexagram"]["lines"]],
                         ["乙未", "乙巳", "乙卯", "癸丑", "癸亥", "癸酉"])

    def test_six_relations_for_qian(self):
        chart = liuyao.build([7, 7, 7, 7, 7, 7], "shake", datetime(2026, 10, 31, 12, 0))
        rel = [r["six_relation"] for r in chart["hexagram"]["lines"]]
        self.assertEqual(rel, ["子孙", "妻财", "父母", "官鬼", "兄弟", "父母"])

    def test_six_shen_order(self):
        chart = liuyao.build([7, 7, 7, 7, 7, 7], "shake", datetime(2026, 10, 31, 12, 0))
        liushen = [r["liu_shen"] for r in chart["hexagram"]["lines"]]
        expected_start = liuyao.DAY_GAN_LIUSHEN_START[chart["day_ganzhi"][0]]
        self.assertEqual(liushen, [liuyao.LIUSHEN[(expected_start + i) % 6] for i in range(6)])

    def test_changed_hexagram(self):
        chart = liuyao.build([9, 6, 7, 8, 7, 8], "shake", datetime(2026, 10, 31, 12, 0))
        self.assertEqual(chart["moving_lines"], [1, 2])
        self.assertIsNotNone(chart["changed"]["name"])
        static = liuyao.build([7, 8, 7, 8, 7, 8], "shake", datetime(2026, 10, 31, 12, 0))
        self.assertIsNone(static["changed"]["name"])
        self.assertEqual(static["moving_lines"], [])

    def test_time_method(self):
        chart = liuyao.build(None, "time", datetime(2026, 10, 31, 19, 40))
        self.assertEqual(chart["method"], "time")
        self.assertEqual(len(chart["hexagram"]["lines"]), 6)
        self.assertEqual(len(chart["moving_lines"]), 1)

    def test_invalid_lines(self):
        with self.assertRaises(ValueError):
            liuyao.build([1, 2, 3], "shake", datetime(2026, 10, 31, 12, 0))
        with self.assertRaises(ValueError):
            liuyao.build([7, 7, 7, 7, 7, 10], "shake", datetime(2026, 10, 31, 12, 0))


if __name__ == "__main__":
    unittest.main(verbosity=2)
