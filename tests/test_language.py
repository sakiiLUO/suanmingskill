"""语言策略回归测试：五语言各自回答、其他语言回落英语。

同时锁住 lint 的多语言结构识别（否则英文/日文回答会被 S1 误判为“缺边界段”）。
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_language  # noqa: E402
import lint_reply  # noqa: E402


class DetectTest(unittest.TestCase):
    def test_english_with_chinese_terms_is_english(self):
        """英文回答里引用中文术语/经文，不能判成中文。"""
        text = ("Chart facts: true solar time 1995-08-17, Four Pillars 乙亥 甲申 庚辰 癸未. "
                "Boundaries and uncertainty: stable. Hypothesis: carry pressure alone. "
                "One small check: look back at three events. This is an interpretive frame.")
        self.assertEqual(check_language.detect(text)[0], "en")

    def test_simplified_and_traditional(self):
        self.assertEqual(check_language.detect("边界与不确定：时柱稳定，假设与可验证动作如下。")[0], "zh-CN")
        self.assertEqual(check_language.detect("邊界與不確定：時柱穩定，假設與可驗證動作如下。")[0], "zh-TW")

    def test_cantonese(self):
        self.assertEqual(check_language.detect("唔鍾意示弱，佢嘅習慣係自己扛，咁樣好攰。")[0], "yue")

    def test_japanese(self):
        self.assertEqual(check_language.detect("仮説ですが、境界と不確実性を確認してください。")[0], "ja")


class CaseTest(unittest.TestCase):
    def test_all_language_cases(self):
        rows = check_language.run()
        self.assertGreaterEqual(len(rows), 6)
        failed = [r for r in rows if not r["ok"]]
        self.assertEqual(failed, [], check_language.render(rows))

    def test_every_case_passes_lint(self):
        for case in check_language.load_cases():
            result = lint_reply.check_text(case["draft"])
            self.assertTrue(result["ok"], f"{case['id']} 未通过 lint：{lint_reply.render(result)}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
