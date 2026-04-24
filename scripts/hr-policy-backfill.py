#!/usr/bin/env python3
"""
HR Policy Daily → Wiki Entity Pages 整合脚本
功能：
  1. 解析所有日报文件，提取各国政策条目
  2. 回填/更新 entity 页的"政策时间线" section
  3. 更新 concepts/hr-policy-daily.md 快照表
  4. 记录操作到 log.md

用法：python3 hr-policy-backfill.py [--dry-run]
"""
import re
import sys
from pathlib import Path
from datetime import datetime

# ============================================================
# 路径配置
# ============================================================
WIKI_ROOT = Path("/home/b4ac5686610a4ae2/wiki")
REPORTS_DIR = WIKI_ROOT / "raw/sources/03_区域政策/政策日报"
ENTITIES_DIR = WIKI_ROOT / "entities"
CONCEPTS_DIR = WIKI_ROOT / "concepts"
LOG_FILE = WIKI_ROOT / "log.md"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)
ENTITIES_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# 国家映射
# ============================================================
COUNTRY_TO_ENTITY = {
    "英国": "yingguo", "德国": "deguo", "法国": "faguo",
    "越南": "yuenan", "新加坡": "xinjapo", "泰国": "taiguo",
    "马来西亚": "malaixiya", "印度": "yindu", "日本": "riben",
    "沙特": "shate", "阿联酋": "ahlianda", "波兰": "bolan",
    "匈牙利": "xiongyali", "美国": "meiguo", "加拿大": "jianada",
    "墨西哥": "moxige", "韩国": "hanguo", "印尼": "yinni",
    "菲律宾": "feilvbin", "西班牙": "xibanya", "荷兰": "helan",
    "意大利": "yidali", "巴西": "baxi",
}

COUNTRY_NAMES = {
    "yingguo": "英国", "deguo": "德国", "faguo": "法国",
    "yuenan": "越南", "xinjapo": "新加坡", "taiguo": "泰国",
    "malaixiya": "马来西亚", "yindu": "印度", "riben": "日本",
    "shate": "沙特阿拉伯", "ahlianda": "阿联酋", "bolan": "波兰",
    "xiongyali": "匈牙利", "meiguo": "美国", "jianada": "加拿大",
    "moxige": "墨西哥", "hanguo": "韩国", "yinni": "印度尼西亚",
    "feilvbin": "菲律宾", "xibanya": "西班牙", "helan": "荷兰",
    "yidali": "意大利", "baxi": "巴西",
}

REGION = {
    "yingguo": "西欧", "deguo": "西欧", "faguo": "西欧",
    "yuenan": "东南亚", "xinjapo": "东南亚", "taiguo": "东南亚",
    "malaixiya": "东南亚", "yindu": "南亚", "riben": "东亚",
    "shate": "中东", "ahlianda": "中东", "bolan": "中东欧",
    "xiongyali": "中东欧", "meiguo": "北美", "jianada": "北美",
    "moxige": "拉美", "hanguo": "东亚", "yinni": "东南亚",
    "feilvbin": "东南亚", "xibanya": "南欧", "helan": "西欧",
    "yidali": "南欧", "baxi": "拉美",
}

REGION_EMOJI = {
    "yingguo": "🇬🇧", "deguo": "🇩🇪", "faguo": "🇫🇷",
    "yuenan": "🇻🇳", "xinjapo": "🇸🇬", "taiguo": "🇹🇭",
    "malaixiya": "🇲🇾", "yindu": "🇮🇳", "riben": "🇯🇵",
    "shate": "🇸🇦", "ahlianda": "🇦🇪", "bolan": "🇵🇱",
    "xiongyali": "🇭🇺", "meiguo": "🇺🇸", "jianada": "🇨🇦",
    "moxige": "🇲🇽", "hanguo": "🇰🇷", "yinni": "🇮🇩",
    "feilvbin": "🇵🇭", "xibanya": "🇪🇸", "helan": "🇳🇱",
    "yidali": "🇮🇹", "baxi": "🇧🇷",
}

TYPE_EMOJI = {
    "最低工资": "💰",
    "社保": "🏦",
    "签证与工作许可": "📋",
    "劳动法与合规": "⚖️",
    "个人所得税": "📊",
    "其他": "📌",
}

# ============================================================
# 第一阶段：解析日报
# ============================================================
def parse_reports():
    report_files = sorted(REPORTS_DIR.glob("*.md"))
    all_entries = {}

    for rf in report_files:
        content = rf.read_text()

        date_match = re.search(r'\*\*日期/Date\*\*:\s*(\d{4}年\d{1,2}月\d{1,2}日)', content)
        if not date_match:
            date_match = re.search(r'\*\*日期/Date\*\*:\s*(\d{4}-\d{2}-\d{2})', content)
        report_date = date_match.group(1) if date_match else rf.stem

        sections = re.split(r'\n(?=### [^\n]+\n)', content)

        for section in sections:
            lines = section.split('\n')
            header_line = next((l for l in lines if re.match(r'^### ', l)), None)
            if not header_line:
                continue

            country_code = None
            for cn, code in COUNTRY_TO_ENTITY.items():
                if cn in header_line:
                    country_code = code
                    break
            if not country_code:
                continue

            if country_code not in all_entries:
                all_entries[country_code] = []

            h3_blocks = re.split(r'\n#### ', section)

            for h3 in h3_blocks[1:]:
                title_match = re.match(r'(🔴\s*)?(.+?)\s*\(', h3)
                if not title_match:
                    continue
                is_red = bool(title_match.group(1))
                pol_type_raw = title_match.group(2).strip()

                pol_type = "其他"
                for kw, t in [
                    ("最低工资", "最低工资"), ("社保", "社保"),
                    ("签证", "签证与工作许可"), ("劳动法", "劳动法与合规"),
                    ("个人所得", "个人所得税"),
                ]:
                    if kw in pol_type_raw:
                        pol_type = t
                        break

                table_match = re.search(
                    r'\| 项目 \|[ 内容]+\|([\s\S]+?)(?:\n\*\*分析|\n#### |\n## )', h3
                )
                if not table_match:
                    continue

                table_content = table_match.group(1)
                rows = re.findall(r'\| \*\*([^*]+)\*\* \|(.+?) \|', table_content)

                entry_parts = []
                for k, v in rows:
                    entry_parts.append(f"- **{k.strip()}**：{v.strip()}")

                eff_match = re.search(r'\*\*生效日期\*\*[:：]\s*(.+?)(?:\n|\|)', h3)
                effective_date = eff_match.group(1).strip() if eff_match else report_date

                analysis_match = re.search(
                    r'\*\*分析/Analysis[:：].*?:\s*(.+?)(?:\n\n|\n\*\*|$)', h3, re.DOTALL
                )
                summary = ""
                if analysis_match:
                    summary = analysis_match.group(1).strip()[:150]

                entry_text = "\n".join(entry_parts)
                if summary:
                    entry_text += f"\n- **摘要**：{summary}"

                is_dup = any(
                    e['type'] == pol_type
                    and e['effective_date'][:10] == effective_date[:10]
                    and e['source'] == rf.stem
                    for e in all_entries[country_code]
                )
                if is_dup:
                    continue

                all_entries[country_code].append({
                    "date": report_date,
                    "effective_date": effective_date,
                    "type": pol_type,
                    "severity": "🔴" if is_red else "🟢",
                    "content": entry_text,
                    "source": rf.stem,
                })

    return all_entries


# ============================================================
# 第二阶段：构建时间线 markdown
# ============================================================
def build_timeline_md(entries):
    entries_sorted = sorted(entries, key=lambda x: (x['effective_date'], x['type']))
    lines = []
    current_date = None

    for e in entries_sorted:
        eff = e['effective_date'][:10] if len(e['effective_date']) > 10 else e['effective_date']
        if eff != current_date:
            lines.append(f"\n### {eff}\n")
            current_date = eff

        emoji = TYPE_EMOJI.get(e['type'], "📌")
        sev = e['severity']
        source_file = e['source']
        lines.append(
            f"{sev}**{emoji}{e['type']}** — "
            f"[[raw/sources/03_区域政策/政策日报/{source_file}|{source_file}]]\n"
        )
        for line in e['content'].split('\n'):
            if line.strip():
                lines.append(f"{line}\n")
        lines.append("\n")

    return "".join(lines)


# ============================================================
# 第三阶段：更新/创建 entity 页
# ============================================================
def update_entity_pages(all_entries, dry_run=False):
    results = {"updated": [], "created": []}

    for country_code, entries in sorted(all_entries.items()):
        entity_file = ENTITIES_DIR / f"{country_code}.md"
        country_name = COUNTRY_NAMES.get(country_code, country_code)
        region = REGION.get(country_code, "其他")
        emoji = REGION_EMOJI.get(country_code, "")
        timeline_md = build_timeline_md(entries)

        sources = sorted(set(e['source'] for e in entries))
        tags_list = ["国家", region] + sorted(set(e['type'] for e in entries))
        tags_str = ", ".join(sorted(set(tags_list)))

        sources_str = ", ".join(
            f"raw/sources/03_区域政策/政策日报/{s}.md" for s in sources
        )

        if entity_file.exists():
            existing = entity_file.read_text()

            if "## 政策时间线" in existing:
                before, _ = existing.split("## 政策时间线", 1)
                new_content = before.rstrip() + "\n" + timeline_md
            else:
                new_content = existing.rstrip() + "\n" + timeline_md

            new_content = re.sub(
                r'^updated: .+$', 'updated: 2026-04-24', new_content, flags=re.MULTILINE
            )

            if not dry_run:
                entity_file.write_text(new_content)
            results["updated"].append(country_code)
            action = "UPDATE"
        else:
            new_entity = f"""---
title: {country_name}
created: 2026-04-24
updated: 2026-04-24
type: entity
tags: [{tags_str}]
sources: [{sources_str}]
confidence: medium
---

# {emoji} {country_name}

## 基本信息

| 项目 | 内容 |
|------|------|
| 英文 | {COUNTRY_NAMES.get(country_code, country_code)} |
| 区域 | {region} |
| 来源 | [[hr-policy-daily|全球HR政策日报]] |

{timeline_md}
## 相关页面

- [[hr-policy-daily]] — 全球HR政策日报
- [[quyu-guihua]] — 区域合规政策
"""
            if not dry_run:
                entity_file.write_text(new_entity)
            results["created"].append(country_code)
            action = "CREATE"

        print(f"  [{action}] {country_code}({country_name}): {len(entries)}条")

    return results


# ============================================================
# 第四阶段：更新 hr-policy-daily 快照表
# ============================================================
def update_hr_policy_daily(all_entries, dry_run=False):
    """从最新日报中提取各国最新政策快照，更新到 hr-policy-daily.md"""
    daily_file = CONCEPTS_DIR / "hr-policy-daily.md"
    if not daily_file.exists():
        print(f"  [SKIP] hr-policy-daily.md not found")
        return

    existing = daily_file.read_text()

    # 提取每个国家的最新条目（按类型）
    latest = {}
    for code, entries in all_entries.items():
        latest[code] = {}
        for e in entries:
            t = e['type']
            if t not in latest[code] or e['date'] > latest[code][t]['date']:
                latest[code][t] = e

    # 构建新快照表格
    snapshot_lines = ["\n## 各国最新政策快照（整合自日报）\n"]
    snapshot_lines.append(f"> 自动生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    snapshot_lines.append("> ⚠️ 以下数据整合自各份日报的时间线条目，部分数值可能已被后续更新覆盖，请以对应国家 entity 页为准。\n")
    snapshot_lines.append("\n| 国家 | 政策类型 | 生效日期 | 摘要 | 严重度 | 来源 |\n")
    snapshot_lines.append("|------|---------|---------|------|------|------|\n")

    for code in sorted(latest.keys()):
        country_name = COUNTRY_NAMES.get(code, code)
        for t, e in sorted(latest[code].items()):
            summary = e['content'].split('\n')[0][:50] if e['content'] else ""
            snapshot_lines.append(
                f"| {country_name} | {e['type']} | {e['effective_date'][:10]} | "
                f"{summary} | {e['severity']} | [[raw/sources/03_区域政策/政策日报/{e['source']}|{e['source']}]] |\n"
            )

    snapshot_md = "".join(snapshot_lines)

    # 替换或追加快照 section
    if "## 各国最新政策快照" in existing:
        before, _ = existing.split("## 各国最新政策快照", 1)
        # 保留 before 的第一部分（到"## 相关页面"之前）
        if "## 相关页面" in before:
            before_part1, _ = before.split("## 相关页面", 1)
            new_content = before_part1.rstrip() + "\n" + snapshot_md + "\n## 相关页面"
        else:
            new_content = before.rstrip() + "\n" + snapshot_md
    else:
        new_content = existing.rstrip() + "\n" + snapshot_md

    new_content = re.sub(
        r'^updated: .+$', f'updated: {datetime.now().strftime("%Y-%m-%d")}',
        new_content, flags=re.MULTILINE
    )

    if not dry_run:
        daily_file.write_text(new_content)

    print(f"  [UPDATE] hr-policy-daily.md: {len(latest)}个国家快照")


# ============================================================
# 第五阶段：记录 log
# ============================================================
def append_log(results, total_entries, dry_run=False):
    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    log_entry = f"\n## {today} — 政策日报整合\n"
    log_entry += f"- 扫描日报：{len(list(REPORTS_DIR.glob('*.md')))}份\n"
    log_entry += f"- 更新 entity：{', '.join(results['updated'])}\n"
    log_entry += f"- 新建 entity：{', '.join(results['created'])}\n"
    log_entry += f"- 总条目：{total_entries}条\n"

    if LOG_FILE.exists():
        existing = LOG_FILE.read_text()
        new_log = existing.rstrip() + log_entry
    else:
        new_log = log_entry

    if not dry_run:
        LOG_FILE.write_text(new_log)


# ============================================================
# 主流程
# ============================================================
def main():
    dry_run = "--dry-run" in sys.argv

    print(f"\n{'[DRY-RUN] ' if dry_run else ''}HR Policy Backfill — {datetime.now().isoformat()}")
    print("=" * 60)

    print("\n[Phase 1] 解析日报...")
    all_entries = parse_reports()
    total_entries = sum(len(v) for v in all_entries.values())
    print(f"  → {len(all_entries)}个国家，{total_entries}条政策条目")

    print("\n[Phase 2] 更新 entity 页...")
    results = update_entity_pages(all_entries, dry_run=dry_run)

    print("\n[Phase 3] 更新 hr-policy-daily.md...")
    update_hr_policy_daily(all_entries, dry_run=dry_run)

    print("\n[Phase 4] 记录 log...")
    append_log(results, total_entries, dry_run=dry_run)

    print(f"\n{'[DRY-RUN] ' if dry_run else ''}完成！")
    print(f"  更新：{len(results['updated'])} | 新建：{len(results['created'])}")


if __name__ == "__main__":
    main()
