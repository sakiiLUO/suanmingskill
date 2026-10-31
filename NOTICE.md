# NOTICE — 第三方依赖与许可

本 skill 的计算层依赖以下开源项目。代码未经修改，以原样打包或通过 pip 安装使用。

## lunar-python

- 项目：https://github.com/6tail/lunar-python
- 版本：1.4.8
- 许可证：MIT License
- 用途：公历/农历转换、二十四节气、干支四柱、十神、大运流年计算。
- 说明：`vendor/` 目录为其未修改的发行包副本（含 `lunar_python-1.4.8.dist-info`，其中包含原始 LICENSE）。分发本 skill 时请保留该目录。

## 未采用但参考过的设计

- [yuangu/sxtwl_cpp](https://github.com/yuangu/sxtwl_cpp)（BSD-3-Clause）：天文历算底座，节气可到分钟。本 skill 未打包，理由见 `docs/01-调研-同类开源项目对比.md`。若你的平台能装，可作为交叉校验（`pip install sxtwl`）。
- [SylarLong/iztro](https://github.com/SylarLong/iztro)（MIT）：紫微斗数排盘，本 skill v1 不包含。
- [Renhuai123/ziwei-doushu](https://github.com/Renhuai123/ziwei-doushu)：仅借鉴其 README 中记录的历法坑清单（真太阳时、1986–1991 夏令时、闰月口径、晚子时），未使用其代码或语料；其倪师讲授内容为 CC BY-NC-SA 4.0，禁止商用，本仓库未包含任何该目录内容。

## 本 skill 原创部分

SKILL.md、references/、scripts/solartime.py、scripts/paipan.py、scripts/hepan.py、scripts/archive.py、scripts/validate_skill.py、tests/ 为本项目原创（建议以 MIT 发布；发布前请按你的实际意愿确认许可证）。

古汉语术语与命理常识属公有领域；本仓库不包含任何现代点校本、他人断语库或付费课程内容。
