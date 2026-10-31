"""合盘 CLI：两份排盘结果 → 关系维度对照（带证据与不确定性）。

刻意不输出“匹配度 87 分”这类伪精确总分：只给维度、证据、倾向和置信度，
让狗头军师把命理当作“提问的角度”，而不是关系结论。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import paipan  # noqa: E402
import solartime  # noqa: E402

LIUHE = {("子", "丑"), ("寅", "亥"), ("卯", "戌"), ("辰", "酉"), ("巳", "申"), ("午", "未")}
SANHE = [set("申子辰"), set("亥卯未"), set("寅午戌"), set("巳酉丑")]
CHONG = {("子", "午"), ("丑", "未"), ("寅", "申"), ("卯", "酉"), ("辰", "戌"), ("巳", "亥")}
HAI = {("子", "未"), ("丑", "午"), ("寅", "巳"), ("卯", "辰"), ("申", "亥"), ("酉", "戌")}
XING_PAIRS = {("子", "卯"), ("寅", "巳"), ("巳", "申"), ("寅", "申"),
              ("丑", "戌"), ("戌", "未"), ("丑", "未"), ("辰", "辰"),
              ("午", "午"), ("酉", "酉"), ("亥", "亥")}
WUXING = {"木", "火", "土", "金", "水"}
SHENG = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
KE = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}


def pair(a: str, b: str, table: set[tuple[str, str]]) -> bool:
    return (a, b) in table or (b, a) in table


def branch_relation(x: str, y: str) -> str:
    """地支关系。同时命中多种关系时按“合 > 冲 > 刑 > 害”的顺序给出主关系并标注兼有。"""
    if x == y:
        return "自刑（同支）" if x in {"辰", "午", "酉", "亥"} else "同支"
    kinds = []
    if pair(x, y, LIUHE):
        kinds.append("六合")
    if any(x in g and y in g for g in SANHE):
        kinds.append("三合局（半合）")
    if pair(x, y, CHONG):
        kinds.append("相冲")
    if pair(x, y, XING_PAIRS):
        kinds.append("相刑")
    if pair(x, y, HAI):
        kinds.append("相害")
    if not kinds:
        return "无直接刑冲合害"
    if len(kinds) == 1:
        return kinds[0]
    return f"{kinds[0]}（兼{'、'.join(kinds[1:])}）"


def level_for(relation: str) -> str:
    if relation.startswith("无"):
        return "中性"
    if "六合" in relation or "三合" in relation:
        return "偏合"
    if any(k in relation for k in ("冲", "刑", "害")):
        return "需磨合"
    return "中性"


def wuxing_relation(a: str, b: str) -> tuple[str, str]:
    """A 的日主五行 与 B 的日主五行 关系。"""
    if a == b:
        return "同五行", "节奏相似，容易共振，也容易在同一个短板上互相强化"
    if SHENG[a] == b:
        return f"{a}生{b}", "A 对 B 有输出/照顾倾向，长期要防止单向消耗"
    if SHENG[b] == a:
        return f"{b}生{a}", "B 对 A 有支持倾向，A 需要留意是否只取不予"
    if KE[a] == b:
        return f"{a}克{b}", "A 对 B 有推动/施压倾向，冲突时要留意分寸"
    return f"{b}克{a}", "B 对 A 有推动/施压倾向，A 容易感到被要求"


def spouse_star_count(chart: dict, gender: str) -> dict:
    """配偶星提示：男看财（正财/偏财），女看官杀（正官/七杀）。

    只统计本命盘天干十神与地支藏干十神，不涉及旺衰喜忌，属于粗略提示。
    """
    targets = {"正财", "偏财"} if gender == "male" else {"正官", "七杀"}
    hits = 0
    for key in ("year", "month", "day", "time"):
        blk = chart["pillars"][key]
        if blk["shishen_gan"] in targets:
            hits += 1
        hits += sum(1 for s in blk["shishen_zhi"] if s in targets)
    return {
        "label": "财星（男命配偶星）" if gender == "male" else "官杀（女命配偶星）",
        "count": hits,
        "note": "仅统计出现次数，不代表配偶质量或婚姻成败。",
    }


def axis(name: str, level: str, evidence: str, confidence: str = "中") -> dict:
    return {"axis": name, "level": level, "evidence": evidence, "confidence": confidence}


def compare(a: dict, b: dict) -> dict:
    pa, pb = a["pillars"], b["pillars"]
    dm_a, dm_b = a["day_master"]["wuxing"], b["day_master"]["wuxing"]
    rel_text, rel_meaning = wuxing_relation(dm_a, dm_b)

    day_rel = branch_relation(pa["day"]["zhi"], pb["day"]["zhi"])
    year_rel = branch_relation(pa["year"]["zhi"], pb["year"]["zhi"])
    month_rel = branch_relation(pa["month"]["zhi"], pb["month"]["zhi"])

    axes = [
        axis("日主五行", "偏合" if rel_text in ("同五行",) or "生" in rel_text else "需磨合",
             f"{a['day_master']['gan']}{dm_a} 与 {b['day_master']['gan']}{dm_b}：{rel_text}；{rel_meaning}",
             "中"),
        axis("日支（亲密互动位）", level_for(day_rel),
             f"日支 {pa['day']['zhi']} 与 {pb['day']['zhi']}：{day_rel}。日支常被用来讨论日常相处节奏，不作关系结论。",
             "中"),
        axis("年支（家庭背景位）", level_for(year_rel),
             f"年支 {pa['year']['zhi']} 与 {pb['year']['zhi']}：{year_rel}。仅作“双方家庭风格差异”的提问角度。",
             "低"),
        axis("月支（成长环境位）", level_for(month_rel),
             f"月支 {pa['month']['zhi']} 与 {pb['month']['zhi']}：{month_rel}。反映习惯与价值排序的差异线索。",
             "低"),
    ]

    # 五行互补：一方最弱是否正好是另一方最旺
    weak_a, strong_b = a["wuxing"]["weakest"], b["wuxing"]["strongest"]
    weak_b, strong_a = b["wuxing"]["weakest"], a["wuxing"]["strongest"]
    comp_lines = []
    if weak_a == strong_b:
        comp_lines.append(f"A 最弱{weak_a}恰是 B 最强，B 的稳定输出可能补上 A 的缺口")
    if weak_b == strong_a:
        comp_lines.append(f"B 最弱{weak_b}恰是 A 最强，A 的稳定输出可能补上 B 的缺口")
    if not comp_lines:
        comp_lines.append(
            f"A 强弱：{a['wuxing']['strongest']}/{a['wuxing']['weakest']}；"
            f"B 强弱：{b['wuxing']['strongest']}/{b['wuxing']['weakest']}，互补关系不明显"
        )
    axes.append(axis("五行互补", "偏合" if len(comp_lines) == 2 else "中性",
                     "；".join(comp_lines) + "（基于简化计数，仅作提示）", "低"))

    # 当前流年交集
    cur = next(iter(a.get("liunian", [])), None)
    if cur:
        b_cur = next((y for y in b.get("liunian", []) if y["year"] == cur["year"]), None)
        if b_cur:
            rel = branch_relation(cur["ganzhi"][1], b_cur["ganzhi"][1])
            axes.append(axis("同年流年", level_for(rel),
                             f"{cur['year']} 年 A 行{cur['ganzhi']}、B 行{b_cur['ganzhi']}，地支{rel}。"
                             f"只说明“同一年的外部主题是否同频”，不预测吉凶。", "低"))

    stars = {
        "a": spouse_star_count(a, a["input"]["gender"]),
        "b": spouse_star_count(b, b["input"]["gender"]),
    }
    axes.append(axis("配偶星出现", "信息不足",
                     f"A：{stars['a']['label']} 出现 {stars['a']['count']} 处；"
                     f"B：{stars['b']['label']} 出现 {stars['b']['count']} 处。"
                     f"不同流派对“多寡”的解释差异极大，只作为“择偶偏好来自哪里”的提问角度。",
                     "低"))

    tally = {k: sum(1 for x in axes if x["level"] == k) for k in ("偏合", "中性", "需磨合", "信息不足")}
    return {
        "schema": "suanming.hepan.v1",
        "a": {"name": a.get("name", "A"), "pillars": [pa[k]["ganzhi"] for k in ("year", "month", "day", "time")],
              "day_master": f"{a['day_master']['gan']}{dm_a}"},
        "b": {"name": b.get("name", "B"), "pillars": [pb[k]["ganzhi"] for k in ("year", "month", "day", "time")],
              "day_master": f"{b['day_master']['gan']}{dm_b}"},
        "axes": axes,
        "tally": tally,
        "framing": (
            "合盘只提供提问角度：它不预测两个人能不能成，也不评价谁配不上谁。"
            "任何结论都必须回到可观察的互动（主动、兑现、边界、冲突修复）。"
        ),
        "disclaimer": paipan.DISCLAIMER,
    }


def load_chart(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="双人合盘（维度对照，不给总分）")
    ap.add_argument("--a-json", help="A 的 paipan JSON 文件")
    ap.add_argument("--b-json", help="B 的 paipan JSON 文件")
    ap.add_argument("--a-birth"); ap.add_argument("--a-gender", choices=["male", "female"])
    ap.add_argument("--a-city"); ap.add_argument("--a-longitude", type=float)
    ap.add_argument("--b-birth"); ap.add_argument("--b-gender", choices=["male", "female"])
    ap.add_argument("--b-city"); ap.add_argument("--b-longitude", type=float)
    ap.add_argument("--tz", type=float, default=8.0)
    ap.add_argument("--dst", default="auto", choices=["auto", "on", "off"])
    ap.add_argument("--late-zi", dest="late_zi", default="next_day", choices=["next_day", "same_day"])
    args = ap.parse_args(argv)

    try:
        if args.a_json and args.b_json:
            a, b = load_chart(args.a_json), load_chart(args.b_json)
        else:
            if not (args.a_birth and args.a_gender and args.b_birth and args.b_gender):
                ap.error("要么给 --a-json/--b-json，要么给两边的 --birth/--gender/--city")
            la, _ = solartime.resolve_longitude(args.a_city, args.a_longitude)
            lb, _ = solartime.resolve_longitude(args.b_city, args.b_longitude)
            a = paipan.chart(paipan.parse_birth(args.a_birth), args.a_gender, la,
                             args.tz, args.dst, args.late_zi)
            b = paipan.chart(paipan.parse_birth(args.b_birth), args.b_gender, lb,
                             args.tz, args.dst, args.late_zi)
        print(json.dumps(compare(a, b), ensure_ascii=False, indent=2))
    except (ValueError, SystemExit) as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


