"""真太阳时校正：夏令时、时区、经度差、均时差。

设计取舍（对应调研结论）：
- 不引入天文库。均时差用 NOAA 简化公式（精度约 ±20 秒，远小于命理使用的时辰粒度）。
- 时区、经度、是否夏令时全部显式传入，绝不读取系统本地时间。
- 1986–1991 中国夏令时表内置，可被 `--dst auto|on|off` 覆盖。
"""

from __future__ import annotations

import math
from datetime import datetime, timedelta, timezone

# 中国 1986–1991 年夏令时区间（含首尾日，切换时刻 02:00，时钟拨快 1 小时）。
# 来源：国务院 1986 年《关于实行夏时制的通知》及历年调整公告。
CN_DST_PERIODS = {
    1986: ((5, 4), (9, 14)),
    1987: ((4, 12), (9, 13)),
    1988: ((4, 10), (9, 11)),
    1989: ((4, 16), (9, 17)),
    1990: ((4, 15), (9, 16)),
    1991: ((4, 14), (9, 15)),
}

# 常用城市经度（东经为正）。只为省去用户查经度，不构成地理数据库。
CITY_LONGITUDE = {
    "北京": 116.407, "上海": 121.474, "广州": 113.264, "深圳": 114.058,
    "天津": 117.201, "重庆": 106.551, "成都": 104.066, "杭州": 120.155,
    "南京": 118.797, "苏州": 120.585, "武汉": 114.305, "西安": 108.940,
    "郑州": 113.625, "长沙": 112.939, "济南": 117.120, "青岛": 120.383,
    "沈阳": 123.431, "哈尔滨": 126.535, "大连": 121.615, "长春": 125.324,
    "福州": 119.296, "厦门": 118.089, "南昌": 115.858, "合肥": 117.227,
    "昆明": 102.833, "贵阳": 106.630, "南宁": 108.367, "海口": 110.199,
    "太原": 112.549, "石家庄": 114.502, "兰州": 103.834, "乌鲁木齐": 87.617,
    "呼和浩特": 111.751, "银川": 106.231, "西宁": 101.778, "拉萨": 91.117,
    "香港": 114.174, "澳门": 113.543, "台北": 121.565, "新加坡": 103.820,
    "东京": 139.692, "首尔": 126.978, "洛杉矶": -118.244, "纽约": -74.006,
    "旧金山": -122.419, "伦敦": -0.128, "悉尼": 151.209,
}


def _is_cn_dst(dt: datetime) -> bool:
    period = CN_DST_PERIODS.get(dt.year)
    if not period:
        return False
    (m1, d1), (m2, d2) = period
    start = datetime(dt.year, m1, d1, 2, 0)
    end = datetime(dt.year, m2, d2, 2, 0)
    return start <= dt < end


def dst_minutes(dt_local: datetime, mode: str = "auto") -> int:
    """返回钟表时间需要扣除的夏令时分钟数。

    mode: "auto" 按内置中国夏时制表判断；"on" 强制按 60 分钟处理；"off" 不处理。
    """
    if mode == "off":
        return 0
    if mode == "on":
        return 60
    if mode != "auto":
        raise ValueError(f"未知 dst 模式: {mode}")
    return 60 if _is_cn_dst(dt_local) else 0


def equation_of_time_minutes(dt_utc: datetime) -> float:
    """均时差（真太阳时 − 平太阳时），NOAA 简化公式，返回分钟。"""
    day_of_year = dt_utc.timetuple().tm_yday
    hour = dt_utc.hour + dt_utc.minute / 60 + dt_utc.second / 3600
    gamma = 2 * math.pi / 365 * (day_of_year - 1 + (hour - 12) / 24)
    eot = 229.18 * (
        0.000075
        + 0.001868 * math.cos(gamma)
        - 0.032077 * math.sin(gamma)
        - 0.014615 * math.cos(2 * gamma)
        - 0.040849 * math.sin(2 * gamma)
    )
    return eot


def true_solar_time(
    clock: datetime,
    longitude: float,
    tz_hours: float = 8.0,
    dst_mode: str = "auto",
) -> dict:
    """把用户提供的钟表时间换算为真太阳时。

    返回调整明细，便于在输出里逐项展示（可复核，而不是黑箱）。
    """
    dst = dst_minutes(clock, dst_mode)
    standard = clock - timedelta(minutes=dst)
    lon_corr = (longitude - tz_hours * 15.0) * 4.0  # 每度 4 分钟
    # 均时差按 UTC 时刻计算；钟表时间已按标准时区归一到 UTC。
    utc = standard - timedelta(hours=tz_hours)
    eot = equation_of_time_minutes(utc)
    true_solar = standard + timedelta(minutes=lon_corr + eot)
    return {
        "clock": clock,
        "dst_minutes": dst,
        "standard_time": standard,
        "longitude_correction_minutes": round(lon_corr, 2),
        "eot_minutes": round(eot, 2),
        "true_solar": true_solar,
        "tz_hours": tz_hours,
        "longitude": longitude,
        "utc": utc,
    }


def resolve_longitude(city: str | None, longitude: float | None) -> tuple[float, str]:
    """城市名或经度，二者至少给一个。"""
    if longitude is not None:
        if not -180 <= longitude <= 180:
            raise ValueError("经度必须在 -180 到 180 之间")
        return float(longitude), "explicit"
    if not city:
        raise ValueError("需要城市或经度（城市名见 solartime.CITY_LONGITUDE）")
    for name, lon in CITY_LONGITUDE.items():
        if name in city:
            return lon, f"city:{name}"
    raise ValueError(f"未知城市 {city!r}，请改用 --longitude 传入东经度数")


def shichen_index(dt: datetime) -> int:
    """时辰序号：0=子(23:00–00:59), 1=丑 ... 11=亥。"""
    hour = dt.hour
    return ((hour + 1) // 2) % 12


def shichen_name(index: int) -> str:
    names = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
    return names[index % 12]


def boundary_distance_minutes(dt: datetime) -> float:
    """距最近时辰交界的分钟数（用于提示“边界风险”）。"""
    minutes = dt.hour * 60 + dt.minute + dt.second / 60
    offset = (minutes + 60) % 120  # 相对 23:00 起每 2 小时一个边界
    return min(offset, 120 - offset)


def utc_from_clock(clock: datetime, tz_hours: float) -> datetime:
    return clock.replace(tzinfo=timezone(timedelta(hours=tz_hours))).astimezone(timezone.utc)
