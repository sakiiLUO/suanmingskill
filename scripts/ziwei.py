"""紫微斗数排盘 CLI：真太阳时校正 → Node 子进程调用 iztro（MIT）→ 结构化 JSON / brief。

依赖说明：紫微用 iztro（MIT，npm），已随仓库 vendor 到 `vendor/iztro/`，离线可用；
需要本机有 Node.js 18+。缺失时给出明确提示，不静默失败。

用法：
  python scripts/ziwei.py --birth "1995-08-17 14:30" --gender male --city 杭州 --format brief
  python scripts/ziwei.py --birth "1990-06-15 09:10" --gender female --city 上海 --year 2026
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import solartime  # noqa: E402

SCHEMA = "suanming.ziwei.v1"
ROOT = Path(__file__).resolve().parents[1]
BRIDGE = Path(__file__).resolve().parent / "ziwei_bridge.cjs"
VENDOR = ROOT / "vendor" / "iztro"
DISCLAIMER = (
    "文化娱乐与自我反思用途，不构成医疗、心理、法律、投资或人生决策建议；"
    "紫微斗数属传统解释框架，不是预测事实。"
)


def parse_birth(text: str) -> datetime:
    text = text.strip().replace("/", "-").replace("T", " ")
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d %H", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    raise argparse.ArgumentTypeError(f"无法解析生日 {text!r}，请用 'YYYY-MM-DD HH:MM'")


def time_index(dt: datetime) -> int:
    """iztro 的时辰序号：0=早子(00:00–00:59)，1=丑 … 11=亥，12=晚子(23:00–23:59)。"""
    return 12 if dt.hour == 23 else (dt.hour + 1) // 2


def node_available() -> str | None:
    return shutil.which("node")


def ensure_iztro() -> None:
    if not (VENDOR / "node_modules" / "iztro").is_dir():
        raise SystemExit(
            "缺少紫微依赖 iztro。修复方式：\n"
            f"  cd {VENDOR} && npm install --no-audit --no-fund\n"
            "（仓库正常打包时 vendor/iztro/node_modules 已包含，无需联网）"
        )


def run_bridge(payload: dict, timeout: int = 30) -> dict:
    node = node_available()
    if not node:
        raise SystemExit("紫微排盘需要 Node.js 18+，当前未找到 node，请先安装 Node.js。")
    ensure_iztro()
    proc = subprocess.run(
        [node, str(BRIDGE), json.dumps(payload, ensure_ascii=False)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=timeout,
    )
    if proc.returncode != 0:
        raise SystemExit(f"iztro 调用失败：{(proc.stderr or '').strip()[:500]}")
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"iztro 输出无法解析：{exc}")


def chart(
    birth: datetime,
    gender: str,
    longitude: float,
    tz_hours: float = 8.0,
    dst_mode: str = "auto",
    late_zi: str = "next_day",
    year: int | None = None,
) -> dict:
    corr = solartime.true_solar_time(birth, longitude, tz_hours, dst_mode)
    solar = corr["true_solar"]
    warnings: list[str] = []
    if corr["dst_minutes"]:
        warnings.append(f"命中 1986–1991 中国夏令时，钟表时间已回拨 {corr['dst_minutes']} 分钟。")

    idx = time_index(solar)
    if idx == 12:
        if late_zi == "next_day":
            solar = solar.replace(hour=0)
            warnings.append("晚子时按“换日”处理：日期取次日，时辰记为早子时。")
            idx = 0
        else:
            warnings.append("晚子时按“不换日”处理（iztro timeIndex=12），不同流派口径不同。")

    if solartime.boundary_distance_minutes(solar) <= 10:
        warnings.append("出生时间距时辰交界 ≤10 分钟，时辰存在换柱风险，请复核出生时间。")

    payload = {
        "date": f"{solar.year}-{solar.month}-{solar.day}",
        "timeIndex": idx,
        "gender": gender,
        "year": year,
    }
    iztro = run_bridge(payload)

    palaces = []
    for p in iztro.get("palaces", []):
        palaces.append({
            "name": p.get("name"),
            "stem": p.get("heavenlyStem"),
            "branch": p.get("earthlyBranch"),
            "is_body_palace": p.get("isBodyPalace"),
            "major_stars": [s.get("name") for s in p.get("majorStars", [])],
            "major_stars_detail": p.get("majorStars", []),
            "minor_stars": [s.get("name") for s in p.get("minorStars", [])],
            "adjective_stars": p.get("adjectiveStars", []),
            "changsheng12": p.get("changsheng12"),
            "decadal": p.get("decadal"),
        })

    return {
        "schema": SCHEMA,
        "input": {
            "birth_clock": birth.strftime("%Y-%m-%d %H:%M"),
            "gender": gender,
            "longitude": longitude,
            "tz_hours": tz_hours,
            "dst_mode": dst_mode,
            "late_zi": late_zi,
        },
        "time_correction": {
            "clock": birth.strftime("%Y-%m-%d %H:%M"),
            "dst_minutes": corr["dst_minutes"],
            "longitude_correction_minutes": corr["longitude_correction_minutes"],
            "eot_minutes": corr["eot_minutes"],
            "true_solar_time": solar.strftime("%Y-%m-%d %H:%M"),
            "shichen": solartime.shichen_name(solartime.shichen_index(solar)),
            "time_index": idx,
        },
        "astrolabe": {
            "solar_date": iztro.get("solarDate"),
            "lunar_date": iztro.get("lunarDate"),
            "chinese_date": iztro.get("chineseDate"),
            "time": iztro.get("time"),
            "five_elements_class": iztro.get("fiveElementsClass"),
            "soul": iztro.get("soul"),
            "body": iztro.get("body"),
            "zodiac": iztro.get("zodiac"),
            "sign": iztro.get("sign"),
            "earthly_branch_of_soul_palace": iztro.get("earthlyBranchOfSoulPalace"),
            "earthly_branch_of_body_palace": iztro.get("earthlyBranchOfBodyPalace"),
        },
        "palaces": palaces,
        "horoscope": iztro.get("horoscope"),
        "warnings": warnings,
        "disclaimer": DISCLAIMER,
        "engine": "iztro 2.6.3 (MIT)",
    }


def to_brief(d: dict) -> str:
    a = d["astrolabe"]
    birth_year = int(d["input"]["birth_clock"][:4])
    year = int((d.get("horoscope") or {}).get("year") or datetime.now().year)
    age = year - birth_year + 1  # 虚岁，iztro 的大限按此口径
    lines = [
        f"真太阳时 {d['time_correction']['true_solar_time']}（{d['time_correction']['shichen']}时）",
        f"紫微盘：{a['five_elements_class']}，命主 {a['soul']}，身主 {a['body']}，生肖 {a['zodiac']}",
    ]
    body_palace = None
    for p in d["palaces"]:
        if p.get("is_body_palace"):
            body_palace = p["name"]
    for p in d["palaces"]:
        label = p["name"]
        stars = [s for s in p["major_stars"] if s and s != "—"]
        if label in ("命宫", "夫妻", "官禄", "财帛", "迁移", "福德"):
            tag = "（身宫）" if label == body_palace else ""
            lines.append(f"{label}{tag}：{'、'.join(stars) or '—'}（{p['stem']}{p['branch']}）")
    for p in d["palaces"]:
        dec = p.get("decadal") or {}
        rng = dec.get("range") or []
        if len(rng) == 2 and rng[0] <= age <= rng[1]:
            lines.append(f"当前大限：{rng[0]}–{rng[1]} 岁（{p['name']}宫），{dec['heavenlyStem']}{dec['earthlyBranch']}")
            break
    horoscope = d.get("horoscope") or {}
    yearly = horoscope.get("yearly") or {}
    if yearly:
        raw_mutagen = yearly.get("mutagen") or []
        labels = ("禄", "权", "科", "忌")
        if isinstance(raw_mutagen, dict):
            mutagen = "、".join(f"{k}:{v}" for k, v in raw_mutagen.items())
        else:
            mutagen = "、".join(f"{lab}{name}" for lab, name in zip(labels, raw_mutagen))
        lines.append(f"{year} 流年：{yearly.get('heavenlyStem')}{yearly.get('earthlyBranch')}" +
                     (f"，四化 {mutagen}" if mutagen else ""))
    if d.get("warnings"):
        lines.append("边界提示：" + "；".join(d["warnings"]))
    lines.append("口径：" + d["disclaimer"])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="紫微斗数排盘（iztro，MIT）")
    ap.add_argument("--birth", required=True, help="公历出生时间 'YYYY-MM-DD HH:MM'")
    ap.add_argument("--gender", required=True, choices=["male", "female"])
    ap.add_argument("--city", help="出生城市")
    ap.add_argument("--longitude", type=float, help="出生地经度（东经为正）")
    ap.add_argument("--tz", type=float, default=8.0, help="时区偏移小时，默认 8")
    ap.add_argument("--dst", default="auto", choices=["auto", "on", "off"])
    ap.add_argument("--late-zi", dest="late_zi", default="next_day", choices=["next_day", "same_day"])
    ap.add_argument("--year", type=int, help="流年（默认今年）")
    ap.add_argument("--format", default="json", choices=["json", "brief"])
    ap.add_argument("--save", help="把 JSON 存到指定路径")
    args = ap.parse_args(argv)

    try:
        birth = parse_birth(args.birth)
        longitude, _ = solartime.resolve_longitude(args.city, args.longitude)
        year = args.year or datetime.now().year
        data = chart(birth, args.gender, longitude, args.tz, args.dst, args.late_zi, year)
    except (ValueError, SystemExit, argparse.ArgumentTypeError) as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 2

    if args.save:
        out = Path(args.save)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(to_brief(data) if args.format == "brief" else json.dumps(data, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
