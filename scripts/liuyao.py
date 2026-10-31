"""六爻排盘 CLI（纯标准库，无第三方依赖）。

为什么自研：现成的六爻库（如 divicast，MIT）依赖 pydantic/rich/tyme4py 且要求 Python 3.12，
与本项目「3.10+、离线、零运行时依赖」的约束冲突；六爻的核心是公开的传统规则表
（八卦纳甲、京房八宫世应、六亲六神、旬空），规模小、可逐条校验，因此这里只实现规则层，
并用测试锁住（八宫卦序、64 卦唯一性、纳甲顺序、世应位置）。

用法：
  # 摇卦结果（自下而上 6 个爻：6 老阴、7 少阳、8 少阴、9 老阳）
  python scripts/liuyao.py --lines 7,8,9,7,6,8 --date "2026-10-31 19:40" --question "这次合作能成吗"

  # 时间起卦（梅花式，无铜钱时用）
  python scripts/liuyao.py --method time --date "2026-10-31 19:40" --question "..."
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import engine  # noqa: E402

SCHEMA = "suanming.liuyao.v1"
DISCLAIMER = (
    "文化娱乐与自我反思用途。六爻属传统解释框架，不是预测事实；"
    "不用于医疗、法律、投资或人身安全决策。"
)

# 八卦：卦名 → (自下而上三爻阴阳, 先天数, 五行, 内卦纳甲三爻, 外卦纳甲三爻)
TRIGRAMS = {
    "乾": {"lines": (1, 1, 1), "number": 1, "element": "金",
           "inner": ("甲子", "甲寅", "甲辰"), "outer": ("壬午", "壬申", "壬戌")},
    "兑": {"lines": (1, 1, 0), "number": 2, "element": "金",
           "inner": ("丁巳", "丁卯", "丁丑"), "outer": ("丁亥", "丁酉", "丁未")},
    "离": {"lines": (1, 0, 1), "number": 3, "element": "火",
           "inner": ("己卯", "己丑", "己亥"), "outer": ("己酉", "己未", "己巳")},
    "震": {"lines": (1, 0, 0), "number": 4, "element": "木",
           "inner": ("庚子", "庚寅", "庚辰"), "outer": ("庚午", "庚申", "庚戌")},
    "巽": {"lines": (0, 1, 1), "number": 5, "element": "木",
           "inner": ("辛丑", "辛亥", "辛酉"), "outer": ("辛未", "辛巳", "辛卯")},
    "坎": {"lines": (0, 1, 0), "number": 6, "element": "水",
           "inner": ("戊寅", "戊辰", "戊午"), "outer": ("戊申", "戊戌", "戊子")},
    "艮": {"lines": (0, 0, 1), "number": 7, "element": "土",
           "inner": ("丙辰", "丙午", "丙申"), "outer": ("丙戌", "丙子", "丙寅")},
    "坤": {"lines": (0, 0, 0), "number": 8, "element": "土",
           "inner": ("乙未", "乙巳", "乙卯"), "outer": ("癸丑", "癸亥", "癸酉")},
}

# 64 卦名：HEXAGRAM_NAMES[(上卦, 下卦)]
HEXAGRAM_NAMES = {
    ("乾", "乾"): "乾为天", ("乾", "兑"): "天泽履", ("乾", "离"): "天火同人",
    ("乾", "震"): "天雷无妄", ("乾", "巽"): "天风姤", ("乾", "坎"): "天水讼",
    ("乾", "艮"): "天山遁", ("乾", "坤"): "天地否",
    ("兑", "乾"): "泽天夬", ("兑", "兑"): "兑为泽", ("兑", "离"): "泽火革",
    ("兑", "震"): "泽雷随", ("兑", "巽"): "泽风大过", ("兑", "坎"): "泽水困",
    ("兑", "艮"): "泽山咸", ("兑", "坤"): "泽地萃",
    ("离", "乾"): "火天大有", ("离", "兑"): "火泽睽", ("离", "离"): "离为火",
    ("离", "震"): "火雷噬嗑", ("离", "巽"): "火风鼎", ("离", "坎"): "火水未济",
    ("离", "艮"): "火山旅", ("离", "坤"): "火地晋",
    ("震", "乾"): "雷天大壮", ("震", "兑"): "雷泽归妹", ("震", "离"): "雷火丰",
    ("震", "震"): "震为雷", ("震", "巽"): "雷风恒", ("震", "坎"): "雷水解",
    ("震", "艮"): "雷山小过", ("震", "坤"): "雷地豫",
    ("巽", "乾"): "风天小畜", ("巽", "兑"): "风泽中孚", ("巽", "离"): "风火家人",
    ("巽", "震"): "风雷益", ("巽", "巽"): "巽为风", ("巽", "坎"): "风水涣",
    ("巽", "艮"): "风山渐", ("巽", "坤"): "风地观",
    ("坎", "乾"): "水天需", ("坎", "兑"): "水泽节", ("坎", "离"): "水火既济",
    ("坎", "震"): "水雷屯", ("坎", "巽"): "水风井", ("坎", "坎"): "坎为水",
    ("坎", "艮"): "水山蹇", ("坎", "坤"): "水地比",
    ("艮", "乾"): "山天大畜", ("艮", "兑"): "山泽损", ("艮", "离"): "山火贲",
    ("艮", "震"): "山雷颐", ("艮", "巽"): "山风蛊", ("艮", "坎"): "山水蒙",
    ("艮", "艮"): "艮为山", ("艮", "坤"): "山地剥",
    ("坤", "乾"): "地天泰", ("坤", "兑"): "地泽临", ("坤", "离"): "地火明夷",
    ("坤", "震"): "地雷复", ("坤", "巽"): "地风升", ("坤", "坎"): "地水师",
    ("坤", "艮"): "地山谦", ("坤", "坤"): "坤为地",
}

# 京房八宫：宫名 → 五行
PALACE_ELEMENT = {"乾": "金", "兑": "金", "离": "火", "震": "木",
                  "巽": "木", "坎": "水", "艮": "土", "坤": "土"}
# 八宫各卦的世爻位置（初爻=1 … 上爻=6）
PALACE_SHI = {"本宫": 6, "一世": 1, "二世": 2, "三世": 3, "四世": 4, "五世": 5, "游魂": 4, "归魂": 3}
PALACE_STAGE_NAMES = ["本宫", "一世", "二世", "三世", "四世", "五世", "游魂", "归魂"]

ELEMENTS = ("金", "木", "水", "火", "土")
SHENG = {"金": "水", "水": "木", "木": "火", "火": "土", "土": "金"}
KE = {"金": "木", "木": "土", "土": "水", "水": "火", "火": "金"}
BRANCH_ELEMENT = {
    "子": "水", "丑": "土", "寅": "木", "卯": "木", "辰": "土", "巳": "火",
    "午": "火", "未": "土", "申": "金", "酉": "金", "戌": "土", "亥": "水",
}
ZHI = "子丑寅卯辰巳午未申酉戌亥"
GAN = "甲乙丙丁戊己庚辛壬癸"
LIUSHEN = ["青龙", "朱雀", "勾陈", "螣蛇", "白虎", "玄武"]
DAY_GAN_LIUSHEN_START = {"甲": 0, "乙": 0, "丙": 1, "丁": 1, "戊": 2,
                         "己": 3, "庚": 4, "辛": 4, "壬": 5, "癸": 5}


def trigram_of(lines: tuple[int, int, int]) -> str:
    for name, info in TRIGRAMS.items():
        if info["lines"] == lines:
            return name
    raise ValueError(f"不是合法八卦：{lines}")


def hexagram_name(upper: str, lower: str) -> str:
    return HEXAGRAM_NAMES[(upper, lower)]


def palace_of(upper: str, lower: str) -> tuple[str, str, int]:
    """返回 (宫名, 世应阶段, 世爻位置)。用京房八宫生成法反查。"""
    target = (upper, lower)
    for palace, info in PALACE_ELEMENT.items():
        seq = palace_sequence(palace)
        for stage, (u, l) in zip(PALACE_STAGE_NAMES, seq):
            if (u, l) == target:
                return palace, stage, PALACE_SHI[stage]
    raise ValueError(f"找不到宫位：{target}")


def palace_sequence(palace: str) -> list[tuple[str, str]]:
    """按京房八宫规则生成 8 个卦的 (上卦, 下卦)。"""
    base = TRIGRAMS[palace]["lines"]  # 本宫纯卦
    lines = [list(base) * 2]  # 6 爻，自下而上
    seq = [base * 2]
    for count in range(1, 6):  # 一世…五世：依次变初爻到五爻
        current = list(seq[-1])
        current[count - 1] = 1 - current[count - 1]
        seq.append(tuple(current))
    # 游魂：在五世基础上再变第四爻
    youhun = list(seq[-1])
    youhun[3] = 1 - youhun[3]
    seq.append(tuple(youhun))
    # 归魂：把游魂的内卦还原为本宫内卦
    guihun = list(seq[-1])
    guihun[0:3] = list(base)
    seq.append(tuple(guihun))
    return [(trigram_of(tuple(l[3:6])), trigram_of(tuple(l[0:3]))) for l in seq[1:]] and \
           [(trigram_of(tuple(l[3:6])), trigram_of(tuple(l[0:3]))) for l in seq]


def six_relation(palace_el: str, line_el: str) -> str:
    if line_el == palace_el:
        return "兄弟"
    if SHENG[line_el] == palace_el:
        return "父母"
    if SHENG[palace_el] == line_el:
        return "子孙"
    if KE[line_el] == palace_el:
        return "官鬼"
    if KE[palace_el] == line_el:
        return "妻财"
    raise ValueError("五行关系异常")


def day_ganzhi(dt: datetime) -> tuple[str, str]:
    engine.ensure_engine()
    from lunar_python import Solar

    lunar = Solar.fromYmdHms(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second).getLunar()
    eight = lunar.getEightChar()
    return eight.getDayGan(), eight.getDayZhi()


def xunkong(day_gan: str, day_zhi: str) -> list[str]:
    """旬空：按日柱所在的六十甲子旬，取该旬缺失的两个地支。"""
    g = GAN.index(day_gan)
    z = ZHI.index(day_zhi)
    # 六十甲子序号
    for i in range(60):
        if i % 10 == g and i % 12 == z:
            start = i - g  # 该旬起始序号（甲子起）
            break
    used = {ZHI[(start + k) % 12] for k in range(10)}
    return [zhi for zhi in ZHI if zhi not in used]


def build(
    lines: list[int] | None,
    method: str,
    moment: datetime,
    question: str | None = None,
    moving_override: list[int] | None = None,
) -> dict:
    if method == "time":
        y, mo, d = moment.year, moment.month, moment.day
        # 年支、时支序号（子=1…亥=12），梅花式取数
        year_zhi = ZHI.index(day_ganzhi(moment)[1])  # 占位，下一行用真实年支
        engine.ensure_engine()
        from lunar_python import Solar

        lunar = Solar.fromYmdHms(y, mo, d, moment.hour, moment.minute, 0).getLunar()
        year_zhi_idx = ZHI.index(lunar.getYearZhi())
        hour_zhi_idx = ZHI.index(lunar.getTimeZhi())
        upper_num = (year_zhi_idx + 1 + mo + d) % 8 or 8
        lower_num = (year_zhi_idx + 1 + mo + d + hour_zhi_idx + 1) % 8 or 8
        moving = ((year_zhi_idx + 1 + mo + d + hour_zhi_idx + 1) % 6) or 6
        num_to_name = {info["number"]: name for name, info in TRIGRAMS.items()}
        upper, lower = num_to_name[upper_num], num_to_name[lower_num]
        raw_lines = list(TRIGRAMS[lower]["lines"]) + list(TRIGRAMS[upper]["lines"])
        moving_lines = [moving]
    else:
        if not lines or len(lines) != 6:
            raise ValueError("--lines 需要 6 个值，自下而上，取值 6/7/8/9")
        if any(v not in (6, 7, 8, 9) for v in lines):
            raise ValueError("爻值只能是 6（老阴）、7（少阳）、8（少阴）、9（老阳）")
        moving_lines = [i + 1 for i, v in enumerate(lines) if v in (6, 9)]
        raw_lines = [1 if v in (7, 9) else 0 for v in lines]
        upper = trigram_of(tuple(raw_lines[3:6]))
        lower = trigram_of(tuple(raw_lines[0:3]))
        if moving_override:
            moving_lines = moving_override

    changed = list(raw_lines)
    for pos in moving_lines:
        changed[pos - 1] = 1 - changed[pos - 1]
    changed_upper = trigram_of(tuple(changed[3:6]))
    changed_lower = trigram_of(tuple(changed[0:3]))

    palace, stage, shi = palace_of(upper, lower)
    ying = shi + 3 if shi <= 3 else shi - 3
    palace_el = PALACE_ELEMENT[palace]

    gan, zhi = day_ganzhi(moment)
    start = DAY_GAN_LIUSHEN_START[gan]
    lunar_year_zhi = None
    try:
        from lunar_python import Solar

        lunar = Solar.fromYmdHms(moment.year, moment.month, moment.day, moment.hour, moment.minute, 0).getLunar()
        lunar_year_zhi = lunar.getYearZhi()
        month_zhi = lunar.getMonthZhi()
    except Exception:  # pragma: no cover
        month_zhi = None
    xk = xunkong(gan, zhi)

    line_rows = []
    for i in range(6):
        pos = i + 1  # 自下而上
        is_yang = raw_lines[i] == 1
        na = TRIGRAMS[lower if pos <= 3 else upper]["inner" if pos <= 3 else "outer"][(pos - 1) % 3]
        na_gan, na_zhi = na[0], na[1]
        el = BRANCH_ELEMENT[na_zhi]
        changed_el = None
        if pos in moving_lines:
            cn = TRIGRAMS[changed_lower if pos <= 3 else changed_upper]["inner" if pos <= 3 else "outer"][(pos - 1) % 3]
            changed_el = BRANCH_ELEMENT[cn[1]]
        line_rows.append({
            "position": pos,
            "yang": is_yang,
            "value": lines[i] if lines else (9 if moving_lines == [pos] and is_yang else 8),
            "moving": pos in moving_lines,
            "najia": na,
            "branch_element": el,
            "six_relation": six_relation(palace_el, el),
            "six_relation_changed": six_relation(palace_el, changed_el) if changed_el else None,
            "liu_shen": LIUSHEN[(start + i) % 6],
            "shi_yao": pos == shi,
            "ying_yao": pos == ying,
            "xunkong": na_zhi in xk,
        })

    return {
        "schema": SCHEMA,
        "method": method,
        "question": question,
        "moment": moment.strftime("%Y-%m-%d %H:%M"),
        "day_ganzhi": gan + zhi,
        "month_branch": month_zhi,
        "year_branch": lunar_year_zhi,
        "xunkong": xk,
        "hexagram": {
            "name": hexagram_name(upper, lower),
            "upper": upper,
            "lower": lower,
            "palace": palace,
            "palace_element": palace_el,
            "stage": stage,
            "shi_position": shi,
            "ying_position": ying,
            "lines": line_rows,
        },
        "changed": {
            "name": hexagram_name(changed_upper, changed_lower) if moving_lines else None,
            "upper": changed_upper,
            "lower": changed_lower,
        },
        "moving_lines": moving_lines,
        "disclaimer": DISCLAIMER,
    }


def to_brief(d: dict) -> str:
    h = d["hexagram"]
    lines = [
        f"卦象：{h['name']}（{h['palace']}宫·{h['palace_element']}·{h['stage']}）",
        f"世爻 {h['shi_position']} 爻，应爻 {h['ying_position']} 爻；动爻：{'、'.join(str(x) for x in d['moving_lines']) or '无'}",
        f"日辰 {d['day_ganzhi']}，月建 {d['month_branch'] or '—'}，旬空 {''.join(d['xunkong']) or '—'}",
    ]
    if d["changed"]["name"]:
        lines.append(f"变卦：{d['changed']['name']}")
    for row in d["hexagram"]["lines"]:
        mark = "○" if row["shi_yao"] else ("×" if row["ying_yao"] else " ")
        moving = "→" if row["moving"] else " "
        lines.append(f"{row['position']}{mark}{moving}{'阳' if row['yang'] else '阴'} "
                     f"{row['liu_shen']} {row['six_relation']}{row['najia']}")
    lines.append("口径：" + d["disclaimer"])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="六爻排盘（纯标准库，规则表可校验）")
    ap.add_argument("--lines", help="自下而上 6 个爻值：6 老阴 / 7 少阳 / 8 少阴 / 9 老阳")
    ap.add_argument("--method", default="shake", choices=["shake", "time"], help="shake=摇卦；time=时间起卦")
    ap.add_argument("--date", help="起卦时间 'YYYY-MM-DD HH:MM'，默认现在")
    ap.add_argument("--question", help="所问何事（一句话，便于记录）")
    ap.add_argument("--format", default="json", choices=["json", "brief"])
    ap.add_argument("--save", help="JSON 存到指定路径")
    args = ap.parse_args(argv)

    if args.date:
        try:
            moment = datetime.strptime(args.date.strip().replace("/", "-"), "%Y-%m-%d %H:%M")
        except ValueError:
            print("错误：--date 格式应为 'YYYY-MM-DD HH:MM'", file=sys.stderr)
            return 2
    else:
        moment = datetime.now()

    try:
        lines = [int(x) for x in args.lines.split(",")] if args.lines else None
        data = build(lines, args.method, moment, args.question)
    except (ValueError, SystemExit) as exc:
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
