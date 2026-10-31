"""对话层评测的回归测试：用例集必须全部符合期望。

它把 tests/cases/dialogue_cases.json 变成 CI 可跑的断言，
以后新增红队用例只需要加 JSON，不需要改测试代码。
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import eval_dialogue  # noqa: E402


class DialogueEvalTest(unittest.TestCase):
    def test_all_cases_match_expectation(self):
        rows = [eval_dialogue.run(c) for c in eval_dialogue.load_cases()]
        self.assertGreaterEqual(len(rows), 15, "红队用例太少，覆盖不足")
        failed = [r for r in rows if not r["ok"]]
        self.assertEqual(
            failed, [],
            "不符合期望的用例：\n" + eval_dialogue.render(rows),
        )

    def test_every_block_case_has_expected_rule(self):
        rows = [eval_dialogue.run(c) for c in eval_dialogue.load_cases()]
        for r in rows:
            if r["expect"] == "block":
                self.assertTrue(r["missed_ids"] == [], f"{r['id']} 未命中期望规则")

    def test_case_ids_unique(self):
        ids = [c["id"] for c in eval_dialogue.load_cases()]
        self.assertEqual(len(ids), len(set(ids)), "用例 id 重复")


if __name__ == "__main__":
    unittest.main(verbosity=2)
