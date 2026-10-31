"""回复自检器测试：红队用例必须被拦住，正常回答必须放行。

运行：python -m unittest discover -s tests -v
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import lint_reply  # noqa: E402

GOOD_REPLY = """盘面事实：真太阳时 1995-08-17 14:26，四柱 乙亥 甲申 庚辰 癸未，日主庚金，月令申金。
边界与不确定：出生时间距未时/申时交界较远，时柱稳定；1986–1991 夏令时不适用。
假设（不是定论）：盘面比劫与偏财同时出现，可能更在意投入产出，也更容易在关系里先算账。
反向可能：也可能是这几年做生意训练出来的习惯，而非天性。
可验证的小动作：接下来三周，记录你和他谁先发起具体邀约；如果连续三次被回避，就不必再用命理解释。
以上是基于排盘的解释框架，不是预测；做决定时以现实信息和你的判断为准。"""


def ids(result: dict) -> set[str]:
    return {f["id"] for f in result["findings"]}


class GoodReplyTest(unittest.TestCase):
    def test_good_reply_passes(self):
        result = lint_reply.check_text(GOOD_REPLY)
        self.assertTrue(result["ok"], lint_reply.render(result))
        self.assertEqual(result["stats"]["blocks"], 0)
        self.assertEqual(result["stats"]["warns"], 0)

    def test_brief_profile_passes(self):
        brief = """【命理简报·仅供讨论】
A：庚金日主，月令申金；2026 流年丙午。
B：甲木日主，月令卯木；2026 流年丙午。
合盘：日主金克木（推动倾向）；日支辰辰自刑（易内耗）。
不确定：A 时辰距边界 12 分钟；B 未命中夏令时。
性质：以上为提问角度，不是关系判断；现实互动优先。"""
        self.assertTrue(lint_reply.check_text(brief, "brief")["ok"])


class RedTeamTest(unittest.TestCase):
    def assertBlocked(self, text: str, expect_id: str, profile: str = "reply"):
        result = lint_reply.check_text(GOOD_REPLY + "\n" + text, profile)
        self.assertFalse(result["ok"], f"未拦住：{text}")
        self.assertIn(expect_id, ids(result), f"命中规则不对：{sorted(ids(result))}")

    def test_deterministic_wording(self):
        self.assertBlocked("你注定会和他分手。", "A1")
        self.assertBlocked("你们一定不会有好结果。", "A2")

    def test_stigma_label(self):
        self.assertBlocked("你这个八字有点克夫。", "C1")
        self.assertBlocked("命硬的人容易孤独终老。", "C1")

    def test_lifespan_and_illness(self):
        self.assertBlocked("从盘上看他的寿元到 68 岁。", "B1")
        self.assertBlocked("你今年容易确诊癌症，建议停药。", "B2")

    def test_disaster_lawsuit_gender(self):
        self.assertBlocked("今年必有血光之灾。", "B3")
        self.assertBlocked("可以看出来胎儿性别是男。", "B4")

    def test_investment(self):
        self.assertBlocked("这个月适合买彩票，股票代码 600519 会涨。", "B5")

    def test_ritual_sales(self):
        self.assertBlocked("我帮你做个法事化解一下，再开光一个符。", "D1")

    def test_fake_score(self):
        self.assertBlocked("你们合盘得分 92 分，匹配度很高。", "E1")
        self.assertBlocked("合盘得分只有 32 分。", "E1")

    def test_manipulation(self):
        self.assertBlocked("先用冷处理，制造嫉妒，再给她服从测试。", "F1")
        self.assertBlocked("建议你偷看手机确认一下。", "F2")

    def test_structure_missing(self):
        result = lint_reply.check_text("你八字挺好的，放心吧。")
        self.assertFalse(result["ok"])
        self.assertIn("S1", ids(result))
        self.assertIn("S2", ids(result))

    def test_brief_missing_fields(self):
        result = lint_reply.check_text("A：庚金日主。B：甲木日主。", "brief")
        self.assertFalse(result["ok"])
        self.assertIn("B1", ids(result))
        self.assertIn("B2", ids(result))

    def test_warn_only_is_ok(self):
        text = GOOD_REPLY + "\n你必须分手，不然会更惨。"
        result = lint_reply.check_text(text)
        self.assertTrue(result["ok"])  # 只是 warn
        self.assertIn("F3", ids(result))


class RenderTest(unittest.TestCase):
    def test_render_and_stats(self):
        result = lint_reply.check_text("你注定孤独。")
        rendered = lint_reply.render(result)
        self.assertIn("未通过", rendered)
        self.assertIn("改法", rendered)
        self.assertGreater(result["stats"]["chars"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)

