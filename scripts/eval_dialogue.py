"""对话层评测：用「像模型真实会写出来的草稿」跑一遍 lint_reply，比对期望结果。

用例放在 tests/cases/dialogue_cases.json，每个用例：
{
  "id": "refusal-lifespan",
  "question": "帮我算算我什么时候死",
  "profile": "reply | brief",
  "expect": "pass | block",
  "expect_ids": ["B1"],          # block 时要求命中的规则（可空）
  "draft": "……"
}

用法：
  python scripts/eval_dialogue.py               # 跑全部，打印表格
  python scripts/eval_dialogue.py --json        # 机器可读
  python scripts/eval_dialogue.py --verbose     # 打印每条 draft 的检查明细
退出码：0 = 全部符合期望；1 = 有用例不符合。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import lint_reply  # noqa: E402

CASES_DIR = Path(__file__).resolve().parents[1] / "tests" / "cases"


def load_cases(paths: list[str] | None = None) -> list[dict]:
    files = [Path(p) for p in paths] if paths else sorted(CASES_DIR.glob("*.json"))
    if not files:
        raise SystemExit(f"没有找到用例文件：{CASES_DIR}/*.json")
    cases = []
    for f in files:
        data = json.loads(f.read_text(encoding="utf-8"))
        for case in data.get("cases", []):
            if "expect" not in case:
                continue  # 语言等其它类型的用例文件，交给各自的 runner
            case["_file"] = f.name
            cases.append(case)
    return cases


def run(case: dict) -> dict:
    result = lint_reply.check_text(case["draft"], case.get("profile", "reply"))
    got = "pass" if result["ok"] else "block"
    hit_ids = {f["id"] for f in result["findings"] if f["severity"] == "block"}
    expect = case["expect"]
    want_ids = set(case.get("expect_ids") or [])
    ok = got == expect and (not want_ids or want_ids <= hit_ids)
    return {
        "id": case["id"],
        "question": case.get("question", ""),
        "expect": expect,
        "got": got,
        "missed_ids": sorted(want_ids - hit_ids) if expect == "block" else [],
        "extra_block_ids": sorted(hit_ids) if expect == "pass" else [],
        "ok": ok,
        "result": result,
    }


def render(rows: list[dict]) -> str:
    lines = [f"{'结果':<4} {'用例':<28} {'期望':<6} {'实际':<6} 说明"]
    for r in rows:
        mark = "PASS" if r["ok"] else "FAIL"
        note = ""
        if r["ok"]:
            note = "拦住了 " + ",".join(sorted({f["id"] for f in r["result"]["findings"]
                                               if f["severity"] == "block"})) if r["expect"] == "block" else ""
        else:
            if r["expect"] == "block":
                note = f"漏拦：{', '.join(r['missed_ids']) or '规则未覆盖'}"
            else:
                note = f"误拦：{', '.join(r['extra_block_ids'])}"
        lines.append(f"{mark:<4} {r['id']:<28} {r['expect']:<6} {r['got']:<6} {note}")
    total = len(rows)
    passed = sum(1 for r in rows if r["ok"])
    lines.append("")
    lines.append(f"合计 {total} 条：通过 {passed}，失败 {total - passed}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="对话层评测（红队用例集）")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--verbose", action="store_true", help="打印每条草稿的检查明细")
    ap.add_argument("--cases", nargs="*", help="指定用例文件（默认 tests/cases/*.json）")
    args = ap.parse_args(argv)

    rows = [run(c) for c in load_cases(args.cases)]
    if args.verbose:
        for r in rows:
            print(f"\n### {r['id']}  [{r['expect']} → {r['got']}]")
            print(lint_reply.render(r["result"]))
    if args.json:
        print(json.dumps([{k: v for k, v in r.items() if k != "result"} |
                          {"blocks": [f["id"] for f in r["result"]["findings"]
                                      if f["severity"] == "block"]}
                          for r in rows], ensure_ascii=False, indent=2))
    else:
        print(render(rows))
    return 0 if all(r["ok"] for r in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())

