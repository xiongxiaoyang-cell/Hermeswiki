#!/usr/bin/env python3
"""
Wiki Compile — 从 wiki 组装报告/培训材料
用法：
  python3 wiki-compile.py --template assessment --country deguo --output report.md
  python3 wiki-compile.py --template policy-report --output report.md
  python3 wiki-compile.py --template training --topics eor,chuhai --output training.md
  python3 wiki-compile.py --template client-report --company "某科技公司" --countries deguo,yingguo --stage "1-10" --output report.md
"""
import sys
import json
import re
import argparse
from pathlib import Path
from datetime import datetime

WIKI_ROOT = Path.home() / "wiki"
WIKI_ENTITIES = WIKI_ROOT / "entities"
WIKI_CONCEPTS = WIKI_ROOT / "concepts"
WIKI_COMPARISONS = WIKI_ROOT / "comparisons"
WIKI_QUERIES = WIKI_ROOT / "queries"
OUTPUT_DIR = WIKI_ROOT / "_compiled"

# ============================================================
# 核心：加载 wiki 页面
# ============================================================
def load_page(slug: str) -> dict:
    """按 slug 加载 wiki 页面，返回 {slug, title, content, frontmatter}"""
    for dir_path in [WIKI_ENTITIES, WIKI_CONCEPTS, WIKI_COMPARISONS, WIKI_QUERIES]:
        f = dir_path / f"{slug}.md"
        if f.exists():
            raw = f.read_text(encoding="utf-8")
            fm, content = parse_frontmatter(raw)
            return {
                "slug": slug,
                "file": str(f.relative_to(WIKI_ROOT)),
                "title": fm.get("title", slug),
                "type": fm.get("type", "unknown"),
                "tags": fm.get("tags", []),
                "confidence": fm.get("confidence", "medium"),
                "sources": fm.get("sources", []),
                "created": fm.get("created", ""),
                "updated": fm.get("updated", ""),
                "content": content.strip(),
                "content_lines": content.strip().split("\n"),
            }
    return None


def parse_frontmatter(raw: str) -> tuple:
    """解析 markdown 文件，返回 (frontmatter_dict, content_str)"""
    if raw.startswith("---"):
        parts = raw.split("---", 2)
        if len(parts) >= 3:
            import yaml
            try:
                fm = yaml.safe_load(parts[1]) or {}
                return fm, parts[2]
            except Exception:
                pass
    return {}, raw


# ============================================================
# 模板 1：出海潜客评估报告
# ============================================================
def template_assessment(company: str, stage: str, target_countries: list,
                        pain_points: str, budget: str, urgency: str) -> str:
    """生成出海潜客评估报告"""
    today = datetime.now().strftime("%Y-%m-%d")

    # 加载相关 country entities
    countries = []
    for code in target_countries:
        p = load_page(code)
        if p:
            countries.append(p)

    # 加载出海三阶段框架
    stage_page = load_page("chuhai-san-jieduan")
    eor_page = load_page("eor-fuwu")
    assess_table = load_page("chuhai-pinggu")

    # 评分
    stage_scores = {"0-1": 10, "1-10": 15, "成熟期": 18, "全球化": 20}
    country_scores = {"deguo": 20, "yingguo": 20, "faguo": 18, "helan": 18,
                      "xibanya": 16, "yidali": 16, "bolan": 15, "shate": 14,
                      "xinjapo": 17, "yuenan": 16, "taiguo": 15, "riben": 16,
                      "hanguo": 14, "baxi": 13, "meiguo": 17, "jianada": 16}
    country_region = {
        "deguo": "西欧", "yingguo": "西欧", "faguo": "西欧", "helan": "西欧",
        "xibanya": "南欧", "yidali": "南欧", "bolan": "中东欧", "shate": "中东",
        "xinjapo": "东南亚", "yuenan": "东南亚", "taiguo": "东南亚", "riben": "东亚",
        "hanguo": "东亚", "baxi": "拉美", "meiguo": "北美", "jianada": "北美"
    }

    total = 0
    dims = []

    # 出海阶段得分
    ss = stage_scores.get(stage, 12)
    total += ss
    dims.append(("出海阶段", ss, f"{stage}期"))

    # 目标市场得分
    cs = sum(country_scores.get(c, 15) for c in target_countries) // max(1, len(target_countries))
    total += cs
    dims.append(("目标市场", cs, ", ".join(country_region.get(c, "其他") for c in target_countries)))

    # 核心痛点
    pain_score = {"合规": 18, "招聘": 16, "薪酬": 14, "签证": 14}.get(pain_points, 12)
    total += pain_score
    dims.append(("核心痛点", pain_score, pain_points))

    # 预算
    budget_score = {"高": 18, "中": 14, "低": 8}.get(budget, 12)
    total += budget_score
    dims.append(("预算", budget_score, budget))

    # 紧迫度
    urgency_score = {"高": 18, "中": 14, "低": 8}.get(urgency, 12)
    total += urgency_score
    dims.append(("紧迫度", urgency_score, urgency))

    verdict = "优质潜客" if total >= 80 else "一般潜客" if total >= 60 else "低优先级"

    lines = [
        f"# 出海HR潜客评估报告",
        f"",
        f"**客户：** {company}",
        f"**评估日期：** {today}",
        f"**评级：** {verdict}（{total}/120分）",
        f"",
        f"---",
        f"",
        f"## 六维度评分",
        f"",
        f"| 维度 | 得分 | 备注 |",
        f"|------|------|------|",
    ]
    for name, score, note in dims:
        bar = "▓" * (score // 4) + "░" * (5 - score // 4)
        lines.append(f"| {name} | {score}/20 {bar} | {note} |")

    lines += ["", f"**总分：{total}/120**", ""]

    if countries:
        lines += [
            "## 目标市场详情",
            "",
        ]
        for c in countries:
            lines.append(f"### {c['title']}（[[{c['slug']}]]）")
            # 提取基本信息表格
            for line in c["content_lines"]:
                if line.startswith("|") and ("最低工资" in line or "区域" in line or "出海阶段" in line):
                    lines.append(line)
            # 提取最近重大更新（前3条）
            recent = []
            capture = False
            for line in c["content_lines"]:
                if re.match(r"#{2,3} \d{4}-\d{2}-\d{2}", line.strip()):
                    capture = True
                    recent = [line]
                elif capture and line.startswith("|"):
                    recent.append(line)
                    if len(recent) > 5:
                        capture = False
                elif capture and line.strip() == "":
                    capture = False
            if recent:
                lines += recent[:5]
            lines.append("")

    if eor_page:
        section = _extract_section(eor_page["content"], "四模式对比")
        lines += [
            "## EOR服务适用性分析",
            "",
        ]
        if section:
            lines.extend(section)
        else:
            lines.extend(eor_page["content_lines"][:15])
        lines += ["", ""]

    if assess_table:
        lines += [
            "## 锴哥评估标准参考",
            "",
            f"优质潜客：80+分 | 一般潜客：60-80分 | 低优先级：<60分",
            f"",
            f"> 西欧（德英法荷等）比东南亚更重要，是锴哥基于实际业务经验的判断。",
            "",
        ]

    lines += [
        "---",
        f"",
        f"**编制：** 锴哥出海HR知识库 | **{today}**",
        f"**数据来源：** wiki知识库（{', '.join(target_countries)} entity页 + 出海评估框架）",
        f"**免责声明：** 本报告基于公开政策数据整理，具体数值以官方发布为准。",
    ]

    return "\n".join(lines)


# ============================================================
# 模板 2：HR政策合规周报
# ============================================================
def template_policy_report(countries: list, days: int = 7) -> str:
    """生成HR政策合规周报"""
    today = datetime.now().strftime("%Y-%m-%d")
    pages = []

    # 加载 hr-policy-daily
    daily = load_page("hr-policy-daily")
    if daily:
        pages.append(daily)

    # 加载国家 entity
    for code in countries:
        p = load_page(code)
        if p:
            pages.append(p)

    lines = [
        f"# 全球HR政策合规简报",
        f"",
        f"**覆盖：** {', '.join(p['title'] for p in pages if p)}",
        f"**周期：** 近{days}天",
        f"**编制日期：** {today}",
        f"",
        f"---",
        "",
    ]

    # 按严重度分类重大变化
    red_items = []
    yellow_items = []
    green_items = []

    for page in pages:
        if not page:
            continue
        for line in page["content_lines"]:
            m = re.search(r"(🔴|🟡|🟢)\s*\*+\*\*[^*]+\*\*[^*]*\*\*[^*]*\*\*\s*[-—]\s*(.+?)\s*[-—]\s*(.+?)(?:\n|$)", line)
            if m:
                severity = m.group(1)
                policy_type = m.group(2).strip()
                desc = m.group(3).strip()
                item = f"- **{page['title']}** | {policy_type} | {desc[:80]}"
                if severity == "🔴":
                    red_items.append(item)
                elif severity == "🟡":
                    yellow_items.append(item)
                else:
                    green_items.append(item)

    if red_items:
        lines += ["## 🔴 重大变化（需立即处理）", ""] + red_items + [""]
    if yellow_items:
        lines += ["## 🟡 政策公告（关注生效日期）", ""] + yellow_items + [""]
    if green_items:
        lines += ["## 🟢 常规更新", ""] + green_items[:10] + [""]
    if not red_items and not yellow_items and not green_items:
        lines += ["*本周无重大政策变化。*", ""]

    # 各国最低工资快照
    lines += [
        "## 最低工资快照（2026年）",
        "",
        "| 国家 | 最低工资 | 生效日期 | 备注 |",
        "|------|---------|---------|------|",
    ]

    for code in countries:
        p = load_page(code)
        if not p:
            continue
        minwage = "—"
        effective = "—"
        for line in p["content_lines"]:
            if "最低工资" in line and "€" in line or "£" in line or "¥" in line or "RM" in line or "SAR" in line or "JPY" in line:
                # 提取数字
                mw = re.findall(r"(?:€|£|¥|RM|SAR|USD|JPY|PLN|HUF|KRW)\s*[\d,]+(?:\.\d+)?/?小时|/月|/天", line)
                if mw:
                    minwage = mw[0]
                eff_m = re.search(r"(\d{4}[-/]\d{2}[-/]\d{2})", line)
                if eff_m:
                    effective = eff_m.group(1)
        if minwage != "—":
            lines.append(f"| {p['title']} | {minwage} | {effective} | {p.get('updated', '')} |")

    lines += [
        "",
        "---",
        f"",
        f"**编制：** 锴哥出海HR知识库 | {today}",
        f"**数据来源：** [[hr-policy-daily]] 全球HR政策日报",
    ]

    return "\n".join(lines)


# ============================================================
# 模板 3：客户培训材料
# ============================================================
def template_training(topics: list, title: str = "出海HR实战培训") -> str:
    """生成培训材料"""
    today = datetime.now().strftime("%Y-%m-%d")
    topic_pages = [load_page(t) for t in topics]
    topic_pages = [p for p in topic_pages if p]

    lines = [
        f"# {title}",
        f"",
        f"**编制日期：** {today}",
        f"**课时：** 约{len(topic_pages) * 0.5:.1f}小时",
        f"",
        f"---",
        "",
    ]

    topic_names = {
        "chuhai-san-jieduan": "一、出海三阶段模型",
        "eor-fuwu": "二、EOR用工模式全解",
        "hegui-fengkong": "三、合规风控四原则",
        "quyu-guihua": "四、区域合规政策",
        "zhaopin": "五、海外招聘策略",
        "xinchou": "六、薪酬体系设计",
        "zuzhi-jiagou": "七、组织架构搭建",
    }

    for i, topic in enumerate(topics):
        page = load_page(topic)
        if not page:
            continue
        heading = topic_names.get(topic, f"模块{chr(65+i)}：{topic}")
        lines += [
            f"## {heading}",
            "",
        ]

        # 提取主要段落（跳过相关页面section）
        content = page["content"]
        in_section = True
        for line in content.split("\n"):
            if line.startswith("## 相关页面"):
                in_section = False
            if in_section and line.strip():
                lines.append(line)
        lines.append("")
        lines.append(f"*参考：[[{page['slug']}]]*")
        lines.append("")

    lines += [
        "---",
        f"",
        f"**培训目标：**",
        f"1. 理解出海HR三阶段模型，明确当前所处阶段",
        f"2. 掌握EOR/IC/自雇佣/外派四种模式的适用场景",
        f"3. 建立合规风控意识，了解主要合规风险点",
        f"4. 熟悉目标市场基本政策（最低工资/社保/签证）",
        "",
        f"**参考资料：** {', '.join('[['+p['slug']+']]' for p in topic_pages if p)}",
        f"",
        f"**编制：** 锴哥出海HR知识库 | {today}",
    ]

    return "\n".join(lines)


# ============================================================
# 模板 4：客户综合报告（基于公司情况）
# ============================================================
def template_client_report(company: str, countries: list, stage: str,
                           employees: str, pain_point: str, output_format: str = "md") -> str:
    """生成客户综合咨询报告"""
    today = datetime.now().strftime("%Y-%m-%d")
    pages = [load_page(c) for c in countries]
    pages = [p for p in pages if p]

    eor = load_page("eor-fuwu")
    stage_m = load_page("chuhai-san-jieduan")

    lines = [
        f"# {company} 出海HR战略咨询报告",
        "",
        f"**委托客户：** {company}",
        f"**目标市场：** {', '.join(p['title'] for p in pages)}",
        f"**出海阶段：** {stage}",
        f"**人员规模：** {employees}",
        f"**核心痛点：** {pain_point}",
        f"**报告日期：** {today}",
        "",
        "---",
        "",
    ]

    # 出海阶段与模式选择
    if stage_m:
        lines += [
            "## 一、出海阶段与模式选择",
            "",
        ]
        content = stage_m["content"]
        for line in content.split("\n"):
            if line.startswith("## 相关页面"):
                break
            if line.strip():
                lines.append(line)
        lines.append("")

    # 四模式对比（聚焦目标市场）
    if eor:
        lines += [
            "## 二、用工模式对比",
            "",
            "### 四种模式速览",
            "",
        ]
        capture = False
        for line in eor["content_lines"]:
            if "四模式对比" in line:
                capture = True
            if capture and line.startswith("## EOR vs"):
                break
            if capture and line.strip():
                lines.append(line)
        lines.append("")
        lines.append("### EOR适用性判断")
        lines.append("")
        lines.append("基于出海阶段和工作模式，给出推荐：")
        lines.append("")
        if stage in ["0-1", "试水期"]:
            lines.append("**推荐：EOR** — 最快合规落地，无需设立主体，1-2周即可开始招聘。")
        elif stage in ["1-10", "增长期"]:
            lines.append("**推荐：EOR + IC混合** — 核心岗位EOR，灵活岗位IC，控制成本与合规风险。")
        else:
            lines.append("**推荐：自雇佣为主** — 规模成熟，建立当地主体，深层管控团队。")
        lines.append("")

    # 国别详情
    for p in pages:
        region = next((t for t in p.get("tags", []) if t in ["西欧", "东南亚", "中东", "北美", "拉美", "东亚", "南欧", "中东欧"]), "其他")
        lines += [
            f"## 三、{p['title']}市场详情（[[{p['slug']}]]）",
            "",
            f"**区域：** {region}",
            "",
            f"### 最低工资与社保",
            "",
        ]

        for line in p["content_lines"]:
            if ("最低工资" in line or "社保" in line) and line.startswith("|"):
                lines.append(line)
            if "工作签证" in line and line.startswith("|"):
                lines.append(line)

        lines += [
            "",
            f"### 近期重大政策变化",
            "",
        ]

        # 提取最近2条时间线
        timeline = []
        capture = False
        for line in p["content_lines"]:
            if re.match(r"#{2,3} \d{4}-\d{2}-\d{2}", line.strip()):
                if timeline:
                    break
                capture = True
                timeline.append(line)
            elif capture and line.strip():
                timeline.append(line)
                if len(timeline) > 8:
                    capture = False

        lines.extend(timeline[:6] if timeline else ["*暂无重大变化记录。*"])
        lines.append("")

    # 下一步建议
    lines += [
        "## 四、下一步行动建议",
        "",
    ]

    if stage in ["0-1", "试水期"]:
        next_steps = [
            "1. **市场验证（2-4周）**：通过EOR快速进入目标市场，招聘首批1-3名本地员工",
            "2. **合规摸底（同步）**：由EOR服务商协助完成当地社保、税务登记",
            "3. **签证准备（如需）**：确认核心岗位签证资质，备齐申请材料",
            "4. **招聘启动（第3周起）**：在EOR平台上发布职位，同步对接用友薪福社EOR服务",
        ]
    elif stage in ["1-10", "增长期"]:
        next_steps = [
            "1. **模式优化（1-2周）**：评估现有EOR合同，考虑增设IC合作模式",
            "2. **招聘升级**：从EOR平台转向本地猎头，聚焦中高端岗位",
            "3. **HR体系搭建**：建立当地HR制度流程，对接总部HR系统",
            "4. **合规深化**：聘请当地法律顾问，处理劳动法合规问题",
        ]
    else:
        next_steps = [
            "1. **主体设立（3-6个月）**：评估在当地设立子公司的可行性",
            "2. **人员平移**：将EOR员工平移至自雇佣体系",
            "3. **全球HR整合**：建立全球HR管理系统，统一薪酬绩效标准",
        ]

    lines.extend(next_steps)
    lines += [
        "",
        "---",
        "",
        f"**本报告由锴哥出海HR知识库编制** | {today}",
        f"**免责声明：** 本报告仅供参考，不构成法律或合规建议。具体政策以当地官方发布为准。",
    ]

    return "\n".join(lines)


# ============================================================
# 工具函数
# ============================================================
def _extract_section(content: str, heading: str) -> list:
    """提取 content 中以 heading 开头的 section 行"""
    lines = []
    capture = False
    for line in content.split("\n"):
        if line.strip() == heading or line.strip().startswith(heading):
            capture = True
            lines.append(line)
        elif capture:
            if line.startswith("## ") or (line.strip() and not lines[-1].startswith("#")):
                pass
            if line.strip() == "":
                continue
            lines.append(line)
    return lines[:20]


def export_markdown(content: str, output_path: Path):
    """导出 markdown"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    print(f"  ✓ 导出：{output_path}")


# ============================================================
# 主入口
# ============================================================
def main():
    parser = argparse.ArgumentParser(description="Wiki Compile — 从 wiki 组装报告")
    parser.add_argument("--template", "-t", required=True,
                        choices=["assessment", "policy-report", "training", "client-report"],
                        help="模板类型")
    parser.add_argument("--output", "-o", help="输出文件路径")
    parser.add_argument("--company", help="公司名称（assessment/client-report）")
    parser.add_argument("--countries", help="国家代码，逗号分隔（deguo,yuenan）")
    parser.add_argument("--stage", help="出海阶段（assessment/client-report）")
    parser.add_argument("--pain-point", help="核心痛点（assessment/client-report）")
    parser.add_argument("--budget", help="预算高低（assessment）")
    parser.add_argument("--urgency", help="紧迫度高/中/低（assessment）")
    parser.add_argument("--employees", help="人员规模（client-report）")
    parser.add_argument("--topics", help="培训主题，逗号分隔（eor,chuhai）")
    parser.add_argument("--days", type=int, default=7, help="政策日报天数")
    parser.add_argument("--title", help="培训材料标题")
    args = parser.parse_args()

    today = datetime.now().strftime("%Y%m%d")

    if args.template == "assessment":
        countries = args.countries.split(",") if args.countries else ["deguo", "yingguo"]
        content = template_assessment(
            company=args.company or "某公司",
            stage=args.stage or "1-10",
            target_countries=countries,
            pain_points=args.pain_point or "合规",
            budget=args.budget or "中",
            urgency=args.urgency or "中",
        )
        fname = args.output or f"{today}_潜客评估_{args.company or '某公司'}.md"

    elif args.template == "policy-report":
        countries = args.countries.split(",") if args.countries else ["yingguo", "deguo", "yuenan"]
        content = template_policy_report(countries, args.days)
        fname = args.output or f"{today}_HR政策简报.md"

    elif args.template == "training":
        topics = args.topics.split(",") if args.topics else ["chuhai-san-jieduan", "eor-fuwu"]
        content = template_training(topics, args.title or "出海HR实战培训")
        fname = args.output or f"{today}_培训材料.md"

    elif args.template == "client-report":
        countries = args.countries.split(",") if args.countries else ["deguo", "yingguo"]
        content = template_client_report(
            company=args.company or "某公司",
            countries=countries,
            stage=args.stage or "1-10",
            employees=args.employees or "待定",
            pain_point=args.pain_point or "合规",
        )
        fname = args.output or f"{today}_{args.company or '某公司'}_咨询报告.md"

    output_path = Path(fname)
    export_markdown(content, output_path)

    # 同步记录到 log.md
    log_path = WIKI_ROOT / "log.md"
    log_entry = f"\n## {today} — Wiki Compile\n"
    log_entry += f"- 模板：{args.template}\n"
    log_entry += f"- 输出：{fname}\n"
    if log_path.exists():
        existing = log_path.read_text()
        log_path.write_text(existing.rstrip() + log_entry)
    else:
        log_path.write_text(log_entry)

    print(f"\n完成：{fname}")


if __name__ == "__main__":
    main()
