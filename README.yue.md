# 算命 skill（suanming）(｡･ω･｡)ﾉ♡

> 一個可以獨立使用嘅**八字排盤同解讀** Agent Skill —— 將個盤算準，將說話講清楚，將界線寫死 ᕕ( ᐛ )ᕗ

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Tests](https://img.shields.io/badge/tests-53%20passing-brightgreen.svg)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB.svg)](https://www.python.org/)
![Good Vibes](https://img.shields.io/badge/vibes-%E5%8F%8B%E5%A5%BD%E4%B8%8D%E5%90%93%E4%BA%BA-ff69b4.svg)

<!-- LANGS:START -->
[简体中文](README.md) · [繁體中文](README.zh-TW.md) · **粵語** · [日本語](README.ja.md) · [English](README.en.md)
<!-- LANGS:END -->

> 呢頁係譯文；如同简体中文版有出入，以简体中文版為準。

---

## 嗨，先睇呢度 (◕‿◕)

呢個係一個俾 AI Agent 用嘅 **skill**：`SKILL.md` 負責「點樣講嘢」，`references/` 係隨時可以查嘅小抄，`scripts/` 係真正將個盤算出來嘅 Python。

佢唔嚇人，亦都唔裝神弄鬼：

- 首先老老實實**排盤**（真太陽時、夏令時、晚子時、節氣邊界全部處理好）
- 然後俾你「**盤面事實 → 邊界同不確定 → 2~3 條有證據嘅假設 → 一個可以自己驗證嘅小動作**」
- 最後提醒你：**呢個係解釋框架，唔係預測。** 決定始終係你自己做 (｡･ω･｡)ﾉ♡

> 關係入面嘅「要唔要繼續、呢句說話點回」？嗰部分可以交俾 [狗頭軍師](https://github.com/shengjidaguai-china/goutoujunshi)，但呢個 skill **默認自己就用到**，唔需要佢。

## 你可能會想咁問 💬

```text
「幫我算吓我係咩命呀～」
「我到底適合做咩工作？(´･ω･`)」
「今年考試過唔過到，唔好氹我」
「我哋夾唔夾？」
「我阿媽點解成日同我嗌交」
「呢樣嘢科學咩？」
「我係咪剋夫……」      ← 呢句會被溫柔咁拆掉
```

## 佢會點樣回你 ✨

```text
盤面事實：真太陽時 1995-08-17 14:26，四柱 乙亥 甲申 庚辰 癸未，日主庚金，月令申金；
          現行辛巳大運（2018–2027），2026 流年丙午。
邊界同不確定：出生時間距離未時/申時交界較遠，時柱穩定；冇撞中 1986–1991 夏令時。
假設（唔係定論）：日主庚金、月令申金，通常會被解釋為遇事先自己扛、唔鍾意示弱。
反方向可能：都可能係由細被要求獨立而形成嘅習慣，唔係天性。
可以驗證嘅小動作：回想最近三次壓力事件，你係先搵人商量定係先自己消化；
              如果全部都係自己消化，呢條就更似你。
以上係解釋框架，唔係預測 (・∀・)
```

睇到未？**每句「結論」都帶住證據、反方向可能同一個可以驗證嘅動作**——唔會俾你「注定」兩個字 (๑•̀ㅂ•́)و✧

## 可以幫你睇啲咩 ⭐

| 你想傾嘅 | 佢會傾嘅 | 佢會明確避開嘅 |
| --- | --- | --- |
| 性格、行為模式 | 2~3 條有證據嘅假設 | 身強身弱、用神喜忌嘅定論 |
| 事業、職業方向 | 工作風格、組織形態、時間窗 | 具體行業/公司、投資標的 |
| 學業、考試 | 學習方式、壓力節奏 | 分數、錄取、上岸機會率 |
| 身體、焦慮狀態 | 壓力反應、作息、求助路徑 | 診斷、疾病預測、停藥建議 |
| 父母、子女、家庭 | 家庭角色、邊界議題 | 第三方壽元/健康/婚變 |
| 戀愛、夾唔夾 | 7 個維度 + 證據 | 「能唔能成」嘅判決 |
| 大運流年、幾時 | 時間窗假設 + 觀察訊號 | 具體應期、吉凶斷言 |
| 「呢樣嘢科學咩？」 | 古籍出處 + A/B/C/D 證據分級 | 將經驗說法包裝成科學結論 |

## 仲可以俾你一句經文 (｡•̀ᴗ-)✧

有時候你唔需要更多分析，只需要一句有份量嘅說話。佢可以喺《道德經》《論語》《心經》《聖經》（和合本）入面揀一句，配一句白話解釋，再落返你件事：

```text
《道德經》二十三章：「飄風不終朝，驟雨不終日。」
意思係：再大嘅風雨，都唔會刮足一整日。
放喺你件事上面——難受係有期限嘅，但期限唔會自己到。
（呢句唔係預言，你都可以唔用。）
```

規矩都寫死：**一次一條、一定要標出處、唔勸誘改宗、唔用地獄/末日/報應嚟恐嚇、唔拿經文當預測依據**。中文《古蘭經》譯本仲喺版權期，所以只轉述大意兼註明 (｀・ω・´)

## 佢唔做啲咩 🚫

- 唔排生死、壽元、疾病診斷、災禍、胎兒性別、官司勝負、投資標的、考試分數
- 唔做剋夫剋妻、命硬命賤、童子命，亦都唔會替人「改運」、收費消災
- 未經同意，唔會分析其他人嘅健康、壽元、私隱
- 唔做未成年人嘅合婚、戀愛合盤
- 遇到自傷、家暴、脅迫，**即刻停止命理解讀**，先確認安全

佢仲自帶一個「發送前自檢器」，答案入面出現「注定/一定會/剋夫/血光/開光/合盤 87 分」呢類說話會被攔落嚟改掉 (｀・ω・´)ｼ

## 三分鐘裝好 (๑•̀ㅂ•́)و✧

```bash
git clone https://github.com/sakiiLUO/suanmingskill.git suanming
cp -r suanming ~/.dsh/skills/        # 目錄名保持 suanming，同 SKILL.md 嘅 name 一致
```

| 宿主 | 放喺邊 |
| --- | --- |
| DSH / DeepSeek Harness | `~/.dsh/skills/suanming/`（或者項目內 `<repo>/.dsh/skills/suanming/`） |
| Claude Code | `~/.claude/skills/suanming/` |
| Codex | `~/.codex/skills/suanming/` |
| 其他 | 任何會讀 `SKILL.md` frontmatter 嘅 agent 都得 |

需要 **Python 3.10+**。曆法依賴 `lunar-python`（MIT）已經放咗喺 `vendor/` 入面，**開箱即用、唔使聯網**；想用 pip 都可以：`pip install -r requirements.txt`。

## 懶得自己裝？叫 AI 幫你 (っ•̀ω•́)っ

將下面呢段直接複製畀你嘅 AI（Claude Code / Codex / DSH / Cursor 都得），佢會自己 clone、裝好、跑測試：

<!-- AI-INSTALL:START -->
```text
請幫我將呢個 Agent Skill 安裝到本機並且驗證：
倉庫：https://github.com/sakiiLUO/suanmingskill

1. 先確認宿主同 skill 目錄，唔確定就問我：
   - DSH：~/.dsh/skills/（項目級用 <repo>/.dsh/skills/）
   - Claude Code：~/.claude/skills/
   - Codex：~/.codex/skills/
2. clone 到臨時目錄，再複製成 <skill目錄>/suanming/；確認根目錄有 SKILL.md，而且 frontmatter 嘅 name 係 suanming。
3. 需要 Python 3.10+；依賴已經內置喺 vendor/，唔好全局 pip 安裝。
4. 驗證：cd <skill目錄>/suanming && python -m unittest discover -s tests && python scripts/validate_skill.py
5. 報告：裝喺邊、Python 版本、測試通過幾多個、有冇失敗項。

約束：唔好改倉庫源碼；唔好用管理員/sudo 權限；唔好全局裝包；唔好跳過驗證；任何一步失敗就停下，同我講原因同回滾方法（刪掉 <skill目錄>/suanming/ 就可以回滾）。
```
<!-- AI-INSTALL:END -->

裝完想確認佢真係做緊嘢？新開一個會話講「幫我算吓我係咩命」，佢應該先問你生日、時間、城市、性別，而唔係直接編 (๑•̀ㅂ•́)و✧

只想檢查裝好未，用呢一句：

```text
幫我檢查本機裝好咗 suanming skill 未：搵到 <skill目錄>/suanming/SKILL.md，
跑 python -m unittest discover -s tests，將路徑同結果話我知；冇裝就話冇裝，唔好自己裝。
```

**裝完小貼士**

- 生效方式：DSH 熱載入；Claude Code 通常唔使重開；**Codex 要重開**先認得。
- Windows 用 junction（`mklink /J`）唔使管理員；不過 **Codex 會跳過 symlink**，畀 Codex 請複製實體資料夾。
- 資料夾名固定 `suanming`（同 `SKILL.md` 嘅 `name` 一致），唔好改。
- 網絡失敗就停低重試，唔好變成 `sudo` 或者全域 `pip install`。

## 用起上嚟 (ﾉ´ヮ`)ﾉ*: ･ﾟ

```bash
# 排盤（brief 模式適合直接貼入回答）
python scripts/paipan.py --birth "1995-08-17 14:30" --gender male --city 杭州 --format brief

# 合盤（想睇兩個人點樣相處嘅時候）
python scripts/paipan.py --birth "1995-08-17 14:30" --gender male   --city 杭州 --save .suanming/a.json
python scripts/paipan.py --birth "1996-03-08 09:15" --gender female --city 北京 --save .suanming/b.json
python scripts/hepan.py --a-json .suanming/a.json --b-json .suanming/b.json

# 回答寫完先自檢一下，唔好講過頭
python scripts/lint_reply.py --file draft.md
```

然後喺對話入面直接講：*「幫我算吓我係咩命」*、*「我適合咩工作」*、*「我哋夾唔夾」* 就得啦～

## 🔍 點解呢層可以信

講笑還講笑，**排盤呢一層係認真嘅**：

| 層 | 做法 | 驗證 |
| --- | --- | --- |
| 曆算 | `lunar-python`（MIT）+ 自研真太陽時/夏令時/晚子時規則 | 53 個測試；包含 **GB/T 33661-2017 干支紀日錨點**（1949-10-01 = 甲子日） |
| 排盤 | 真太陽時（經度差 + 均時差）、1986–1991 夏令時、立春/節氣邊界告警 | 立春換柱、夏時制首尾日、晚子時兩種口徑 |
| 說話 | 回覆自檢器：20+ 條越界規則 + 結構檢查 | 34 條對話紅隊用例，全部符合預期 |
| 引用 | 古籍只收 8 條經核對原文並標 D 級；實證研究標 A/B/C | `references/11`、`references/12` |

```bash
python -m unittest discover -s tests -v   # 53 tests
python scripts/validate_skill.py           # 結構/引用/許可/禁用內容
python scripts/eval_dialogue.py            # 34 條紅隊用例
```

## 倉庫入面有啲咩 📦

```text
suanmingskill/                # 倉庫根 = skill 根（安裝目錄建議叫 suanming）
├─ SKILL.md                   # 行為內核：模型唯一必讀嗰份
├─ references/                # 14 份按需載入（含經文與格言）：排盤、十神、合盤、時間窗、倫理、
│                             #   事業、學業、身心、家庭、古籍、證據分級、檔案
├─ scripts/                   # paipan / hepan / solartime / archive /
│                             #   lint_reply / eval_dialogue / validate_skill
├─ tests/                     # 53 個測試 + 34 條紅隊用例
├─ vendor/lunar_python/       # 未修改嘅 MIT 依賴（離線可用）
├─ docs/                      # 設計筆記：調研、架構、配合協議、評測、測試報告
├─ agents/openai.yaml         # Codex 側展示資訊（可選）
├─ NOTICE.md                  # 第三方許可與借鑑聲明
└─ .github/workflows/ci.yml   # CI：測試 + 校驗 + 紅隊 + smoke
```

## 📚 文獻與證據

- **古籍**：《淵海子平》《三命通會》《滴天髓》《窮通寶鑑》《子平真詮》《神峰通考》《命理約言》——7 部書目，外加 **8 條經核對嘅逐字原文**（每條都帶來源連結）
- **實證**：Forer 1949（巴納姆效應）、Carlson 1985（Nature 雙盲測試）、Hartmann 等 2006、Jurin 2026 預印本、Pugh 1983
- **分級規則**：古籍斷語 D 級、古籍體系 C 級、實證 A/B；**禁止將 D 級包裝成 A 級** (｀・ω・´)

## 常見小問題 (・∀・)

**Q：要聯網咩？**
唔使。`vendor/` 入面已經放好依賴，排盤純本地。

**Q：要錢咩？**
唔使，MIT。隨便用，署個名就得。

**Q：我個生日會被上傳咩？**
唔會。計算全部喺本地；要存檔案必須你明確同意（`--consent`），而且隨時查得、刪得。

**Q：可以算紫微斗數 / 六爻 / 塔羅咩？**
暫時冇。紫微喺路線圖入面（打算用 MIT 嘅 iztro，走 Node 子進程），歡迎 PR (๑•̀ㅂ•́)و✧

**Q：佢會唔會突然同我講「你注定……」？**
唔會。`scripts/lint_reply.py` 會攔，`SKILL.md` 都寫死咗唔准用決定論措辭。

**Q：準唔準呀？**
佢自己會講：*「我唔會話自己算得準。盤面係算出來嘅，解釋係假設；準唔準要睇你能唔能夠由假設入面揀出對你有用嘅部分。」* (´･ω･`)

## 許可

MIT。內置嘅 lunar-python 都係 MIT，原始許可證喺 `vendor/lunar_python-1.4.8.dist-info/LICENSE`；第三方說明見 `NOTICE.md`。

## 致謝 (｡･ω･｡)ﾉ♡

- [6tail/lunar-python](https://github.com/6tail/lunar-python)：曆算底座
- [shengjidaguai-china/goutoujunshi](https://github.com/shengjidaguai-china/goutoujunshi)：可選協作對象，亦都係 skill 組織方式嘅參照

> 本項目唔構成醫療、心理、法律、財務建議。命理唔係預測事實，重要決定請以現實資訊同專業意見為準 (◕‿◕)
