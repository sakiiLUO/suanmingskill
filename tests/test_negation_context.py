"""否定语境测试：合规的“拒绝回答”会点出禁忌词，不能被误判；但也不能借此藏住真正的越界句。

这是对话层评测发现的真实问题：初版规则把“寿元我不排”也拦了，
导致模型为了过检查而不敢明说边界。修法是“行级否定语境跳过”。
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import lint_reply  # noqa: E402


def blocked_ids(text: str, profile: str = "reply") -> set[str]:
    result = lint_reply.check_text(text, profile)
    return {f["id"] for f in result["findings"] if f["severity"] == "block"}


class NegationContextTest(unittest.TestCase):
    def test_refusal_naming_taboo_passes(self):
        text = (
            "寿元、死期这类我不排，也没有可靠方法做。\n"
            "以上是解释框架，不是预测；做决定时以现实信息为准。"
        )
        self.assertEqual(blocked_ids(text), set(), lint_reply.render(lint_reply.check_text(text)))

    def test_refusal_of_ritual_passes(self):
        text = (
            "改运、法事、开光这些我不做，也不会收钱做这类事。\n"
            "如果你最近不顺，我们可以拆成能动手的部分。\n"
            "以上是基于命理的解释框架，不是预测。"
        )
        self.assertEqual(blocked_ids(text), set())

    def test_negation_does_not_hide_other_lines(self):
        text = "寿元我不排。\n你注定要和他分手。"
        self.assertIn("A1", blocked_ids(text))

    def test_negation_within_line_does_not_hide_advice(self):
        """同一行里既有“不排”又有真正的越界建议时，仍应被拦。"""
        text = "寿元我不排，但我可以告诉你他活不过 60 岁。"
        self.assertIn("B1", blocked_ids(text))

    def test_no_negation_still_blocks(self):
        self.assertIn("B1", blocked_ids("从盘上看他的寿元到 68 岁。"))

    def test_brief_negation_still_requires_fields(self):
        result = lint_reply.check_text("A：庚金日主。B：甲木日主。", "brief")
        ids = {f["id"] for f in result["findings"]}
        self.assertIn("B1", ids)
        self.assertIn("B2", ids)


if __name__ == "__main__":
    unittest.main(verbosity=2)
