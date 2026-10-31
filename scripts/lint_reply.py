"""回复自检器：在把命理解读发给用户之前，先检查草稿是否越界。

为什么需要它：SKILL.md 里的“不许绝对化、不许断生死、不许承诺改运”是提示词约束，
模型偶尔仍会说过头。把规则做成可执行检查，至少能让“越界”在发送前被拦一次。

用法：
  python scripts/lint_reply.py --file draft.md
  python scripts/lint_reply.py --text "你注定..."
  python scripts/lint_reply.py --file draft.md --profile brief --json
退出码：0 = 通过（可能有 warning）；1 = 存在 block 级问题；2 = 输入错误。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Rule:
    rid: str
    severity: str  # block / warn
    pattern: str
    message: str
    suggestion: str


RULES: list[Rule] = [
    # A. 绝对化表述
    Rule("A1", "block", r"注定|铁定|百分之百|100\s*%|绝对会|必然会|必(破|发|离|死|病|灾|升|降|成|败)",
         "出现决定论表述", "改成“可能/倾向/从盘面看更像”，并补一句反向可能"),
    Rule("A2", "block", r"一定(不)?(会|能|要|是)|一定(升|发|结|离|分|死|病|破|成|败|赢|输)|肯定不会|绝不会|必会|逃不掉|跑不了",
         "出现“一定会/一定不会”", "给出条件句：在什么条件下更可能，什么信号出现就改判"),
    # B. 生死 / 疾病 / 灾祸 / 官司 / 性别
    Rule("B1", "block", r"寿元|死期|活不过|阳寿|大限将至|命不久|还能活|活\s*\d+\s*年|活到\s*\d+|剩\s*\d+\s*年",
         "涉及寿元/死期", "删除；说明本 skill 不做这类判断"),
    Rule("B2", "block", r"癌症|绝症|有病|确诊|诊断你|停药|不用看医生",
         "涉及疾病诊断", "改为建议就医，明确不替代医疗"),
    Rule("B3", "block", r"血光|车祸|牢狱|官司(必|一定)(胜|败)|判\s*\d+\s*年",
         "涉及灾祸/官司结果", "删除断言；只保留“现实风险要咨询专业人士”"),
    Rule("B4", "block", r"胎儿性别|生男生女|查男女|是男(孩|宝)|是女(孩|宝)|男宝|女宝",
         "涉及胎儿性别", "拒绝并说明原因"),
    Rule("B6", "block", r"(八字|命盘|盘面|盘上).{0,8}(显示|看出|说明|代表).{0,10}(病|虚|弱|不好|亏|癌)",
         "用命理做疾病暗示/诊断", "删除；说明命理无诊断能力，身体不适请就医"),
    Rule("B5", "block", r"彩票|股票代码|必涨|稳赚|投资标的|推荐买",
         "涉及具体投资", "拒绝给标的；只谈风险意识"),
    # R. 宗教恐吓 / 劝诱 / 冒充神意
    Rule("R1", "block", r"下地狱|地狱里|异教徒|不信就|信了才|信就能|改宗|皈依|报应你|神会惩罚|真主会惩罚|菩萨会惩罚",
         "用宗教恐吓或劝诱", "删除；经文只作文学与伦理引用，不劝诱、不恐吓"),
    Rule("R2", "block", r"神(告诉|说|指引)我|真主(启示|说)我|菩萨(托梦|说)我|经上说要你",
         "冒充神意/宗教权威", "改成“这句话常被用来……”，不替宗教发言"),
    # C. 污名化标签
    Rule("C1", "block", r"克夫|克妻|克父|克母|命硬|童子命|扫把星|天煞孤星|孤寡命|桃花劫",
         "使用污名化命理标签", "说明这是旧说法、有污名化风险，改说具体行为倾向"),
    # D. 改运/消费陷阱
    Rule("D1", "block", r"开光|法事|符咒|消灾|改运|转运|供奉|做法事",
         "承诺或推销“改运”", "删除；给现实替代（作息、沟通、专业帮助）"),
    Rule("D2", "warn", r"付费|收费|加微信|私聊|课程",
         "出现付费/引流话术", "删除；skill 不做交易"),
    # E. 伪精确
    Rule("E1", "block", r"(匹配度|合盘得分|缘分值|成功率)[^0-9]{0,8}\d+",
         "给出伪精确分数", "合盘只给维度、证据、置信度，不给总分"),
    # F. 操控 / PUA / 越界建议
    Rule("F1", "block", r"冷处理|欲擒故纵|制造嫉妒|服从测试|打压对方|PUA",
         "提供操控性策略", "删除；改为真实表达与双向筛选"),
    Rule("F2", "block", r"跟踪|偷看手机|查对方手机|私自查|查她|查他",
         "涉及跟踪/侵犯隐私", "删除；说明这是越界行为"),
    Rule("F3", "warn", r"你必须(分手|离婚|辞职|结婚)|直接分手|马上离婚",
         "替用户做重大决定", "改成“决定权在你”，并列出现实证据与可逆选项"),
    # G. 第三方隐私
    Rule("G1", "warn", r"对方的(健康|寿元|灾祸)|偷偷排|没告诉他就排",
         "涉及未经同意的第三方分析", "只做相处方式的讨论，不分析第三方健康/寿元"),
    # H. 格式与流程
    Rule("H1", "warn", r"(?i)TODO|待补充|占位",
         "草稿里有未完成内容", "补完或删除"),
]


# 结构检查：四段式的弱检测（不追求 100% 准确，只兜底“整段缺失”）
STRUCTURE_RULES = [
    ("S1", "缺“边界/不确定”说明",
     ["不确定", "边界", "口径", "可能变", "待核实", "不確定", "邊界", "不確実", "Boundaries", "uncertain"],
     "block", "补一段：时辰是否边界、夏令时是否命中、有没有口径差异"),
    ("S2", "缺“解释框架”声明",
     ["娱乐", "不是预测", "假设", "参考", "解释框架", "不是預測", "假設", "仮説", "解釈",
      "Hypothesis", "hypothesis", "interpretive", "not a prediction", "not a verdict"],
     "warn", "补一句“以上是解释框架，不是预测；以现实信息和你的判断为准”"),
    ("S3", "缺可验证动作",
     ["观察", "记录", "验证", "下次", "信号", "停止条件", "觀察", "可驗證", "検証",
      "small check", "One small check", "look back"],
     "warn", "给一个观察窗口和一个停止条件"),
]

# 拒绝语境：合规的拒绝回答会“点出”禁忌词（“寿元我不排”），不能因此误判。
# 同一行内出现这些标记时，该行的命理禁忌命中跳过。
NEGATION_MARKERS = (
    "不排", "不做", "无法", "拒绝", "不提供", "不预测", "不建议",
    "不涉及", "不属于", "不合适", "帮不了", "不收钱", "不收费", "不在我",
    "不会判断", "不会根据", "不会预测", "不会建议", "不会给", "不判断", "不预测", "不认为",
)
# 整段是拒绝/说明边界时，不再要求四段式中的“边界段”和“动作段”。
REFUSAL_MARKERS = ("不排", "不做", "拒绝", "帮不了", "不在我", "不提供")

BRIEF_REQUIRED = [
    ("B1", "简报缺“不确定”行", ["不确定"], "block"),
    ("B2", "简报缺“性质”行", ["性质", "仅供讨论"], "block"),
]


# 只按强标点切子句；顿号“、”属于同一句话的列举，不能把否定语境切断
SEGMENT_SPLIT = re.compile(r"[，,。；;：:！!？?]")


def _segments(line: str) -> list[tuple[int, int, str]]:
    """按标点切分句，用于判断“否定语境”的范围只覆盖所在的子句。"""
    out, start = [], 0
    for m in SEGMENT_SPLIT.finditer(line):
        out.append((start, m.start(), line[start:m.start()]))
        start = m.end()
    out.append((start, len(line), line[start:]))
    return [s for s in out if s[2].strip()]


def _negated(segments: list[tuple[int, int, str]], pos: int) -> bool:
    for start, end, seg in segments:
        if start <= pos < end:
            return any(mark in seg for mark in NEGATION_MARKERS)
    return False


def check_text(text: str, profile: str = "reply") -> dict:
    findings = []
    lines = text.splitlines()
    for rule in RULES:
        rx = re.compile(rule.pattern)
        for idx, line in enumerate(lines, 1):
            segments = _segments(line)
            for m in rx.finditer(line):
                if _negated(segments, m.start()):
                    continue  # 该子句本身是在拒绝/说明边界，允许出现禁忌词
                findings.append({
                    "id": rule.rid,
                    "severity": rule.severity,
                    "line": idx,
                    "match": m.group(0),
                    "message": rule.message,
                    "suggestion": rule.suggestion,
                    "text": line.strip()[:120],
                })
    if profile == "brief":
        for rid, msg, keys, sev in BRIEF_REQUIRED:
            if not any(k in text for k in keys):
                findings.append({"id": rid, "severity": sev, "line": 0, "match": "",
                                 "message": msg, "suggestion": "按 06-命理档案与交接协议.md 的模板补全",
                                 "text": ""})
    else:
        is_refusal = any(mark in text for mark in REFUSAL_MARKERS)
        for rid, msg, keys, sev, sug in STRUCTURE_RULES:
            if is_refusal and rid in {"S1", "S3"}:
                continue  # 纯拒绝回答不需要四段式
            if not any(k in text for k in keys):
                findings.append({"id": rid, "severity": sev, "line": 0, "match": "",
                                 "message": msg, "suggestion": sug, "text": ""})

    blocks = [f for f in findings if f["severity"] == "block"]
    warns = [f for f in findings if f["severity"] == "warn"]
    return {
        "ok": not blocks,
        "profile": profile,
        "stats": {"chars": len(text), "blocks": len(blocks), "warns": len(warns)},
        "findings": findings,
    }


def render(result: dict) -> str:
    out = []
    for f in result["findings"]:
        loc = f"第{f['line']}行" if f["line"] else "全文"
        out.append(f"[{f['severity'].upper():5}] {f['id']} {loc}：{f['message']}")
        if f["match"]:
            out.append(f"        命中：{f['match']}｜原文：{f['text']}")
        out.append(f"        改法：{f['suggestion']}")
    s = result["stats"]
    out.append("")
    out.append(f"结论：{'通过' if result['ok'] else '未通过'}（block {s['blocks']} / warn {s['warns']}，{s['chars']} 字）")
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="命理解读回复自检（发送前拦截越界表述）")
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", help="草稿文件路径")
    group.add_argument("--text", help="直接传入草稿文本")
    ap.add_argument("--profile", default="reply", choices=["reply", "brief"],
                    help="reply=完整回答；brief=给狗头军师的命理简报")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args(argv)

    if args.file:
        try:
            text = open(args.file, encoding="utf-8").read()
        except OSError as exc:
            print(f"读取失败：{exc}", file=sys.stderr)
            return 2
    else:
        text = args.text

    result = check_text(text, args.profile)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render(result))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())








