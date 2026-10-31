"""校验 skill 包：结构、frontmatter、引用链接、脚本可编译、依赖许可、禁用内容。

用法：python scripts/validate_skill.py [--skill-dir .] [--verbose]
CI 建议在提交前运行；退出码非 0 表示不可发布。
"""

from __future__ import annotations

import argparse

import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    "核心原则",
    "首次使用",
    "排盘流程",
    "合盘与配合",
    "按需加载",
    "安全与伦理边界",
    "发送前自检",
    "领域路由",
]

REQUIRED_FILES = [
    "SKILL.md",
    "references/00-导读与加载路由.md",
    "references/07-事业-财运-职业方向.md",
    "references/08-学业-考试与专业选择.md",
    "references/09-身心状态与健康边界.md",
    "references/10-家庭六亲与代际关系.md",
    "references/11-古籍与文献索引.md",
    "references/12-证据分级与现代研究.md",
    "references/13-经文与格言.md",
    "scripts/paipan.py",
    "scripts/hepan.py",
    "scripts/archive.py",
    "scripts/lint_reply.py",
    "scripts/eval_dialogue.py",
    "scripts/check_language.py",
    "scripts/validate_skill.py",
    "NOTICE.md",
]

FORBIDDEN_PATTERNS = [
    (re.compile(r"[A-Z]:\\\\|/Users/|/home/"), "绝对路径"),
    (re.compile(r"TODO|FIXME|待补充"), "未完成标记"),
    (re.compile(r"sk-[A-Za-z0-9]{16,}"), "疑似密钥"),
]

MAX_REFERENCE_BYTES = 40_000


def parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    meta = {}
    for line in text[3:end].splitlines():
        if ":" in line and not line.lstrip().startswith("#"):
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skill-dir", default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args(argv)

    root = Path(args.skill_dir).resolve()
    errors: list[str] = []
    warns: list[str] = []

    for rel in REQUIRED_FILES:
        if not (root / rel).exists():
            errors.append(f"缺少文件：{rel}")

    skill_md = root / "SKILL.md"
    if skill_md.exists():
        text = skill_md.read_text(encoding="utf-8")
        meta = parse_frontmatter(text)
        for key in ("name", "description"):
            if not meta.get(key):
                errors.append(f"frontmatter 缺少 {key}")
        if meta.get("name") and not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,63}", meta["name"]):
            errors.append("frontmatter name 需要小写字母/数字/连字符")
        for sec in REQUIRED_SECTIONS:
            if sec not in text:
                errors.append(f"SKILL.md 缺少章节：{sec}")
        if len(text) > 24_000:
            warns.append(f"SKILL.md 偏长（{len(text)} 字符），考虑移到 references/")

        for rel in re.findall(r"`(references/[^`]+\.md)`", text):
            if not (root / rel).exists():
                errors.append(f"SKILL.md 引用了不存在的文件：{rel}")

    for ref in sorted((root / "references").glob("*.md")):
        size = ref.stat().st_size
        if size > MAX_REFERENCE_BYTES:
            errors.append(f"{ref.name} 超过 {MAX_REFERENCE_BYTES} 字节（{size}）")
        if size < 200:
            warns.append(f"{ref.name} 内容过短（{size} 字节）")

    for py in sorted((root / "scripts").glob("*.py")):
        try:
            compile(py.read_text(encoding="utf-8"), str(py), "exec")
        except SyntaxError as exc:
            errors.append(f"{py.name} 编译失败：{exc.msg}")

    # 多语言 README：语言切换条里链接的版本必须存在，且每个版本要链回 README.md
    readme = root / "README.md"
    if readme.exists():
        text = readme.read_text(encoding="utf-8")
        langs = sorted(set(re.findall(r"\((README\.[A-Za-z-]+\.md)\)", text)))
        for name in langs:
            target = root / name
            if not target.exists():
                errors.append(f"语言切换条引用了不存在的文件：{name}")
            elif "(README.md)" not in target.read_text(encoding="utf-8"):
                errors.append(f"{name} 缺少指回 README.md 的语言切换链接")
        if not langs:
            warns.append("README 没有语言切换条（单语仓库可忽略）")

        # AI 安装提示词：每个语言版本都要有，且标记成对出现
        ai_files = [readme] + [root / name for name in langs]
        for f in ai_files:
            if not f.exists():
                continue
            body = f.read_text(encoding="utf-8")
            if "AI-INSTALL:START" not in body or "AI-INSTALL:END" not in body:
                errors.append(f"{f.name} 缺少 AI 安装提示词标记（AI-INSTALL:START/END）")
            elif body.index("AI-INSTALL:START") > body.index("AI-INSTALL:END"):
                errors.append(f"{f.name} 的 AI 安装提示词标记顺序反了")
    notice = root / "NOTICE.md"
    if notice.exists():
        ntext = notice.read_text(encoding="utf-8")
        for dep in ("lunar-python", "MIT"):
            if dep not in ntext:
                errors.append(f"NOTICE.md 未声明依赖或许可证：{dep}")
    if not (root / "vendor" / "lunar_python").is_dir() and not (root.parent / "vendor" / "lunar_python").is_dir():
        warns.append("未找到 vendor/lunar_python，运行期需自行 pip install lunar-python")

    for path in list(root.glob("*.md")) + list((root / "references").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        for pattern, label in FORBIDDEN_PATTERNS:
            if pattern.search(text):
                errors.append(f"{path.name} 命中禁用内容：{label}")

    if args.verbose:
        for w in warns:
            print(f"WARN  {w}")
    if errors:
        for e in errors:
            print(f"ERROR {e}")
        print(f"\n校验失败：{len(errors)} 个错误")
        return 1
    print(f"校验通过：{root}（{len(warns)} 条警告）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())








