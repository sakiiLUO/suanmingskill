<p align="center">
  <img src="assets/logo.png" width="120" alt="suanming logo">
</p>
# 算命 skill（suanming）(｡･ω･｡)ﾉ♡

> 一个能独立使用的**八字排盘与解读** Agent Skill —— 把盘算准，把话说明白，把边界写死 ᕕ( ᐛ )ᕗ

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Tests](https://img.shields.io/badge/tests-77%20passing-brightgreen.svg)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB.svg)](https://www.python.org/)
![Good Vibes](https://img.shields.io/badge/vibes-%E5%8F%8B%E5%A5%BD%E4%B8%8D%E5%90%93%E4%BA%BA-ff69b4.svg)

<!-- LANGS:START -->
**简体中文** · [繁體中文](README.zh-TW.md) · [粵語](README.yue.md) · [日本語](README.ja.md) · [English](README.en.md)
<!-- LANGS:END -->

> 本页为简体中文原文；其他语言版本如与本文有出入，以本页为准。

---

## 嗨，先看这里 (◕‿◕)

这是一个给 AI Agent 用的 **skill**：`SKILL.md` 负责“怎么说话”，`references/` 是随手可查的小抄，`scripts/` 是真正把盘算出来的 Python。

它不吓人，也不装神弄鬼：

- 先老老实实**排盘**（真太阳时、夏令时、晚子时、节气边界都处理掉）
- 再给你「**盘面事实 → 边界与不确定 → 2~3 条带证据的假设 → 一个能自己验证的小动作**」
- 最后提醒你：**这是解释框架，不是预测。** 决定还是你自己做 (｡･ω･｡)ﾉ♡

> 关系里的“要不要继续、这句话怎么回”？那部分可以交给 [狗头军师](https://github.com/shengjidaguai-china/goutoujunshi)，但这个 skill **默认自己就能用**，不需要它。

## 你可能想这么问 💬

```text
“帮我算算我是什么命呀～”
“我到底适合做什么工作？(´･ω･`)”
“今年考试能过吗，别哄我”
“我俩合不合？”
“我妈为啥总跟我吵”
“这玩意儿科学吗？”
“我是不是克夫……”      ← 这句会被温柔地拆掉
```

## 它会怎么回你 ✨

```text
盘面事实：真太阳时 1995-08-17 14:26，四柱 乙亥 甲申 庚辰 癸未，日主庚金，月令申金；
          当前行辛巳大运（2018–2027），2026 流年丙午。
边界与不确定：出生时间距未时/申时交界较远，时柱稳定；未命中 1986–1991 夏令时。
假设（不是定论）：日主庚金、月令申金，通常被解释为遇事先自己扛、不爱示弱。
反向可能：也可能是从小被要求独立形成的习惯，不是天性。
可验证的小动作：回想最近三次压力事件，你是先找人商量还是先自己消化；
              如果都是自己消化，这条就更像你。
以上是解释框架，不是预测 (・∀・)
```

看到了吗？**每句“结论”都带着证据、反向可能和一个能验证的动作**——不给你“注定”两个字 (๑•̀ㅂ•́)و✧

## 能帮你看什么 ⭐

| 你想聊的 | 它会聊的 | 它会明确绕开的 |
| --- | --- | --- |
| 性格、行为模式 | 2~3 条带证据的假设 | 身强身弱、用神喜忌的定论 |
| 事业、职业方向 | 工作风格、组织形态、时间窗 | 具体行业/公司、投资标的 |
| 学业、考试 | 学习方式、压力节奏 | 分数、录取、上岸概率 |
| 身体、焦虑状态 | 压力反应、作息、求助路径 | 诊断、疾病预测、停药建议 |
| 父母、子女、家庭 | 家庭角色、边界议题 | 第三方寿元/健康/婚变 |
| 恋爱、合不合 | 7 个维度 + 证据 | “能不能成”的判决 |
| 大运流年、什么时候 | 时间窗假设 + 观察信号 | 具体应期、吉凶断言 |
| “这科学吗？” | 古籍出处 + A/B/C/D 证据分级 | 把经验说法包装成科学结论 |

## 还能给你一句经文 (｡•̀ᴗ-)✧

有时候你不需要更多分析，只需要一句有分量的话。它能从《道德经》《论语》《心经》《圣经》（和合本）里挑一句，配一句白话解释，再落回你的事：

```text
《道德经》二十三章：「飘风不终朝，骤雨不终日。」
意思是：再大的风雨，也不会刮一整天。
放到你这件事上——难受是有期限的，但期限不会自己到。
（这句不是预言，你也可以不用。）
```

规矩也写死：**一次一条、必须标出处、不劝诱改宗、不用地狱/末日/报应恐吓、不拿经文当预测依据**。中文《古兰经》译本还在版权期，所以只转述大意并注明 (｀・ω・´)

## 它不做什么 🚫

- 不排生死、寿元、疾病诊断、灾祸、胎儿性别、官司胜负、投资标的、考试分数
- 不做克夫克妻、命硬命贱、童子命，也不替人“改运”、收费消灾
- 未经同意，不分析别人的健康、寿元、隐私
- 不做未成年人的合婚、婚期、结婚推算；恋爱合盘可以聊相处与边界
- 遇到自伤、家暴、胁迫，**立刻停止命理解读**，先确认安全

它甚至自带一个“发送前自检器”，回答里出现“注定/一定会/克夫/血光/开光/合盘 87 分”这类话会被拦下来改掉 (｀・ω・´)ｼ

## 三分钟装上 (๑•̀ㅂ•́)و✧

```bash
git clone https://github.com/sakiiLUO/suanmingskill.git suanming
cp -r suanming ~/.dsh/skills/        # 目录名保持 suanming，跟 SKILL.md 的 name 一致
```

| 宿主 | 放哪儿 |
| --- | --- |
| DSH / DeepSeek Harness | `~/.dsh/skills/suanming/`（或项目内 `<repo>/.dsh/skills/suanming/`） |
| Claude Code | `~/.claude/skills/suanming/` |
| Codex | `~/.codex/skills/suanming/` |
| 其他 | 任何读 `SKILL.md` frontmatter 的 agent 都行 |

需要 **Python 3.10+**。历法依赖 `lunar-python`（MIT）已经放在 `vendor/` 里了，**开箱即用、不用联网**；想用 pip 也可以：`pip install -r requirements.txt`。

## 懒得自己装？让 AI 帮你 (っ•̀ω•́)っ

把下面这段直接复制给你的 AI（Claude Code / Codex / DSH / Cursor 都行），它会自己 clone、装好、跑测试：

<!-- AI-INSTALL:START -->
```text
请帮我把这个 Agent Skill 安装到本机并验证：
仓库：https://github.com/sakiiLUO/suanmingskill

1. 先确认宿主和 skill 目录，不确定就问我：
   - DSH：~/.dsh/skills/（项目级用 <repo>/.dsh/skills/）
   - Claude Code：~/.claude/skills/
   - Codex：~/.codex/skills/
2. clone 到临时目录，再复制成 <skill目录>/suanming/；确认根目录有 SKILL.md，且 frontmatter 的 name 是 suanming。
3. 需要 Python 3.10+；依赖已内置在 vendor/，不要全局 pip 安装。
4. 验证：cd <skill目录>/suanming && python -m unittest discover -s tests && python scripts/validate_skill.py
5. 报告：装在哪、Python 版本、测试通过几个、有没有失败项。

约束：不要改仓库源码；不要用管理员/sudo 权限；不要全局装包；不要跳过验证；任何一步失败就停下，告诉我原因和回滚方法（删掉 <skill目录>/suanming/ 即可回滚）。
```
<!-- AI-INSTALL:END -->

装完想确认它真在工作？新开一个会话说「帮我算算我是什么命」，它应该先问你生日、时间、城市、性别，而不是直接编 (๑•̀ㅂ•́)و✧

只想检查装没装好，用这一句：

```text
帮我检查本机是否装好了 suanming skill：找到 <skill目录>/suanming/SKILL.md，
跑 python -m unittest discover -s tests，把路径和结果告诉我；没装就说没装，不要自己装。
```
**装完小贴士**

- 生效方式：DSH 热加载；Claude Code 一般不用重启；**Codex 要重启**才认。
- Windows 用 junction（`mklink /J`）不需要管理员；但 **Codex 会跳过 symlink**，给 Codex 请复制实体目录。
- 目录名固定 `suanming`（与 `SKILL.md` 的 `name` 一致），别改。
- 网络失败就停下重试，别退化成 `sudo` 或全局 `pip install`。

## 还能排紫微、摇六爻，也能聊「怎么长久」 (｡•̀ᴗ-)✧

```bash
# 紫微斗数：十二宫 + 主星 + 四化 + 大限流年（iztro/MIT，离线；需要 Node.js 18+）
python scripts/ziwei.py --birth "1995-08-17 14:30" --gender male --city 杭州 --format brief

# 六爻：摇一卦问一件具体的事（纯标准库，规则表由测试锁定）
python scripts/liuyao.py --lines 7,8,9,7,6,8 --date "2026-10-31 19:40" --question "这次合作能成吗" --format brief
```

- **紫微**看十二宫与四化落点，**六爻**看一件事的世应与动爻；两套都**不做吉凶打分、不承诺应期**。
- 想聊“怎么维持下去”，它给的是《长期维护指南》里的动作：每周 20 分钟低压对话、冲突后 24 小时内修复、一次只改一个习惯……**不承诺“照做就一定长久”** (｀・ω・´)
## 用起来 (ﾉ´ヮ`)ﾉ*: ･ﾟ

```bash
# 排盘（brief 模式适合直接贴进回答）
python scripts/paipan.py --birth "1995-08-17 14:30" --gender male --city 杭州 --format brief

# 合盘（想看两个人怎么相处的时候）
python scripts/paipan.py --birth "1995-08-17 14:30" --gender male   --city 杭州 --save .suanming/a.json
python scripts/paipan.py --birth "1996-03-08 09:15" --gender female --city 北京 --save .suanming/b.json
python scripts/hepan.py --a-json .suanming/a.json --b-json .suanming/b.json

# 回答写完先自检一下，别说过头
python scripts/lint_reply.py --file draft.md
```

然后在对话里直接说：*“帮我算算我是什么命”*、*“我适合什么工作”*、*“我俩合不合”* 就好啦～

## 🔍 为什么这层可以信

玩笑归玩笑，**算盘这一层是认真的**：

| 层 | 做法 | 验证 |
| --- | --- | --- |
| 历算 | `lunar-python`（MIT）+ 自研真太阳时/夏令时/晚子时规则 | 77 个测试；含 **GB/T 33661-2017 干支纪日锚点**（1949-10-01 = 甲子日） |
| 排盘 | 真太阳时（经度差 + 均时差）、1986–1991 夏令时、立春/节气边界告警 | 立春换柱、夏时制首尾日、晚子时两口径 |
| 说话 | 回复自检器：20+ 条越界规则 + 结构检查 | 34 条对话红队用例，全部符合期望 |
| 引用 | 古籍只收 8 条经核对原文并标 D 级；实证研究标 A/B/C | `references/11`、`references/12` |

```bash
python -m unittest discover -s tests -v   # 77 tests
python scripts/validate_skill.py           # 结构/引用/许可/禁用内容
python scripts/eval_dialogue.py            # 40 条红队用例
```

## 仓库里都有啥 📦

```text
suanmingskill/                # 仓库根 = skill 根（安装目录建议叫 suanming）
├─ assets/                   # logo / social preview
├─ SKILL.md                   # 行为内核：模型唯一必读的那份
├─ references/                # 16 份按需加载（含经文、长期维护、紫微与六爻）：排盘、十神、合盘、时间窗、伦理、
│                             #   事业、学业、身心、家庭、古籍、证据分级、档案
├─ scripts/                   # paipan / hepan / ziwei / liuyao / solartime / archive /
│                             #   lint_reply / eval_dialogue / validate_skill
├─ tests/                     # 77 个测试 + 40 条红队用例
├─ vendor/lunar_python/       # 未修改的 MIT 依赖（离线可用）
├─ docs/                      # 设计笔记：调研、架构、配合协议、评测、测试报告
├─ agents/openai.yaml         # Codex 侧展示信息（可选）
├─ NOTICE.md                  # 第三方许可与借鉴声明
└─ .github/workflows/ci.yml   # CI：测试 + 校验 + 红队 + smoke
```

## 📚 文献与证据

- **古籍**：《渊海子平》《三命通会》《滴天髓》《穷通宝鉴》《子平真诠》《神峰通考》《命理约言》——7 部书目，外加 **8 条经核对的逐字原文**（每条都带来源链接）
- **实证**：Forer 1949（巴纳姆效应）、Carlson 1985（Nature 双盲测试）、Hartmann 等 2006、Jurin 2026 预印本、Pugh 1983
- **分级规则**：古籍断语 D 级、古籍体系 C 级、实证 A/B；**禁止把 D 级包装成 A 级** (｀・ω・´)

## 常见小问题 (・∀・)

**Q：要联网吗？**
不用。`vendor/` 里已经放好依赖，排盘纯本地。

**Q：要钱吗？**
不要，MIT。随便用，署个名就行。

**Q：我的生日会被上传吗？**
不会。计算全在本地；要存档案必须你明确同意（`--consent`），而且随时能查、能删。

**Q：能算紫微斗数 / 六爻 / 塔罗吗？**
紫微和六爻已经能排了（紫微用 MIT 的 iztro，六爻是纯标准库的规则层）；塔罗还没有，欢迎 PR (๑•̀ㅂ•́)و✧

**Q：它会不会突然跟我说“你注定……”？**
不会。`scripts/lint_reply.py` 会拦，`SKILL.md` 也写死了不许用决定论措辞。

**Q：准不准呀？**
它自己会说：*“我不会说自己算得准。盘面是算出来的，解释是假设；准不准要看你能不能从假设里挑出对你有用的部分。”* (´･ω･`)

**Q：支持哪些语言？**
简中、繁中、粤语、日语、英语。用这五种语言提问，就用同一种语言回答；其他语言默认用英语回答。

## 许可

MIT。内置的 lunar-python 也是 MIT，原始许可证在 `vendor/lunar_python-1.4.8.dist-info/LICENSE`；第三方说明见 `NOTICE.md`。

## 致谢 (｡･ω･｡)ﾉ♡

- [6tail/lunar-python](https://github.com/6tail/lunar-python)：历算底座
- [shengjidaguai-china/goutoujunshi](https://github.com/shengjidaguai-china/goutoujunshi)：可选协作对象，也是 skill 组织方式的参照

> 本项目不构成医疗、心理、法律、财务建议。命理不是预测事实，重要决定请以现实信息与专业意见为准 (◕‿◕)




