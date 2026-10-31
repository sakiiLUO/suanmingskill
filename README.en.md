# Fortune-Telling Skill (suanming) (｡･ω･｡)ﾉ♡

> A standalone **BaZi charting and interpretation** Agent Skill — get the chart right, say it plainly, and make the boundaries non-negotiable ᕕ( ᐛ )ᕗ

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Tests](https://img.shields.io/badge/tests-53%20passing-brightgreen.svg)
[![Python](https://img.shields.io/badge/python-3.10%2B-3776AB.svg)](https://www.python.org/)
![Good Vibes](https://img.shields.io/badge/vibes-%E5%8F%8B%E5%A5%BD%E4%B8%8D%E5%90%93%E4%BA%BA-ff69b4.svg)

<!-- LANGS:START -->
[简体中文](README.md) · [繁體中文](README.zh-TW.md) · [粵語](README.yue.md) · [日本語](README.ja.md) · **English**
<!-- LANGS:END -->

> This page is a translation; if it differs from the Simplified Chinese README, the Simplified Chinese version prevails.

---

## Hi, Start Here (◕‿◕)

This is a **skill** for AI agents: `SKILL.md` handles *how to talk*, `references/` holds cheat sheets you can look up on demand, and `scripts/` is the Python that actually computes the chart.

It isn't scary, and it doesn't play the mystic:

- First it honestly **casts the chart** (true solar time, daylight saving time, the late-Zi hour (晚子时), and solar-term boundaries all handled)
- Then it gives you "**chart facts → boundaries and uncertainty → 2–3 evidence-backed hypotheses → one small testable action**"
- Finally it reminds you: **this is an interpretive framework, not a prediction.** The decisions are still yours (｡･ω･｡)ﾉ♡

> The "should I stay, and how do I reply to that?" side of relationships can go to [Goutou Junshi](https://github.com/shengjidaguai-china/goutoujunshi), but this skill **works fine on its own by default** — it doesn't require it.

## Things You Might Want to Ask 💬

```text
“Read my fortune, would you～”
“What job am I actually suited for? (´･ω･`)”
“Will I pass the exam this year? And don't sugarcoat it.”
“Are my partner and I compatible?”
“Why does my mom keep picking fights with me?”
“Is this stuff even scientific?”
“Am I a husband-killer...”      ← this one gets gently taken apart
```

## How It Answers You ✨

```text
Chart facts: true solar time 1995-08-17 14:26, Four Pillars (四柱) Yi-Hai, Jia-Shen, Geng-Chen, Gui-Wei; day master (日主) Geng metal, month command (月令) Shen metal;
          currently in the Xin-Si major cycle (大运, 2018–2027), with 2026 as the Bing-Wu annual pillar (流年).
Boundaries and uncertainty: the birth time is well away from the Wei/Shen hour boundary, so the hour pillar is stable; the birth did not fall in the 1986–1991 daylight saving period.
Hypothesis (not a verdict): a Geng-metal day master in a Shen-metal month is usually read as someone who carries things alone first and dislikes showing weakness.
The opposite is possible too: it could be a habit formed by being made to be independent early, rather than temperament.
Testable small action: think back over your last three stressful events — did you go find someone to talk it over, or digest it yourself first?
               If you digested all three yourself, this reading fits you better.
The above is an interpretive framework, not a prediction (・∀・)
```

See? **Every "conclusion" comes with evidence, a reverse possibility, and something you can verify** — the word "destined" never shows up (๑•̀ㅂ•́)و✧

## What It Can Look At ⭐

| What you want to discuss | What it will discuss | What it deliberately steers around |
| --- | --- | --- |
| Personality, behavioral patterns | 2–3 evidence-backed hypotheses | Verdicts on strong/weak day master (身强身弱) or favorable elements (用神喜忌) |
| Career, professional direction | Work style, organizational fit, timing windows | Specific industries or companies, investment targets |
| Study, exams | Learning style, stress rhythm | Scores, admissions, odds of passing |
| Body, anxiety | Stress responses, sleep and routine, where to get help | Diagnosis, disease prediction, advice to stop medication |
| Parents, children, family | Family roles, boundary issues | A third party's lifespan, health, or divorce |
| Romance, compatibility | 7 dimensions plus evidence | A ruling on "will it work out" |
| Major cycles and years, timing | Timing-window hypotheses plus signals to watch | Exact dates of events, auspicious or inauspicious pronouncements |
| "Is this scientific?" | Classical sources plus A/B/C/D evidence grading | Dressing experiential claims up as scientific findings |

## It Can Also Give You a Line of Scripture (｡•̀ᴗ-)✧

Sometimes you don't need more analysis, just one sentence with some weight behind it. It picks a passage from the *Tao Te Ching*, the *Analects*, the *Heart Sutra*, or the *Bible* (Chinese Union Version), adds a plain-language reading, and brings it back to your situation:

```text
Tao Te Ching, chapter 23: “A whirlwind does not last the morning; a sudden rainstorm does not last the day.”
Meaning: no matter how fierce the wind and rain, they don't blow all day.
For your situation — the pain does have a limit, but the limit won't arrive on its own.
(This is not a prophecy, and you're free not to use it.)
```

The rules are hard-coded too: **one passage at a time, source always cited, no attempts to convert anyone, no hell / doomsday / retribution scare tactics, and never scripture as the basis for a prediction**. A Chinese translation of the Quran is still under copyright, so that one is only paraphrased in substance with a note (｀・ω・´)

## What It Doesn't Do 🚫

- No readings on life and death, lifespan, disease diagnosis, disasters, fetal sex, lawsuit outcomes, investment targets, or exam scores
- No "husband-killer / wife-killer" (克夫克妻), "hard fate / cheap fate" (命硬命贱), or "child destiny" (童子命); and no "luck-changing" for anyone, no paid disaster clearance
- Without consent, it won't analyze anyone else's health, lifespan, or private life
- No marriage matching or romance compatibility charts for minors
- When self-harm, domestic violence, or coercion comes up, it **stops the reading immediately** and checks on safety first

It even ships with a "pre-send self-check": if a reply contains phrases like "destined / bound to / husband-killer / bloodshed / consecrated / compatibility score of 87", they get flagged and rewritten (｀・ω・´)ｼ

## Install in Three Minutes (๑•̀ㅂ•́)و✧

```bash
git clone https://github.com/sakiiLUO/suanmingskill.git suanming
cp -r suanming ~/.dsh/skills/        # keep the directory named suanming, matching the name in SKILL.md
```

| Host | Where to put it |
| --- | --- |
| DSH / DeepSeek Harness | `~/.dsh/skills/suanming/` (or `<repo>/.dsh/skills/suanming/` inside a project) |
| Claude Code | `~/.claude/skills/suanming/` |
| Codex | `~/.codex/skills/suanming/` |
| Other | Any agent that reads `SKILL.md` frontmatter will do |

It needs **Python 3.10+**. The calendar dependency `lunar-python` (MIT) is already bundled in `vendor/`, so it **works out of the box with no network access**; if you'd rather use pip: `pip install -r requirements.txt`.

## Too Lazy to Install It Yourself? Let AI Do It (っ•̀ω•́)っ

Copy the block below straight to your AI (Claude Code / Codex / DSH / Cursor all work) — it will clone, install, and run the tests on its own:

<!-- AI-INSTALL:START -->
```text
Please install this Agent Skill on my machine and verify it for me:
Repo: https://github.com/sakiiLUO/suanmingskill

1. First confirm the host and the skill directory; ask me if you're unsure:
   - DSH: ~/.dsh/skills/ (for project level use <repo>/.dsh/skills/)
   - Claude Code: ~/.claude/skills/
   - Codex: ~/.codex/skills/
2. Clone it into a temporary directory, then copy it to <skill目录>/suanming/; confirm that SKILL.md is at the root and that the frontmatter name is suanming.
3. Python 3.10+ is required; dependencies are already bundled in vendor/, do not pip install them globally.
4. Verify: cd <skill目录>/suanming && python -m unittest discover -s tests && python scripts/validate_skill.py
5. Report: where it was installed, the Python version, how many tests passed, and whether anything failed.

Constraints: do not modify the repo source; do not use admin/sudo privileges; do not install packages globally; do not skip verification; if any step fails, stop and tell me the reason and how to roll back (just delete <skill目录>/suanming/).
```
<!-- AI-INSTALL:END -->

Want to confirm it's really working after the install? Open a new session and say "Read my fortune" — it should ask for your birthday, time, city, and sex first instead of making things up (๑•̀ㅂ•́)و✧

To just check whether it's installed properly, use this one:

```text
Check whether the suanming skill is properly installed on this machine: locate <skill目录>/suanming/SKILL.md,
run python -m unittest discover -s tests, and tell me the path and the result; if it isn't installed, say so — don't install it yourself.
```

**After install**

- Activation: DSH hot-reloads; Claude Code usually needs no restart; **Codex requires a restart**.
- On Windows a junction (`mklink /J`) needs no admin rights — but **Codex skips symlinks**, so give Codex a real copy.
- Keep the folder name `suanming` (matching `name` in `SKILL.md`).
- If the network fails, stop and retry — don't fall back to `sudo` or a global `pip install`.

## Using It (ﾉ´ヮ`)ﾉ*: ･ﾟ

```bash
# Cast a chart (brief mode is handy for pasting straight into an answer)
python scripts/paipan.py --birth "1995-08-17 14:30" --gender male --city 杭州 --format brief

# Compatibility (for when you want to see how two people get along)
python scripts/paipan.py --birth "1995-08-17 14:30" --gender male   --city 杭州 --save .suanming/a.json
python scripts/paipan.py --birth "1996-03-08 09:15" --gender female --city 北京 --save .suanming/b.json
python scripts/hepan.py --a-json .suanming/a.json --b-json .suanming/b.json

# Run the self-check after drafting a reply, so you don't overstate
python scripts/lint_reply.py --file draft.md
```

Then in the conversation just say: *“Read my fortune”*, *“What work suits me”*, *“Are we compatible?”* — and you're all set～

## 🔍 Why This Layer Can Be Trusted

Jokes aside, **the chart-casting layer is serious**:

| Layer | Approach | Verification |
| --- | --- | --- |
| Calendar math | `lunar-python` (MIT) plus in-house rules for true solar time / daylight saving / late-Zi hour | 53 tests; includes the **GB/T 33661-2017 sexagenary day-cycle anchor** (1949-10-01 = Jia-Zi day) |
| Charting | True solar time (longitude difference + equation of time), 1986–1991 daylight saving, Start-of-Spring / solar-term boundary warnings | Pillar change at Start of Spring (立春), first and last DST days, late-Zi hour under both conventions |
| Speaking | Reply self-check: 20+ boundary rules plus structural checks | 34 red-team dialogue cases, all matching expectations |
| Citations | Classical texts: only 8 passages with verified wording, marked grade D; empirical studies marked A/B/C | `references/11`, `references/12` |

```bash
python -m unittest discover -s tests -v   # 53 tests
python scripts/validate_skill.py           # structure / citations / license / banned content
python scripts/eval_dialogue.py            # 34 red-team cases
```

## What's in the Repo 📦

```text
suanmingskill/                # repo root = skill root (install directory recommended: suanming)
├─ SKILL.md                   # behavioral core: the one file the model must read
├─ references/                # 14 on-demand files (incl. scripture and aphorisms): charting, Ten Gods,
│                             #   compatibility, timing windows, ethics, career, study, body and mind, family, classics, evidence grading, archive
├─ scripts/                   # paipan / hepan / solartime / archive /
│                             #   lint_reply / eval_dialogue / validate_skill
├─ tests/                     # 53 tests + 34 red-team cases
├─ vendor/lunar_python/       # unmodified MIT dependency (works offline)
├─ docs/                      # design notes: research, architecture, collaboration protocol, evaluation, test report
├─ agents/openai.yaml         # Codex display metadata (optional)
├─ NOTICE.md                  # third-party licenses and attribution
└─ .github/workflows/ci.yml   # CI: tests + validation + red team + smoke
```

## 📚 Literature and Evidence

- **Classical texts**: *Yuanhai Ziping*, *Sanming Tonghui*, *Ditiansui*, *Qiongtong Baojian*, *Ziping Zhenquan*, *Shenfeng Tongkao*, *Mingli Yueyan* — 7 titles, plus **8 verified verbatim passages** (each with a source link)
- **Empirical**: Forer 1949 (Barnum effect), Carlson 1985 (Nature double-blind test), Hartmann et al. 2006, Jurin 2026 preprint, Pugh 1983
- **Grading rules**: classical aphorisms grade D, classical systems grade C, empirical work A/B; **passing D off as A is forbidden** (｀・ω・´)

## Common Little Questions (・∀・)

**Q: Does it need the internet?**
No. The dependency is already in `vendor/`, and charting is fully local.

**Q: Does it cost money?**
No, MIT. Use it however you like, just keep the attribution.

**Q: Will my birthday be uploaded?**
No. All computation is local; saving an archive requires your explicit consent (`--consent`), and you can inspect or delete it at any time.

**Q: Can it do Zi Wei Dou Shu / Liu Yao / tarot?**
Not yet. Zi Wei is on the roadmap (the plan is to use the MIT-licensed iztro through a Node subprocess); PRs welcome (๑•̀ㅂ•́)و✧

**Q: Will it suddenly tell me "you are destined to..."?**
No. `scripts/lint_reply.py` blocks it, and `SKILL.md` hard-codes a ban on deterministic wording.

**Q: Is it accurate?**
It says of itself: *“I won't claim my readings are accurate. The chart is computed; the interpretation is a hypothesis. Whether it's accurate depends on whether you can pick out the part that's useful to you.”* (´･ω･`)

**Q: Which languages are supported?**
Simplified Chinese, Traditional Chinese, Cantonese, Japanese and English. Ask in one of these and you get the same language back; anything else defaults to English.

## License

MIT. The bundled lunar-python is MIT as well; the original license is at `vendor/lunar_python-1.4.8.dist-info/LICENSE`; third-party notices are in `NOTICE.md`.

## Acknowledgements (｡･ω･｡)ﾉ♡

- [6tail/lunar-python](https://github.com/6tail/lunar-python): the calendar-math foundation
- [shengjidaguai-china/goutoujunshi](https://github.com/shengjidaguai-china/goutoujunshi): an optional collaboration partner and a reference for how the skill is organized

> This project does not constitute medical, psychological, legal, or financial advice. Fortune-telling is not the prediction of facts; for important decisions, rely on real-world information and professional opinion (◕‿◕)
