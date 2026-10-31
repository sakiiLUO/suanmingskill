# GitHub 仓库元数据（Description / Website / Topics）

> 用途：仓库首页右侧 About 区域的三个字段。GitHub 没有原生 API 之外的“文件配置”，
> 这三个值只能在 Settings 或 API 里设置；本页给出可直接复制的文案与命令。

## 一、Description（三选一）

**推荐：中英混排（中文优先，尾部带英文关键词，利于搜索）**

```text
八字 · 紫微 · 六爻排盘与解读 Agent Skill：真太阳时校正、双人合盘、大运流年、长期维护建议；只给可验证的假设与边界，不断生死/疾病/投资。BaZi · Zi Wei · Liu Yao skill for AI agents (MIT).
```

**纯中文（更短，首页显示更完整）**

```text
八字·紫微·六爻的 AI 排盘与解读 Skill：真太阳时校正、合盘、大运流年、长期维护建议；只给假设与边界，不做生死/疾病/投资断言。
```

**纯英文**

```text
A BaZi / Zi Wei / Liu Yao divination skill for AI agents: true-solar-time charts, compatibility, annual cycles and long-term advice — hypotheses and boundaries only, never life/death, health or investment claims. MIT.
```

> 长度都远低于 350 字符上限；首页显示约 160 字符，所以把“是什么”放最前面。

## 二、Website

没有独立官网时，建议填 README 锚点（点进去直接是文档）：

```text
https://github.com/sakiiLUO/suanmingskill#readme
```

也可以留空——留空不会减分，只是少一个入口。若以后有文档站（如 GitHub Pages），改成站点根地址。

## 三、Topics（18 个，直接复制）

```text
bazi, four-pillars, ziwei-doushu, liuyao, iching, chinese-metaphysics, fortune-telling, divination, lunar-calendar, true-solar-time, agent-skills, claude-skills, codex-skills, dsh, ai-agents, llm, python, i18n
```

分组的考量：

| 组 | topics | 作用 |
| --- | --- | --- |
| 术数本体 | `bazi` `four-pillars` `ziwei-doushu` `liuyao` `iching` `chinese-metaphysics` `fortune-telling` `divination` | 让“算命/命理”相关搜索命中 |
| 技术点 | `lunar-calendar` `true-solar-time` | 差异化：真太阳时与历法正确性 |
| Skill 生态 | `agent-skills` `claude-skills` `codex-skills` `dsh` | 被找 skill 的人发现 |
| 通用 | `ai-agents` `llm` `python` `i18n` | 扩大触达 |

GitHub 规则：最多 20 个、每个 ≤50 字符、只能小写字母/数字/连字符。

## 四、怎么设置

### 网页

1. 仓库页 → 右侧 About 的齿轮 ⚙️
2. 填 Description、Website；Topics 输入后按回车逐个添加，最后 **Save changes**

### API（需要 PAT，`repo` 或细粒度 Administration: Read and write）

**坑：`PATCH /repos/{owner}/{repo}` 不接受 `topics`**——传了会返回 200，但 topics 不变。
Topics 必须用专门的 `PUT /repos/{owner}/{repo}/topics`，字段名是 `names` 而不是 `topics`。

```bash
export GITHUB_TOKEN=ghp_xxx

# 1) 描述 + 主页
curl -X PATCH https://api.github.com/repos/sakiiLUO/suanmingskill \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -d '{
    "description": "八字 · 紫微 · 六爻排盘与解读 Agent Skill：真太阳时校正、双人合盘、大运流年、长期维护建议；只给可验证的假设与边界，不断生死/疾病/投资。BaZi · Zi Wei · Liu Yao skill for AI agents (MIT).",
    "homepage": "https://github.com/sakiiLUO/suanmingskill#readme"
  }'

# 2) Topics（注意是 PUT + names）
curl -X PUT https://api.github.com/repos/sakiiLUO/suanmingskill/topics \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -d '{"names":["bazi","four-pillars","ziwei-doushu","liuyao","iching","chinese-metaphysics","fortune-telling","divination","lunar-calendar","true-solar-time","agent-skills","claude-skills","codex-skills","dsh","ai-agents","llm","python","i18n"]}'
```

### GitHub CLI

```bash
gh repo edit sakiiLUO/suanmingskill \
  --description "八字 · 紫微 · 六爻排盘与解读 Agent Skill：真太阳时校正、双人合盘、大运流年、长期维护建议；只给可验证的假设与边界。" \
  --homepage "https://github.com/sakiiLUO/suanmingskill#readme" \
  --add-topic bazi --add-topic four-pillars --add-topic ziwei-doushu --add-topic liuyao --add-topic iching \
  --add-topic chinese-metaphysics --add-topic fortune-telling --add-topic divination --add-topic lunar-calendar \
  --add-topic true-solar-time --add-topic agent-skills --add-topic claude-skills --add-topic codex-skills \
  --add-topic dsh --add-topic ai-agents --add-topic llm --add-topic python --add-topic i18n
```

## 五、设置后怎么验证

```bash
curl -sS https://api.github.com/repos/sakiiLUO/suanmingskill | python -c "import json,sys; d=json.load(sys.stdin); print(d['description']); print(d['homepage']); print(', '.join(d['topics']))"
```

期望输出：描述非空、homepage 指向 README、topics 含 18 项。

## 六、加分项（不在字段里，但影响点击率）

1. **Social preview**：Settings → Social preview 上传 1280×640 图（建议：左边「算命 skill」字样，右边一张排盘卡片截图）。
2. **Pin 仓库**：账号主页 Pin 上这个仓库。
3. **README 首屏**：已有徽章与「你可能想这么问」，保持前 10 行不出现长表格即可。
4. **Release**：给 v0.4.0 打一个 tag，Release note 直接复用 CHANGELOG 段落。

## 已设置（2026-10-31）

三项已通过 API 设置并验证（页面 About 区域可见）：

- Description：中英混排版
- Homepage：`https://github.com/sakiiLUO/suanmingskill#readme`
- Topics：18 个（`agent-skills` … `ziwei-doushu`，页面已渲染为 topic 标签）

验证方式：`curl -sSL https://github.com/sakiiLUO/suanmingskill | grep -o '/topics/[a-z0-9-]*' | sort -u`（公开 API 的 `topics` 字段有 CDN 缓存延迟，页面 HTML 是准的）。