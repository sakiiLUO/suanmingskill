"""排盘 CLI：公历生日 → 真太阳时校正 → 四柱/十神/大运/流年 → 结构化 JSON。

用法示例：
  python scripts/paipan.py --birth "1995-08-17 14:30" --gender male --city 杭州
  python scripts/paipan.py --birth "2000-01-01 00:30" --gender female --longitude 116.4 --format brief
  python scripts/paipan.py --birth "1990-06-15 09:10" --gender male --city 上海 --dst auto

输出是一份“事实层 + 边界条件”的 JSON，解读交给 SKILL.md 的流程，不在这里写断语。
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import engine  # noqa: E402
import solartime  # noqa: E402

SCHEMA = "suanming.paipan.v1"
DISCLAIMER = (
    "文化娱乐与自我反思用途，不构成医疗、心理、法律、投资或人生决策建议；"
    "命理不是预测事实，结论仅为可讨论的假设。"
)

HIDDEN_WEIGHTS = (1.0, 0.5, 0.3)  # 本气 / 中气 / 余气
WUXING_OF_GAN = {
    "甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土",
    "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水",
}
WUXING_OF_ZHI = {
    "子": "水", "丑": "土", "寅": "木", "卯": "木", "辰": "土", "巳": "火",
    "午": "火", "未": "土", "申": "金", "酉": "金", "戌": "土", "亥": "水",
}
SHENG = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}  # A 生 B
KE = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}  # A 克 B


def parse_birth(text: str) -> datetime:
    text = text.strip().replace("/", "-").replace("T", " ")
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d %H", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    raise argparse.ArgumentTypeError(f"无法解析生日 {text!r}，请用 'YYYY-MM-DD HH:MM'")


def pillar_block(eight, key: str) -> dict:
    cap = key.capitalize()
    get = lambda name: getattr(eight, f"get{cap}{name}")()  # noqa: E731
    hidden = get("HideGan")
    return {
        "ganzhi": get(""),
        "gan": get("Gan"),
        "zhi": get("Zhi"),
        "hidden_gan": hidden,
        "wuxing": get("WuXing"),
        "nayin": get("NaYin"),
        "shishen_gan": get("ShiShenGan"),
        "shishen_zhi": get("ShiShenZhi"),
        "dishi": get("DiShi"),
        "xunkong": get("XunKong"),
    }


def wuxing_profile(eight) -> dict:
    """简化五行计数：天干计 1.0，地支藏干按 1.0/0.5/0.3 加权。

    明确标注为“计数”，不等于专业旺衰/格局判定。
    """
    counts = {k: 0.0 for k in "木火土金水"}
    for key in ("Year", "Month", "Day", "Time"):
        gan = getattr(eight, f"get{key}Gan")()
        hidden = getattr(eight, f"get{key}HideGan")()
        counts[WUXING_OF_GAN[gan]] += 1.0
        for i, h in enumerate(hidden):
            counts[WUXING_OF_GAN[h]] += HIDDEN_WEIGHTS[min(i, len(HIDDEN_WEIGHTS) - 1)]
    total = sum(counts.values()) or 1.0
    return {
        "counts": {k: round(v, 2) for k, v in counts.items()},
        "percent": {k: round(v / total * 100, 1) for k, v in counts.items()},
        "strongest": sorted(counts, key=counts.get, reverse=True)[0],
        "weakest": sorted(counts, key=counts.get)[0],
        "note": "按天干 1.0、藏干本气 1.0 / 中气 0.5 / 余气 0.3 加权，仅作强弱提示，非专业旺衰定论。",
    }


def day_master_hint(eight) -> dict:
    gan = eight.getDayGan()
    wx = WUXING_OF_GAN[gan]
    month_zhi_wx = WUXING_OF_ZHI[eight.getMonthZhi()]
    relation = "同气" if month_zhi_wx == wx else ("得生" if SHENG.get(month_zhi_wx) == wx else "被克/泄")
    return {
        "gan": gan,
        "wuxing": wx,
        "yin_yang": "阳" if gan in "甲丙戊庚壬" else "阴",
        "month_branch_wuxing": month_zhi_wx,
        "month_relation": relation,
        "note": "“得令”仅按月支本气判断，是讨论起点，不是结论。",
    }


def build_chart(birth_solar: datetime, gender: str) -> dict:
    from lunar_python import Solar

    lunar = Solar.fromYmdHms(
        birth_solar.year, birth_solar.month, birth_solar.day,
        birth_solar.hour, birth_solar.minute, birth_solar.second,
    ).getLunar()
    eight = lunar.getEightChar()
    gender_code = 1 if gender == "male" else 0
    yun = eight.getYun(gender_code)

    dayun = []
    for d in yun.getDaYun()[1:]:  # 第 0 个是起运前的小运段
        dayun.append({
            "ganzhi": d.getGanZhi(),
            "start_year": d.getStartYear(),
            "end_year": d.getEndYear(),
            "start_age": d.getStartAge(),
            "end_age": d.getEndAge(),
        })

    current_year = datetime.now().year
    liunian = []
    for d in yun.getDaYun()[1:]:
        for n in d.getLiuNian():
            if current_year - 1 <= n.getYear() <= current_year + 5:
                liunian.append({
                    "year": n.getYear(),
                    "ganzhi": n.getGanZhi(),
                    "age": n.getAge(),
                    "shishen_gan": n.getShiShenGan() if hasattr(n, "getShiShenGan") else None,
                })

    jieqi = lunar.getJieQiTable()
    return {
        "lunar": {
            "text": lunar.toString(),
            "year": lunar.getYear(),
            "month": lunar.getMonth(),
            "day": lunar.getDay(),
            "is_leap_month": lunar.getMonth() < 0,
        },
        "pillars": {k: pillar_block(eight, k) for k in ("year", "month", "day", "time")},
        "day_master": day_master_hint(eight),
        "wuxing": wuxing_profile(eight),
        "aux": {
            "taiyuan": eight.getTaiYuan(),
            "minggong": eight.getMingGong(),
            "shengong": eight.getShenGong(),
        },
        "yun": {
            "gender": gender,
            "start_solar": yun.getStartSolar().toYmd(),
            "start_age_text": f"{yun.getStartYear()}年{yun.getStartMonth()}个月{yun.getStartDay()}天起运",
            "dayun": dayun,
        },
        "liunian": liunian,
        "jieqi": {
            "prev_jie": {"name": lunar.getPrevJie().getName(),
                          "at": lunar.getPrevJie().getSolar().toYmdHms()},
            "next_jie": {"name": lunar.getNextJie().getName(),
                          "at": lunar.getNextJie().getSolar().toYmdHms()},
            "lichun_this_lunar_year": jieqi["立春"].toYmdHms() if "立春" in jieqi else None,
        },
    }


def chart(
    birth: datetime,
    gender: str,
    longitude: float,
    tz_hours: float = 8.0,
    dst_mode: str = "auto",
    late_zi: str = "next_day",
) -> dict:
    engine.ensure_engine()
    corr = solartime.true_solar_time(birth, longitude, tz_hours, dst_mode)
    solar = corr["true_solar"]
    warnings: list[str] = []

    if corr["dst_minutes"]:
        warnings.append(
            f"出生日期落在 1986–1991 中国夏令时区间内，钟表时间已回拨 {corr['dst_minutes']} 分钟。"
        )
    if abs(corr["longitude_correction_minutes"]) > 30:
        warnings.append(
            f"经度差 {corr['longitude_correction_minutes']:.1f} 分钟较大，时柱对边界更敏感，建议核对出生地。"
        )

    late_zi_applied = False
    if solar.hour >= 23:
        if late_zi == "next_day":
            solar = solar + timedelta(days=1)
            solar = solar.replace(hour=0, minute=solar.minute, second=solar.second)
            late_zi_applied = True
            warnings.append("晚子时按“子时换日”处理：日柱取次日，时柱仍为子时（可用 --late-zi same_day 关闭）。")
        else:
            warnings.append("晚子时按“不换日”处理，日柱仍为当天（不同流派口径不同，需在结论中说明）。")

    dist = solartime.boundary_distance_minutes(solar)
    if dist <= 10:
        warnings.append(
            f"出生时间距时辰交界仅 {dist:.0f} 分钟，时柱存在换柱风险；请复核出生时间或注明不确定性。"
        )

    data = build_chart(solar, gender)
    data.update({
        "schema": SCHEMA,
        "input": {
            "birth_clock": birth.strftime("%Y-%m-%d %H:%M"),
            "gender": gender,
            "tz_hours": tz_hours,
            "dst_mode": dst_mode,
            "late_zi": late_zi,
            "longitude": longitude,
        },
        "time_correction": {
            "clock": corr["clock"].strftime("%Y-%m-%d %H:%M"),
            "dst_minutes": corr["dst_minutes"],
            "standard_time": corr["standard_time"].strftime("%Y-%m-%d %H:%M"),
            "longitude_correction_minutes": corr["longitude_correction_minutes"],
            "eot_minutes": corr["eot_minutes"],
            "true_solar_time": solar.strftime("%Y-%m-%d %H:%M"),
            "late_zi_applied": late_zi_applied,
            "shichen": solartime.shichen_name(solartime.shichen_index(solar)),
        },
        "warnings": warnings,
        "disclaimer": DISCLAIMER,
    })
    return data


def to_brief(d: dict) -> str:
    p = d["pillars"]
    lines = [
        f"真太阳时 {d['time_correction']['true_solar_time']}（{d['time_correction']['shichen']}时，"
        f"经度差 {d['time_correction']['longitude_correction_minutes']:+.1f} 分，均时差 {d['time_correction']['eot_minutes']:+.1f} 分）",
        f"四柱：{p['year']['ganzhi']} {p['month']['ganzhi']} {p['day']['ganzhi']} {p['time']['ganzhi']}",
        f"日主：{d['day_master']['gan']}{d['day_master']['wuxing']}（{d['day_master']['yin_yang']}），月支{d['day_master']['month_branch_wuxing']}，{d['day_master']['month_relation']}",
        "十神：" + " / ".join(
            f"{k}柱{p[k]['shishen_gan']}" for k in ("year", "month", "day")
        ) + f" / 时柱{p['time']['shishen_gan']}",
        f"五行占比：{d['wuxing']['percent']}（最强 {d['wuxing']['strongest']}，最弱 {d['wuxing']['weakest']}）",
        f"大运：{d['yun']['start_solar']} 起运；" + "、".join(
            f"{x['start_age']}–{x['end_age']}岁{x['ganzhi']}" for x in d["yun"]["dayun"][:5]
        ),
    ]
    if d["liunian"]:
        lines.append("流年：" + "、".join(f"{x['year']}{x['ganzhi']}" for x in d["liunian"][:5]))
    if d["warnings"]:
        lines.append("边界提示：" + "；".join(d["warnings"]))
    lines.append("口径：" + d["disclaimer"])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="八字排盘（真太阳时校正 + 结构化输出）")
    ap.add_argument("--birth", required=True, help="公历出生时间 'YYYY-MM-DD HH:MM'")
    ap.add_argument("--gender", required=True, choices=["male", "female"])
    ap.add_argument("--city", help="出生城市（内置常用城市经度表）")
    ap.add_argument("--longitude", type=float, help="出生地经度（东经为正），与 --city 二选一")
    ap.add_argument("--tz", type=float, default=8.0, help="出生地时区偏移小时数，默认 8")
    ap.add_argument("--dst", default="auto", choices=["auto", "on", "off"],
                    help="夏令时：auto 按 1986–1991 中国夏时制表，on 强制扣 60 分钟，off 不处理")
    ap.add_argument("--late-zi", dest="late_zi", default="next_day", choices=["next_day", "same_day"])
    ap.add_argument("--format", default="json", choices=["json", "brief"])
    ap.add_argument("--save", help="把 JSON 结果另存到指定路径（供 hepan.py 使用）")
    args = ap.parse_args(argv)

    try:
        birth = parse_birth(args.birth)
        longitude, lon_src = solartime.resolve_longitude(args.city, args.longitude)
        data = chart(birth, args.gender, longitude, args.tz, args.dst, args.late_zi)
        data["input"]["longitude_source"] = lon_src
    except (ValueError, SystemExit, argparse.ArgumentTypeError) as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 2

    if args.save:
        out = Path(args.save)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    if args.format == "brief":
        print(to_brief(data))
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

