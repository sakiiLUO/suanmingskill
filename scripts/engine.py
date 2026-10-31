"""历算引擎定位：优先使用随 skill 打包的 vendor/，其次使用已安装的 lunar-python。

设计取舍：不为了“零依赖”重写历算。lunar-python（MIT，纯 Python）是经过验证的实现，
我们只在它之上写规则层（真太阳时、晚子时、五行计数、合盘），并通过 tests 锁住行为。
"""

from __future__ import annotations

import sys
from pathlib import Path

VENDOR_HINT = "lunar-python (MIT, https://github.com/6tail/lunar-python)"


def _candidate_roots() -> list[Path]:
    here = Path(__file__).resolve()
    roots = [
        here.parents[1] / "vendor",  # skill/suanming/vendor
        here.parents[2] / "vendor",  # repo 根 vendor（本地开发）
    ]
    return roots


def ensure_engine() -> str:
    """确保 lunar_python 可导入，返回实际来源描述。"""
    try:
        import lunar_python  # noqa: F401

        return "installed:" + getattr(lunar_python, "__file__", "")
    except ImportError:
        pass
    for root in _candidate_roots():
        if (root / "lunar_python").is_dir():
            sys.path.insert(0, str(root))
            try:
                import lunar_python  # noqa: F401

                return "vendor:" + str(root)
            except ImportError:  # pragma: no cover
                sys.path.pop(0)
    raise SystemExit(
        "缺少历算依赖 lunar-python。安装方式：\n"
        "  python -m pip install lunar-python\n"
        "或把随包 vendor/ 目录放回 skill 根目录（离线可用）。\n"
        f"依赖信息：{VENDOR_HINT}"
    )
