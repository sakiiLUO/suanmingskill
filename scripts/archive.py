"""命理档案：最小化、可撤销、需明确同意的本地 JSON 记录。

原则（与狗头军师的关系档案协议保持一致）：
- 默认不写盘；必须显式 --consent 才保存。
- 只存排盘必需的字段，不存聊天原文、不存截图、不存他人评价。
- 随时可 list / show / delete；删除是硬删除。
- 档案目录默认在工作区 .suanming/，可用 --dir 或 SUANMING_ARCHIVE_DIR 覆盖。
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime
from pathlib import Path

SCHEMA = "suanming.profile.v1"
FIELDS = ("name", "gender", "birth_clock", "city", "longitude", "tz_hours",
          "dst_mode", "late_zi", "pillars", "day_master", "notes")
FPLACE = "（本档案只保存排盘所需字段，不含聊天原文与截图）"


def archive_dir(explicit: str | None) -> Path:
    d = explicit or os.environ.get("SUANMING_ARCHIVE_DIR") or ".suanming"
    p = Path(d).expanduser().resolve()
    p.mkdir(parents=True, exist_ok=True)
    return p


def _path(d: Path, name: str) -> Path:
    safe = "".join(c for c in name if c.isalnum() or c in "._-一-鿿")[:40] or "profile"
    return d / f"{safe}.json"


def save(d: Path, payload: dict, consent: bool) -> Path:
    if not consent:
        raise SystemExit("未提供 --consent：默认不落盘。用户明确同意后再加 --consent 保存。")
    data = {k: payload.get(k) for k in FIELDS if k in payload}
    data["schema"] = SCHEMA
    data["updated_at"] = datetime.now().isoformat(timespec="seconds")
    data["notice"] = FPLACE
    name = str(payload.get("name") or "profile")
    path = _path(d, name)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def list_profiles(d: Path) -> list[dict]:
    rows = []
    for p in sorted(d.glob("*.json")):
        try:
            data = _load(p)
        except (OSError, json.JSONDecodeError):
            continue
        if data.get("schema") != SCHEMA:
            continue  # 跳过 paipan 原始输出等非档案文件
        rows.append({
            "file": p.name,
            "name": data.get("name"),
            "gender": data.get("gender"),
            "birth_clock": data.get("birth_clock"),
            "pillars": data.get("pillars"),
            "updated_at": data.get("updated_at"),
            "sha256": hashlib.sha256(p.read_bytes()).hexdigest()[:12],
        })
    return rows


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="命理档案（需同意、可删除）")
    ap.add_argument("command", choices=["save", "list", "show", "delete"])
    ap.add_argument("--dir", help="档案目录，默认 .suanming/")
    ap.add_argument("--name", help="代号，如 我 / A / 对象B")
    ap.add_argument("--json", dest="json_file", help="save 时读取 paipan 输出 JSON 或档案 JSON")
    ap.add_argument("--notes", help="用户补充的背景（勿写聊天原文）")
    ap.add_argument("--consent", action="store_true", help="用户已明确同意保存")
    args = ap.parse_args(argv)
    d = archive_dir(args.dir)

    if args.command == "list":
        print(json.dumps(list_profiles(d), ensure_ascii=False, indent=2))
        return 0

    if args.command == "save":
        if not (args.name and args.json_file):
            ap.error("save 需要 --name 与 --json")
        payload = _load(Path(args.json_file))
        payload.setdefault("name", args.name)
        if args.notes:
            payload["notes"] = args.notes
        path = save(d, payload, args.consent)
        print(f"已保存：{path}")
        return 0

    if not args.name:
        ap.error("show/delete 需要 --name")
    path = _path(d, args.name)
    if args.command == "show":
        if not path.exists():
            print(f"没有找到档案：{path}", file=sys.stderr)
            return 1
        print(json.dumps(_load(path), ensure_ascii=False, indent=2))
        return 0

    if path.exists():
        path.unlink()
        print(f"已删除：{path}")
    else:
        print("档案不存在，无需删除。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

