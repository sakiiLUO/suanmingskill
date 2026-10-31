# 算命 skill（suanming）(｡･ω･｡)ﾉ♡

> 一個能獨立使用的**八字排盤與解讀** Agent Skill —— 把盤算準，把話說明白，把邊界寫死 ᕕ( ᐛ )ᕗ

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Tests](https://img.shields.io/badge/tests-53%20passing-brightgreen.svg)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB.svg)](https://www.python.org/)
![Good Vibes](https://img.shields.io/badge/vibes-%E5%8F%8B%E5%A5%BD%E4%B8%8D%E5%90%93%E4%BA%BA-ff69b4.svg)

<!-- LANGS:START -->
[简体中文](README.md) · **繁體中文** · [粵語](README.yue.md) · [日本語](README.ja.md) · [English](README.en.md)
<!-- LANGS:END -->

> 本頁為譯文；如與简体中文版有出入，以简体中文版為準。

---

## 嗨，先看這裡 (◕‿◕)

這是一個給 AI Agent 用的 **skill**：`SKILL.md` 負責「怎麼說話」，`references/` 是隨手可查的小抄，`scripts/` 是真正把盤算出來的 Python。

它不嚇人，也不裝神弄鬼：

- 先老老實實**排盤**（真太陽時、夏令時、晚子時、節氣邊界都處理掉）
- 再給你「**盤面事實 → 邊界與不確定 → 2~3 條帶證據的假設 → 一個能自己驗證的小動作**」
- 最後提醒你：**這是解釋框架，不是預測。** 決定還是你自己做 (｡･ω･｡)ﾉ♡

> 關係裡的「要不要繼續、這句話怎麼回」？那部分可以交給 [狗頭軍師](https://github.com/shengjidaguai-china/goutoujunshi)，但這個 skill **預設自己就能用**，不需要它。

## 你可能想這麼問 💬

```text
“幫我算算我是什麼命呀～”
“我到底適合做什麼工作？(´･ω･`)”
“今年考試能過嗎，別哄我”
“我倆合不合？”
“我媽為啥總跟我吵”
“這玩意兒科學嗎？”
“我是不是剋夫……”      ← 這句會被溫柔地拆掉
```

## 它會怎麼回你 ✨

```text
盤面事實：真太陽時 1995-08-17 14:26，四柱 乙亥 甲申 庚辰 癸未，日主庚金，月令申金；
          當前走辛巳大運（2018–2027），2026 流年丙午。
邊界與不確定：出生時間距未時/申時交界較遠，時柱穩定；未命中 1986–1991 夏令時。
假設（不是定論）：日主庚金、月令申金，通常被解釋為遇事先自己扛、不愛示弱。
反向可能：也可能是從小被要求獨立形成的習慣，不是天性。
可驗證的小動作：回想最近三次壓力事件，你是先找人商量還是先自己消化；
              如果都是自己消化，這條就更像你。
以上是解釋框架，不是預測 (・∀・)
```

看到了嗎？**每句「結論」都帶著證據、反向可能和一個能驗證的動作**——不給你「注定」兩個字 (๑•̀ㅂ•́)و✧

## 能幫你看什麼 ⭐

| 你想聊的 | 它會聊的 | 它會明確繞開的 |
| --- | --- | --- |
| 性格、行為模式 | 2~3 條帶證據的假設 | 身強身弱、用神喜忌的定論 |
| 事業、職業方向 | 工作風格、組織形態、時間窗 | 具體行業/公司、投資標的 |
| 學業、考試 | 學習方式、壓力節奏 | 分數、錄取、上岸機率 |
| 身體、焦慮狀態 | 壓力反應、作息、求助路徑 | 診斷、疾病預測、停藥建議 |
| 父母、子女、家庭 | 家庭角色、邊界議題 | 第三方壽元/健康/婚變 |
| 戀愛、合不合 | 7 個維度 + 證據 | 「能不能成」的判決 |
| 大運流年、什麼時候 | 時間窗假設 + 觀察訊號 | 具體應期、吉凶斷言 |
| 「這科學嗎？」 | 古籍出處 + A/B/C/D 證據分級 | 把經驗說法包裝成科學結論 |

## 還能給你一句經文 (｡•̀ᴗ-)✧

有時候你不需要更多分析，只需要一句有分量的話。它能從《道德經》《論語》《心經》《聖經》（和合本）裡挑一句，配一句白話解釋，再落回你的事：

```text
《道德經》二十三章：「飄風不終朝，驟雨不終日。」
意思是：再大的風雨，也不會颳一整天。
放到你這件事上——難受是有期限的，但期限不會自己到。
（這句不是預言，你也可以不用。）
```

規矩也寫死：**一次一條、必須標出處、不勸誘改宗、不用地獄/末日/報應恐嚇、不拿經文當預測依據**。中文《古蘭經》譯本還在版權期，所以只轉述大意並註明 (｀・ω・´)

## 它不做什麼 🚫

- 不排生死、壽元、疾病診斷、災禍、胎兒性別、官司勝負、投資標的、考試分數
- 不做剋夫剋妻、命硬命賤、童子命，也不替人「改運」、收費消災
- 未經同意，不分析別人的健康、壽元、隱私
- 不做未成年人的合婚、戀愛合盤
- 遇到自傷、家暴、脅迫，**立刻停止命理解讀**，先確認安全

它甚至自帶一個「送出前自檢器」，回答裡出現「注定/一定會/剋夫/血光/開光/合盤 87 分」這類話會被攔下來改掉 (｀・ω・´)ｼ

## 三分鐘裝上 (๑•̀ㅂ•́)و✧

```bash
git clone https://github.com/sakiiLUO/suanmingskill.git suanming
cp -r suanming ~/.dsh/skills/        # 目錄名保持 suanming，跟 SKILL.md 的 name 一致
```

| 宿主 | 放哪兒 |
| --- | --- |
| DSH / DeepSeek Harness | `~/.dsh/skills/suanming/`（或專案內 `<repo>/.dsh/skills/suanming/`） |
| Claude Code | `~/.claude/skills/suanming/` |
| Codex | `~/.codex/skills/suanming/` |
| 其他 | 任何會讀 `SKILL.md` frontmatter 的 agent 都行 |

需要 **Python 3.10+**。曆法依賴 `lunar-python`（MIT）已經放在 `vendor/` 裡了，**開箱即用、不用連網**；想用 pip 也可以：`pip install -r requirements.txt`。

## 用起來 (ﾉ´ヮ`)ﾉ*: ･ﾟ

```bash
# 排盤（brief 模式適合直接貼進回答）
python scripts/paipan.py --birth "1995-08-17 14:30" --gender male --city 杭州 --format brief

# 合盤（想看兩個人怎麼相處的時候）
python scripts/paipan.py --birth "1995-08-17 14:30" --gender male   --city 杭州 --save .suanming/a.json
python scripts/paipan.py --birth "1996-03-08 09:15" --gender female --city 北京 --save .suanming/b.json
python scripts/hepan.py --a-json .suanming/a.json --b-json .suanming/b.json

# 回答寫完先自檢一下，別說過頭
python scripts/lint_reply.py --file draft.md
```

然後在對話裡直接說：*“幫我算算我是什麼命”*、*“我適合什麼工作”*、*“我倆合不合”* 就好啦～

## 🔍 為什麼這層可以信

玩笑歸玩笑，**算盤這一層是認真的**：

| 層 | 做法 | 驗證 |
| --- | --- | --- |
| 曆算 | `lunar-python`（MIT）+ 自研真太陽時/夏令時/晚子時規則 | 53 個測試；含 **GB/T 33661-2017 干支紀日錨點**（1949-10-01 = 甲子日） |
| 排盤 | 真太陽時（經度差 + 均時差）、1986–1991 夏令時、立春/節氣邊界告警 | 立春換柱、夏時制首尾日、晚子時兩口徑 |
| 說話 | 回覆自檢器：20+ 條越界規則 + 結構檢查 | 34 條對話紅隊用例，全部符合期望 |
| 引用 | 古籍只收 8 條經核對原文並標 D 級；實證研究標 A/B/C | `references/11`、`references/12` |

```bash
python -m unittest discover -s tests -v   # 53 tests
python scripts/validate_skill.py           # 結構/引用/許可/禁用內容
python scripts/eval_dialogue.py            # 34 條紅隊用例
```

## 倉庫裡都有啥 📦

```text
suanmingskill/                # 倉庫根 = skill 根（安裝目錄建議叫 suanming）
├─ SKILL.md                   # 行為內核：模型唯一必讀的那份
├─ references/                # 14 份按需載入（含經文與格言）：排盤、十神、合盤、時間窗、倫理、
│                             #   事業、學業、身心、家庭、古籍、證據分級、檔案
├─ scripts/                   # paipan / hepan / solartime / archive /
│                             #   lint_reply / eval_dialogue / validate_skill
├─ tests/                     # 53 個測試 + 34 條紅隊用例
├─ vendor/lunar_python/       # 未修改的 MIT 依賴（離線可用）
├─ docs/                      # 設計筆記：調研、架構、配合協定、評測、測試報告
├─ agents/openai.yaml         # Codex 側展示資訊（可選）
├─ NOTICE.md                  # 第三方授權與借鑑聲明
└─ .github/workflows/ci.yml   # CI：測試 + 校驗 + 紅隊 + smoke
```

## 📚 文獻與證據

- **古籍**：《淵海子平》《三命通會》《滴天髓》《窮通寶鑑》《子平真詮》《神峰通考》《命理約言》——7 部書目，外加 **8 條經核對的逐字原文**（每條都帶來源連結）
- **實證**：Forer 1949（巴納姆效應）、Carlson 1985（Nature 雙盲測試）、Hartmann 等 2006、Jurin 2026 預印本、Pugh 1983
- **分級規則**：古籍斷語 D 級、古籍體系 C 級、實證 A/B；**禁止把 D 級包裝成 A 級** (｀・ω・´)

## 常見小問題 (・∀・)

**Q：要連網嗎？**
不用。`vendor/` 裡已經放好依賴，排盤純本機。

**Q：要錢嗎？**
不要，MIT。隨便用，署個名就行。

**Q：我的生日會被上傳嗎？**
不會。計算全在本機；要存檔案必須你明確同意（`--consent`），而且隨時能查、能刪。

**Q：能算紫微斗數 / 六爻 / 塔羅嗎？**
暫時沒有。紫微在路線圖裡（打算用 MIT 的 iztro，走 Node 子進程），歡迎 PR (๑•̀ㅂ•́)و✧

**Q：它會不會突然跟我說「你注定……」？**
不會。`scripts/lint_reply.py` 會攔，`SKILL.md` 也寫死了不許用決定論措辭。

**Q：準不準呀？**
它自己會說：*“我不會說自己算得準。盤面是算出來的，解釋是假設；準不準要看你能不能從假設裡挑出對你有用的部分。”* (´･ω･`)

## 許可

MIT。內建的 lunar-python 也是 MIT，原始授權在 `vendor/lunar_python-1.4.8.dist-info/LICENSE`；第三方說明見 `NOTICE.md`。

## 致謝 (｡･ω･｡)ﾉ♡

- [6tail/lunar-python](https://github.com/6tail/lunar-python)：曆算底座
- [shengjidaguai-china/goutoujunshi](https://github.com/shengjidaguai-china/goutoujunshi)：可選協作對象，也是 skill 組織方式的參照

> 本專案不構成醫療、心理、法律、財務建議。命理不是預測事實，重要決定請以現實資訊與專業意見為準 (◕‿◕)
