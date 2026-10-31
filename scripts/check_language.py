"""语言策略检查：判断一段回答属于哪种语言，并跑 tests/cases/language_cases.json 回归。

用途：SKILL.md 规定“简中/繁中/粤语/日语/英语五语言优先，其他语言回落英语”。
这条规则是提示词级的，无法像 lint 那样直接约束模型；但可以用“草稿 → 语言检测”做
回归：只要样例回答的语言分类正确，且能通过越界检查，就说明这套规则至少可执行、可测。

用法：
  python scripts/check_language.py                 # 跑用例，打印表格
  python scripts/check_language.py --json
  python scripts/check_language.py --text "..."     # 检测单段文本
退出码：0 = 全部符合；1 = 有不符合。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import lint_reply  # noqa: E402

CASES = Path(__file__).resolve().parents[1] / "tests" / "cases" / "language_cases.json"

KANA = re.compile(r"[\u3040-\u30ff]")
CANTONESE = re.compile(r"嘅|咗|唔|佢|係|喺|咁|啲|冇|嗰|嚟|睇|搵|啱")
TRAD_ONLY = "們個這說時學會來對裡發現國無為與從還讓給後點麼樣經應該數據"
SIMP_ONLY = "们个这说时学会来对里发现国无为与从还让给后点么样经应该数据"
CJK = re.compile(r"[\u4e00-\u9fff]")
LATIN = re.compile(r"[A-Za-z]")


def detect(text: str) -> tuple[str, dict]:
    """返回 (语言标签, 证据)。标签：zh-CN / zh-TW / yue / ja / en / unknown。"""
    evidence: dict[str, float | int] = {}
    if KANA.search(text):
        return "ja", {"kana": len(KANA.findall(text))}
    cantonese = len(CANTONESE.findall(text))
    evidence["cantonese_marks"] = cantonese
    if cantonese >= 3:
        return "yue", evidence
    trad = sum(1 for ch in text if ch in TRAD_ONLY)
    simp = sum(1 for ch in text if ch in SIMP_ONLY)
    evidence["traditional_marks"] = trad
    evidence["simplified_marks"] = simp
    cjk = len(CJK.findall(text))
    latin = len(LATIN.findall(text))
    evidence["cjk"] = cjk
    evidence["latin"] = latin
    # 英文回答里可能引用中文术语/经文，所以先看拉丁是否绝对占优
    if latin >= 50 and latin >= cjk * 3:
        return "en", evidence
    if cjk >= 10:
        if trad > simp:
            return "zh-TW", evidence
        return "zh-CN", evidence
    if latin > cjk * 2 and latin >= 20:
        return "en", evidence
    return "unknown", evidence


def load_cases() -> list[dict]:
    data = json.loads(CASES.read_text(encoding="utf-8"))
    return data["cases"]


def run() -> list[dict]:
    rows = []
    for case in load_cases():
        got, evidence = detect(case["draft"])
        lint = lint_reply.check_text(case["draft"])
        ok = got == case["expect_lang"] and lint["ok"]
        rows.append({
            "id": case["id"],
            "question": case["question"],
            "expect": case["expect_lang"],
            "got": got,
            "lint_ok": lint["ok"],
            "evidence": evidence,
            "ok": ok,
        })
    return rows


def render(rows: list[dict]) -> str:
    out = [f"{'结果':<4} {'用例':<18} {'期望语言':<8} {'检测语言':<8} {'lint':<5}"]
    for r in rows:
        mark = "PASS" if r["ok"] else "FAIL"
        out.append(f"{mark:<4} {r['id']:<18} {r['expect']:<8} {r['got']:<8} "
                   f"{'ok' if r['lint_ok'] else 'FAIL':<5}")
    total = len(rows)
    passed = sum(1 for r in rows if r["ok"])
    out.append("")
    out.append(f"合计 {total} 条：通过 {passed}，失败 {total - passed}")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="语言策略检查（五语言优先，其余回落英语）")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--text", help="只检测一段文本的语言，不跑用例")
    args = ap.parse_args(argv)

    if args.text:
        lang, evidence = detect(args.text)
        print(json.dumps({"lang": lang, "evidence": evidence}, ensure_ascii=False, indent=2))
        return 0

    rows = run()
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        print(render(rows))
    return 0 if all(r["ok"] for r in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
