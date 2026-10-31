# 算命 skill（suanming）

> 一个可以独立使用的**八字排盘与解读** Agent Skill：把盘算准，把话说明白，把边界写死。

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-53%20passing-brightgreen.svg)](#测试)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB.svg)](https://www.python.org/)

---

## 这是什么

一个给 AI Agent 用的 skill（`SKILL.md` + 按需加载的 `references/` + 可离线运行的 Python 脚本）。

**它做的事**：按出生信息排盘 → 处理真太阳时/夏令时/晚子时/节气边界 → 给出「盘面事实 / 边界与不确定 / 2–3 条带证据的假设 / 一个可验证的小动作」。

**它不做的事**：预测生死、诊断疾病、断官司胜负、给投资标的、承诺「改运」。命理在这里是**提问与反思的工具**，不是预测机器。

覆盖领域：性格、事业与职业方向、财运、学业与考试、家庭与代际、身心状态（非医疗）、关系合盘、大运流年的时间窗。

> 关系策略、话术、情绪支持**不在这里**——那部分可选交给 [狗头军师（goutoujunshi）](https://github.com/shengjidaguai-china/goutoujunshi)。本 skill 默认独立可用，不需要它。

## 输出长什么样

```text
盘面事实：真太阳时 1995-08-17 14:26，四柱 乙亥 甲申 庚辰 癸未，日主庚金，月令申金；
          当前行辛巳大运（2018–2027），2026 流年丙午。
边界与不确定：出生时间距未时/申时交界较远，时柱稳定；未命中 1986–1991 夏令时。
假设（不是定论）：日主庚金、月令申金，通常被解释为遇事先自己扛、不爱示弱。
反向可能：也可能是从小被要求独立形成的习惯，不是天性。
可验证的小动作：回想最近三次压力事件，你是先找人商量还是先自己消化；
              如果都是自己消化，这条就更像你。
以上是解释框架，不是预测。
```

## 安装

**通用方式**：把仓库克隆下来后，目录命名为 `suanming`，放进宿主查找 skill 的目录。

| 宿主 | 目录 |
| --- | --- |
| DSH / DeepSeek Harness | `~/.dsh/skills/suanming/`（或项目内 `<repo>/.dsh/skills/suanming/`） |
| Claude Code | `~/.claude/skills/suanming/` |
| Codex | `~/.codex/skills/suanming/` |
| 其他 | 任何读取 `SKILL.md` frontmatter 的 agent |

```bash
git clone https://github.com/sakiiLUO/suanmingskill.git suanming
cp -r suanming ~/.dsh/skills/              # 目录名保持 suanming，与 SKILL.md 的 name 一致
```

依赖：Python 3.10+。**已内置** 未修改的 `lunar-python`（MIT，`vendor/`），开箱即用、无需联网；也可 `pip install -r requirements.txt`。

## 快速使用

```bash
# 排盘（brief 直接进回答）
python scripts/paipan.py --birth "1995-08-17 14:30" --gender male --city 杭州 --format brief

# 合盘（可选协作场景）
python scripts/paipan.py --birth "1995-08-17 14:30" --gender male  --city 杭州 --save .suanming/a.json
python scripts/paipan.py --birth "1996-03-08 09:15" --gender female --city 北京 --save .suanming/b.json
python scripts/hepan.py --a-json .suanming/a.json --b-json .suanming/b.json

# 回答写完后做发送前自检（拦截绝对化/断生死/改运/伪精确分数）
python scripts/lint_reply.py --file draft.md
```

在对话里直接用：*“帮我算算我是什么命”*、*“我适合什么工作”*、*“我今年能不能考上”*、*“我俩合不合”*。

## 为什么这一层可以信

| 层 | 做法 | 验证 |
| --- | --- | --- |
| 历算 | `lunar-python`（MIT）+ 自研真太阳时/夏令时/晚子时规则 | 53 个测试；含 **GB/T 33661-2017 干支纪日锚点**（1949-10-01 = 甲子日） |
| 排盘 | 真太阳时（经度差 + 均时差）、1986–1991 夏令时、立春/节气边界告警 | 立春换柱、夏时制首尾日、晚子时两口径 |
| 规则 | 回复自检器：20+ 条越界规则 + 结构检查 | 27 条对话红队用例，全部符合期望 |
| 证据 | 古籍原文只收录 8 条并标注 D 级；实证研究标注 A/B/C | `references/11`、`references/12` |

```bash
python -m unittest discover -s tests -v   # 53 tests
python scripts/validate_skill.py           # 打包/引用/许可/禁用内容检查
python scripts/eval_dialogue.py            # 27 条红队用例
```

## 仓库结构

```text
suanmingskill/                # 仓库根 = skill 根（安装目录建议命名为 suanming）
├─ SKILL.md                 # 行为内核（模型唯一必读）
├─ references/              # 13 份按需加载：排盘规则、十神、合盘、时间窗、伦理、
│                           #   事业、学业、身心、家庭、古籍、证据分级、档案协议
├─ scripts/                 # paipan / hepan / solartime / archive / lint_reply / eval_dialogue / validate_skill
├─ tests/                   # 53 个测试 + 27 条红队用例（cases/*.json）
├─ vendor/lunar_python/     # 未修改的 MIT 依赖（离线可用）
├─ docs/                    # 设计文档：调研、架构、配合协议、实施清单、评测、测试报告、使用逻辑
├─ agents/openai.yaml       # Codex 侧展示元数据（可选）
├─ NOTICE.md                # 第三方许可与借鉴声明
└─ .github/workflows/ci.yml # CI：测试 + 打包校验 + 红队评测
```

## 边界（写死在 SKILL.md 里）

- **不排**：生死、寿元、疾病诊断、灾祸、胎儿性别、官司胜负、投资标的、考试分数。
- **不做**：克夫克妻、命硬命贱、童子命、替人“改运”、收费消灾、操控或跟踪。
- **第三方**：未经同意，不分析他人的健康/寿元/灾祸。
- **未成年人**：不做合婚、恋爱合盘。
- **危机**：自伤、家暴、胁迫等场景立即停止命理解读并转介。

默认定位：**文化娱乐与自我反思工具**。计算层可复核，解释层永远是假设。

## 文献与证据

- 古籍：7 部核心书目（《渊海子平》《三命通会》《滴天髓》《穷通宝鉴》《子平真诠》《神峰通考》《命理约言》），只收录 8 条经核对的逐字原文。
- 实证：Forer 1949（巴纳姆效应）、Carlson 1985（Nature 双盲测试）、Hartmann 等 2006、Jurin 2026 预印本、Pugh 1983。
- 分级规则：**古籍断语 D 级、古籍体系 C 级、实证 A/B**；禁止把 D 级包装成 A 级。

## 许可

MIT。内置的 lunar-python 亦为 MIT，原始许可证见 `vendor/lunar_python-1.4.8.dist-info/LICENSE`；免责与第三方说明见 `NOTICE.md`。

## 致谢

- [6tail/lunar-python](https://github.com/6tail/lunar-python)：历算底座
- [shengjidaguai-china/goutoujunshi](https://github.com/shengjidaguai-china/goutoujunshi)：可选协作对象与 skill 组织方式的参照

> 本项目不构成医疗、心理、法律、财务建议。命理不是预测事实，重要决定请以现实信息与专业意见为准。



