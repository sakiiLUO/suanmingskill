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

## iztro（紫微斗数引擎）

- 项目：https://github.com/SylarLong/iztro
- 版本：2.6.3
- 许可证：MIT
- 用途：紫微斗数排盘（十二宫、主星/辅星、四化、大限、流年）。
- 说明：`vendor/iztro/` 为 `npm install` 后的未修改依赖树（含 dayjs / i18next / lunar-lite / lunar-typescript，均为 MIT），保留各包自带 LICENSE。本仓库只通过 `scripts/ziwei_bridge.cjs` 调用其公开 API，未复制其源码。

## 六爻

- 规则依据：京房八宫卦序、纳甲、世应、六亲六神、月建日辰旬空等**公有领域传统规则**（可参考《卜筮正宗》《增删卜易》）。
- 实现：`scripts/liuyao.py` 为原创实现，未复制任何第三方代码；规则表由 `tests/test_liuyao.py` 校验（八宫卦序、纳甲、六亲、六神、64 卦唯一性）。
- 未采用 divicast（MIT）：其要求 Python 3.12 + pydantic/rich/tyme4py，与本项目「Python 3.10+、零第三方运行时依赖」的约束冲突；仅借鉴其「盘面 JSON 化、不做吉凶评分」的设计思路。
- 未采用 `ziwei`（PyPI，MIT）：其依赖原生 wheel（celestial-calendar），跨平台安装风险高于 Node 方案；仅列入参考。