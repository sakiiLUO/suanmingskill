# Contributing

欢迎补规则、补用例、补文献。这个项目最容易改坏的地方不是代码，而是**边界**——所以改动前请先读下面的约定。

## 快速开始

```bash
python -m unittest discover -s tests -v   # 必须全绿
python scripts/validate_skill.py           # 打包/引用/许可检查
python scripts/eval_dialogue.py            # 红队用例
```

内置 `vendor/lunar_python`（MIT），离线可跑；也可 `pip install -r requirements.txt`。

## 改什么、怎么改

| 想改 | 改哪里 | 必须加什么 |
| --- | --- | --- |
| 历法/排盘行为 | `scripts/paipan.py`、`scripts/solartime.py` | `tests/test_suanming.py` 里的回归或不变量 |
| 新增越界说法拦截 | `scripts/lint_reply.py` | `tests/cases/dialogue_cases.json` 用例（含“合规版本必须放行”） |
| 解读话术/领域规则 | 对应 `references/*.md` | 确认“只给什么/不给什么”仍完整 |
| 古籍或研究引用 | `references/11`、`references/12` | 必须实际抓取/核对，附来源链接；未核实的写进“不可引用” |
| 输出结构 | `SKILL.md` | 跑完整评测，确认结构检查仍通过 |

## 硬规则

1. **不伪造古籍原文**：只允许引用 `references/11` 收录的 8 条；表外只写“大意”。
2. **不混证据等级**：古籍断语 D 级、古籍体系 C 级、实证 A/B；不得把 D 写成 A。
3. **不引入来源不明的代码或语料**：新依赖必须有明确许可证（MIT/BSD/Apache），并写入 `NOTICE.md`。
4. **不碰版权内容**：现代点校本、译注、课程讲义、他人断语库不复制。
5. **规则改动必须有反例**：新增拦截规则时，同时加“合规版本不能被误拦”的用例（参考否定语境测试）。
6. **一次只改一处**：计算层、规则层、话术层分开提交，方便定位回归。

## 提交前检查

- [ ] `python -m unittest discover -s tests` 全绿
- [ ] `python scripts/validate_skill.py` 通过
- [ ] `python scripts/eval_dialogue.py` 全部符合期望
- [ ] 新增/修改的 references 有明确“不给什么”
- [ ] 无 `.suanming/`、密钥、真实用户生日等隐私数据进入 diff
