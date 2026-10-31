"""回归与不变量测试：锁定真太阳时、节气边界、晚子时与干支连续性。

运行：python -m unittest discover -s tests -v
"""

from __future__ import annotations

import sys
import unittest
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import hepan  # noqa: E402
import paipan  # noqa: E402
import solartime  # noqa: E402

GAN = "甲乙丙丁戊己庚辛壬癸"
ZHI = "子丑寅卯辰巳午未申酉戌亥"


def gz_index(ganzhi: str) -> int:
    return next(i for i in range(60) if GAN[i % 10] + ZHI[i % 12] == ganzhi)


class SolarTimeTest(unittest.TestCase):
    def test_cn_dst_periods(self):
        self.assertEqual(solartime.dst_minutes(datetime(1990, 6, 15, 9, 10), "auto"), 60)
        self.assertEqual(solartime.dst_minutes(datetime(1990, 4, 14, 9, 10), "auto"), 0)  # 首日前一天
        self.assertEqual(solartime.dst_minutes(datetime(1990, 4, 15, 9, 10), "auto"), 60)
        self.assertEqual(solartime.dst_minutes(datetime(1992, 6, 15, 9, 10), "auto"), 0)  # 1991 后取消
        self.assertEqual(solartime.dst_minutes(datetime(1990, 6, 15, 9, 10), "off"), 0)
        self.assertEqual(solartime.dst_minutes(datetime(2000, 1, 1, 9, 10), "on"), 60)

    def test_longitude_correction(self):
        corr = solartime.true_solar_time(datetime(1995, 8, 17, 14, 30), 120.155)
        self.assertAlmostEqual(corr["longitude_correction_minutes"], 0.62, places=2)
        self.assertAlmostEqual(corr["eot_minutes"], -4.5, delta=1.0)

    def test_equation_of_time_bounds(self):
        for month in range(1, 13):
            eot = solartime.equation_of_time_minutes(datetime(2020, month, 15, 12))
            self.assertGreater(eot, -17.5)
            self.assertLess(eot, 17.5)

    def test_shichen(self):
        self.assertEqual(solartime.shichen_name(solartime.shichen_index(datetime(2020, 1, 1, 23, 30))), "子")
        self.assertEqual(solartime.shichen_name(solartime.shichen_index(datetime(2020, 1, 1, 0, 30))), "子")
        self.assertEqual(solartime.shichen_name(solartime.shichen_index(datetime(2020, 1, 1, 14, 30))), "未")

    def test_city_lookup(self):
        lon, src = solartime.resolve_longitude("杭州市", None)
        self.assertAlmostEqual(lon, 120.155)
        self.assertTrue(src.startswith("city:"))
        with self.assertRaises(ValueError):
            solartime.resolve_longitude("不存在市", None)


class PaipanTest(unittest.TestCase):
    def test_reference_chart(self):
        d = paipan.chart(datetime(1995, 8, 17, 14, 30), "male", 120.155)
        self.assertEqual([d["pillars"][k]["ganzhi"] for k in ("year", "month", "day", "time")],
                         ["乙亥", "甲申", "庚辰", "癸未"])
        self.assertEqual(d["day_master"]["gan"], "庚")
        self.assertEqual(d["time_correction"]["shichen"], "未")
        self.assertFalse(d["time_correction"]["late_zi_applied"])

    def test_lichun_boundary(self):
        before = paipan.chart(datetime(1995, 2, 3, 12, 0), "male", 120.0)
        after = paipan.chart(datetime(1995, 2, 5, 12, 0), "male", 120.0)
        self.assertEqual(before["pillars"]["year"]["ganzhi"], "甲戌")
        self.assertEqual(after["pillars"]["year"]["ganzhi"], "乙亥")
        self.assertNotEqual(before["pillars"]["month"]["ganzhi"], after["pillars"]["month"]["ganzhi"])

    def test_late_zi_toggle(self):
        next_day = paipan.chart(datetime(1995, 8, 17, 23, 30), "male", 120.155, late_zi="next_day")
        same_day = paipan.chart(datetime(1995, 8, 17, 23, 30), "male", 120.155, late_zi="same_day")
        self.assertEqual(next_day["pillars"]["day"]["ganzhi"], "辛巳")
        self.assertEqual(same_day["pillars"]["day"]["ganzhi"], "庚辰")
        self.assertTrue(any("晚子时" in w for w in next_day["warnings"]))

    def test_dst_chart(self):
        d = paipan.chart(datetime(1990, 6, 15, 9, 10), "male", 121.474)
        self.assertEqual(d["time_correction"]["dst_minutes"], 60)
        self.assertEqual(d["pillars"]["time"]["ganzhi"], "壬辰")  # 回拨后为辰时

    def test_day_pillar_continuity(self):
        """连续 60 天的日柱必须逐日 +1，防止历算层换表/时区漂移。"""
        start = datetime(1995, 1, 1, 12, 0)
        prev = None
        for i in range(60):
            d = paipan.chart(start + timedelta(days=i), "female", 120.0)
            cur = gz_index(d["pillars"]["day"]["ganzhi"])
            if prev is not None:
                self.assertEqual((prev + 1) % 60, cur, f"第 {i} 天日柱不连续")
            prev = cur

    def test_hour_gan_rule(self):
        """五鼠遁：甲己日起甲子、乙庚日起丙子、丙辛日起戊子、丁壬日起庚子、戊癸日起壬子。"""
        start_map = {"甲": "甲", "己": "甲", "乙": "丙", "庚": "丙", "丙": "戊",
                     "辛": "戊", "丁": "庚", "壬": "庚", "戊": "壬", "癸": "壬"}
        for day in (datetime(1995, 8, 17, 2, 0), datetime(2001, 3, 5, 2, 30), datetime(2010, 12, 1, 1, 30)):
            d = paipan.chart(day, "male", 120.0)
            day_gan = d["pillars"]["day"]["gan"]
            hour_gan = d["pillars"]["time"]["gan"]
            base = GAN.index(start_map[day_gan])
            expect = GAN[(base + ZHI.index(d["pillars"]["time"]["zhi"])) % 10]
            self.assertEqual(hour_gan, expect)

    def test_national_standard_anchor(self):
        """GB/T 33661-2017 规定干支纪日参照 1949-10-01 为甲子日。"""
        d = paipan.chart(datetime(1949, 10, 1, 12, 0), "male", 116.4)
        self.assertEqual(d["pillars"]["day"]["ganzhi"], "甲子")

    def test_output_contract(self):
        d = paipan.chart(datetime(2000, 1, 1, 0, 30), "female", 116.4)
        for key in ("schema", "input", "time_correction", "pillars", "day_master",
                    "wuxing", "yun", "liunian", "warnings", "disclaimer"):
            self.assertIn(key, d)
        self.assertEqual(sum(d["wuxing"]["counts"].values()) > 0, True)
        self.assertEqual(len(d["yun"]["dayun"]), 9)
        paipan.to_brief(d)  # brief 渲染不抛错


class HepanTest(unittest.TestCase):
    def test_branch_relations(self):
        self.assertEqual(hepan.branch_relation("子", "丑"), "六合")
        self.assertEqual(hepan.branch_relation("子", "午"), "相冲")
        self.assertEqual(hepan.branch_relation("申", "子"), "三合局（半合）")
        self.assertTrue(hepan.branch_relation("寅", "巳").startswith("相刑"))  # 寅巳兼相害
        self.assertEqual(hepan.level_for("无直接刑冲合害"), "中性")
        self.assertEqual(hepan.level_for("相冲（兼相害）"), "需磨合")

    def test_compare_contract(self):
        a = paipan.chart(datetime(1995, 8, 17, 14, 30), "male", 120.155)
        b = paipan.chart(datetime(1996, 3, 8, 9, 15), "female", 116.4)
        out = hepan.compare(a, b)
        self.assertEqual(out["schema"], "suanming.hepan.v1")
        self.assertGreaterEqual(len(out["axes"]), 5)
        for ax in out["axes"]:
            self.assertIn(ax["level"], {"偏合", "中性", "需磨合", "信息不足"})
            self.assertTrue(ax["evidence"])
        self.assertIn("framing", out)


if __name__ == "__main__":
    unittest.main(verbosity=2)



