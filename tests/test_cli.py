"""CLI 级端到端测试：直接调用 scripts/*.py，验证参数、退出码与输出契约。

区别：test_suanming.py 测函数，这里测“模型真正敲的命令能不能跑通”。
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
PY = sys.executable


def run(args: list[str], stdin: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [PY, "-X", "utf8", *args],
        capture_output=True, text=True, encoding="utf-8", stdin=subprocess.PIPE if stdin else None,
        input=stdin, cwd=str(ROOT),
    )


class PaipanCliTest(unittest.TestCase):
    def test_brief(self):
        r = run([str(SCRIPTS / "paipan.py"), "--birth", "1995-08-17 14:30",
                 "--gender", "male", "--city", "杭州", "--format", "brief"])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("乙亥 甲申 庚辰 癸未", r.stdout)
        self.assertIn("真太阳时", r.stdout)

    def test_json_contract_and_save(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "a.json"
            r = run([str(SCRIPTS / "paipan.py"), "--birth", "1996-03-08 09:15",
                     "--gender", "female", "--city", "北京", "--save", str(out)])
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertTrue(out.exists())
            data = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(data["schema"], "suanming.paipan.v1")
            self.assertEqual(data["input"]["gender"], "female")
            self.assertIn("warnings", data)

    def test_bad_birth_returns_2(self):
        r = run([str(SCRIPTS / "paipan.py"), "--birth", "1995/13/40", "--gender", "male", "--city", "杭州"])
        self.assertEqual(r.returncode, 2)
        self.assertIn("错误", r.stderr)

    def test_unknown_city_returns_2(self):
        r = run([str(SCRIPTS / "paipan.py"), "--birth", "1995-08-17 14:30",
                 "--gender", "male", "--city", "不存在市"])
        self.assertEqual(r.returncode, 2)
        self.assertIn("经度", r.stderr)

    def test_dst_warning_in_output(self):
        r = run([str(SCRIPTS / "paipan.py"), "--birth", "1990-06-15 09:10",
                 "--gender", "male", "--city", "上海", "--format", "brief"])
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("夏令时", r.stdout)


class HepanCliTest(unittest.TestCase):
    def test_hepan_from_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            a, b = Path(tmp) / "a.json", Path(tmp) / "b.json"
            for path, birth, gender, city in ((a, "1995-08-17 14:30", "male", "杭州"),
                                              (b, "1996-03-08 09:15", "female", "北京")):
                run([str(SCRIPTS / "paipan.py"), "--birth", birth, "--gender", gender,
                     "--city", city, "--save", str(path)])
            r = run([str(SCRIPTS / "hepan.py"), "--a-json", str(a), "--b-json", str(b)])
            self.assertEqual(r.returncode, 0, r.stderr)
            out = json.loads(r.stdout)
            self.assertEqual(out["schema"], "suanming.hepan.v1")
            self.assertGreaterEqual(len(out["axes"]), 5)
            self.assertNotIn("score", json.dumps(out).lower())  # 不允许伪精确总分

    def test_missing_args(self):
        r = run([str(SCRIPTS / "hepan.py"), "--a-birth", "1995-08-17 14:30"])
        self.assertNotEqual(r.returncode, 0)


class ArchiveCliTest(unittest.TestCase):
    def test_requires_consent(self):
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp) / "a.json"
            run([str(SCRIPTS / "paipan.py"), "--birth", "1995-08-17 14:30",
                 "--gender", "male", "--city", "杭州", "--save", str(src)])
            r = run([str(SCRIPTS / "archive.py"), "save", "--name", "A",
                     "--json", str(src), "--dir", str(Path(tmp) / "arc")])
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("consent", r.stderr.lower() + r.stdout.lower())

    def test_save_list_delete(self):
        with tempfile.TemporaryDirectory() as tmp:
            arc = Path(tmp) / "arc"
            src = Path(tmp) / "a.json"
            run([str(SCRIPTS / "paipan.py"), "--birth", "1995-08-17 14:30",
                 "--gender", "male", "--city", "杭州", "--save", str(src)])
            r = run([str(SCRIPTS / "archive.py"), "save", "--name", "A",
                     "--json", str(src), "--dir", str(arc), "--consent"])
            self.assertEqual(r.returncode, 0, r.stderr)
            r = run([str(SCRIPTS / "archive.py"), "list", "--dir", str(arc)])
            rows = json.loads(r.stdout)
            self.assertEqual(rows[0]["name"], "A")
            r = run([str(SCRIPTS / "archive.py"), "delete", "--name", "A", "--dir", str(arc)])
            self.assertEqual(r.returncode, 0)
            r = run([str(SCRIPTS / "archive.py"), "list", "--dir", str(arc)])
            self.assertEqual(json.loads(r.stdout), [])


class LintCliTest(unittest.TestCase):
    def test_good_exit_0(self):
        r = run([str(SCRIPTS / "lint_reply.py"), "--text",
                 "边界与不确定：时柱稳定。\n假设：可能更在意投入产出。\n"
                 "以上是解释框架，不是预测。\n接下来三周记录谁先发起邀约。"])
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_bad_exit_1(self):
        r = run([str(SCRIPTS / "lint_reply.py"), "--text", "你注定要分手。"])
        self.assertEqual(r.returncode, 1)
        self.assertIn("BLOCK", r.stdout)

    def test_json_output(self):
        r = run([str(SCRIPTS / "lint_reply.py"), "--text", "你注定要分手。", "--json"])
        payload = json.loads(r.stdout)
        self.assertFalse(payload["ok"])
        self.assertIn("A1", {f["id"] for f in payload["findings"]})

    def test_missing_file_exit_2(self):
        r = run([str(SCRIPTS / "lint_reply.py"), "--file", str(ROOT / "不存在.md")])
        self.assertEqual(r.returncode, 2)


class EvalCliTest(unittest.TestCase):
    def test_dialogue_cases_all_pass(self):
        r = run([str(SCRIPTS / "eval_dialogue.py")])
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("失败 0", r.stdout)


class ValidatorCliTest(unittest.TestCase):
    def test_validate_passes(self):
        r = run([str(SCRIPTS / "validate_skill.py")])
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("校验通过", r.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
