#!/usr/bin/env python3
"""
Wiki Index Generator — 按主题生成聚合索引页
将 index.md 的按 type 分类升级为按主题跨类型导航

用法：python3 wiki-index-gen.py [--dry-run]
"""
import yaml
import re
from pathlib import Path
from datetime import datetime

WIKI_ROOT = Path.home() / "wiki"
INDEX_DIR = WIKI_ROOT / "_index"
TYPES = ["entities", "concepts", "comparisons", "queries"]

# ============================================================
# 加载所有 wiki 页面
# ============================================================
def load_all_pages():
    pages = {}
    for d in TYPES:
        for f in (WIKI_ROOT / d).glob("*.md"):
            raw = f.read_text(encoding="utf-8")
            if raw.startswith("---"):
                parts = raw.split("---", 2)
                if len(parts) >= 3:
                    try:
                        fm = yaml.safe_load(parts[1]) or {}
                    except Exception:
                        fm = {}
                    content = parts[2]
                else:
                    fm = {}
                    content = raw
            else:
                fm = {}
                content = raw

            slug = f.stem
            pages[slug] = {
                "title": fm.get("title", slug),
                "type": fm.get("type", d),
                "tags": fm.get("tags", []),
                "sources": fm.get("sources", []),
                "confidence": fm.get("confidence", "medium"),
                "updated": fm.get("updated", ""),
                "file": str(f.relative_to(WIKI_ROOT)),
                "content": content.strip(),
            }
    return pages


def build_tag_index(pages):
    """构建 tag → [slug, ...] 反向索引"""
    tag_index = {}
    for slug, page in pages.items():
        for tag in page["tags"]:
            tag = tag.strip()
            if tag not in tag_index:
                tag_index[tag] = []
            tag_index[tag].append(slug)
    return tag_index


def tag_to_slug(tag: str) -> str:
    """将 tag 转为 url-safe slug"""
    s = tag.lower()
    s = re.sub(r"[^\w\s]", "", s)
    s = re.sub(r"\s+", "-", s)
    return s


def page_link(slug: str, title: str = "") -> str:
    """生成 wikilink 行"""
    if title:
        return f"- [[{slug}]] — {title}"
    return f"- [[{slug}]]"


# ============================================================
# 核心：按主题聚合
# ============================================================

# 主题定义：(slug, title, description, tags_to_include, exclude_slugs)
THEMES = [
    {
        "slug": "xiwang-quyu",
        "title": "西欧市场",
        "description": "西欧（德国/英国/法国/荷兰/意大利/西班牙/波兰/匈牙利）出海HR合规专题。覆盖最低工资、社保、签证、劳动法核心数据。",
        "include_tags": ["西欧", "南欧", "中东欧"],
        "exclude_tags": [],
        "exclude_slugs": [],
        "region": "西欧",
    },
    {
        "slug": "dongnanya-quyu",
        "title": "东南亚市场",
        "description": "东南亚（越南/新加坡/泰国/马来西亚/印尼/菲律宾）出海HR专题。聚焦EOR模式、招聘合规、薪税政策。",
        "include_tags": ["东南亚"],
        "exclude_tags": [],
        "exclude_slugs": [],
        "region": "东南亚",
    },
    {
        "slug": "hegui-zhengce",
        "title": "合规政策体系",
        "description": "出海HR合规全景图：最低工资/社保/签证/劳动法/数据合规。高置信度来源标注。",
        "include_tags": ["合规", "劳动法", "社保", "签证", "风控", "AI合规"],
        "exclude_tags": [],
        "exclude_slugs": [],
        "region": None,
    },
    {
        "slug": "yonggong-moshi",
        "title": "用工模式全解",
        "description": "EOR/IC（独立承包商）/自雇佣/外派员工四种模式对比。适用场景、成本、合规风险、演进路径。",
        "include_tags": ["EOR", "用工模式", "外派"],
        "exclude_tags": [],
        "exclude_slugs": [],
        "region": None,
    },
    {
        "slug": "chuhai-jieduan",
        "title": "出海阶段与模式选择",
        "description": "试水期(0-1) → 增长期(1-10) → 全球化(成熟期) 三阶段框架。各阶段核心痛点、用工模式、HR战略重点。",
        "include_tags": ["出海阶段", "出海"],
        "exclude_tags": [],
        "exclude_slugs": [],
        "region": None,
    },
    {
        "slug": "yongyou-shengtai",
        "title": "用友薪福社生态",
        "description": "用友薪福社全产品线：EOR服务/猎头(海猎)/Payroll薪税/签证服务，覆盖欧洲29国/亚太18国/中东非洲30+/美洲7国。",
        "include_tags": ["用友", "用友薪福社"],
        "exclude_tags": [],
        "exclude_slugs": [],
        "region": None,
    },
    {
        "slug": "xinchou-shebao",
        "title": "薪酬与社保",
        "description": "全球薪酬体系设计：属地化薪酬结构、外派薪酬包、社保合规、个税处理。附各国最低工资与社保费率数据。",
        "include_tags": ["薪酬", "薪税"],
        "exclude_tags": [],
        "exclude_slugs": [],
        "region": None,
    },
    {
        "slug": "zimeiti-yunying",
        "title": "自媒体运营",
        "description": "锴哥抖音/视频号/知乎账号矩阵：IP人设定位、内容策略（政策/干货/人设）、热点追踪系统、选题库。",
        "include_tags": ["自媒体", "抖音", "视频号", "选题"],
        "exclude_tags": [],
        "exclude_slugs": [],
        "region": None,
    },
]


def generate_index_page(theme: dict, pages: dict, tag_index: dict) -> str:
    """生成单个主题索引页"""
    today = datetime.now().strftime("%Y-%m-%d")

    # 收集匹配的 pages
    matched = []
    for slug, page in pages.items():
        if slug in theme.get("exclude_slugs", []):
            continue
        page_tags = set(page["tags"])
        include_tags = set(theme.get("include_tags", []))
        if page_tags & include_tags:
            matched.append((slug, page))

    # 按 type 分组
    by_type = {"entity": [], "concept": [], "comparison": [], "query": []}
    for slug, page in matched:
        t = page["type"]
        if t not in by_type:
            by_type[t] = []
        by_type[t].append((slug, page))

    # 候选 tags（用于显示有哪些相关 tag）
    related_tags = set()
    for slug, page in matched:
        related_tags.update(page["tags"])
    related_tags = sorted(related_tags - set(theme.get("include_tags", [])))[:6]

    lines = [
        "---",
        f"title: {theme['title']}",
        f"created: {today}",
        f"updated: {today}",
        "type: summary",
        f"tags: [{', '.join(theme.get('include_tags', []))}]",
        f"sources: []",
        "confidence: high",
        "---",
        "",
        f"# {theme['title']}",
        "",
        theme["description"],
        "",
    ]

    # 相关标签
    if related_tags:
        lines += [
            "**相关主题：** " + " · ".join(f"#{t}" for t in related_tags),
            "",
        ]

    lines += [
        f"**收录页面：** {len(matched)} 个",
        "",
        "---",
        "",
    ]

    # 按类型输出
    type_labels = {
        "entity": "🇨🇳 国家实体",
        "concept": "📖 概念框架",
        "comparison": "⚖️ 对比分析",
        "query": "❓ 常见问题",
    }

    for ptype, label in type_labels.items():
        items = sorted(by_type.get(ptype, []), key=lambda x: x[1]["title"])
        if not items:
            continue
        lines += [f"### {label}", ""]
        for slug, page in items:
            conf_mark = "🔴" if page["confidence"] == "high" else "🟡" if page["confidence"] == "medium" else "⚪"
            updated = f"({page['updated']})" if page["updated"] else ""
            lines.append(f"- [[{slug}]] {conf_mark} {updated}")
        lines.append("")

    lines += [
        "---",
        "",
        f"*最后更新：{today} | 来源：wiki知识库自动聚合*",
    ]

    return "\n".join(lines)


# ============================================================
# 主流程
# ============================================================
def main():
    dry_run = "--dry-run" in __import__("sys").argv
    print(f"\n{'[DRY-RUN] ' if dry_run else ''}Wiki Index Generator — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    pages = load_all_pages()
    tag_index = build_tag_index(pages)
    print(f"  已加载：{len(pages)} 个页面 | {len(tag_index)} 个标签")

    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    created = []
    for theme in THEMES:
        slug = theme["slug"]
        content = generate_index_page(theme, pages, tag_index)
        index_file = INDEX_DIR / f"{slug}.md"

        if index_file.exists() and not dry_run:
            # 增量更新：只更新 frontmatter + 页面列表，保留原有描述
            existing = index_file.read_text(encoding="utf-8")
            # 替换 frontmatter 和页面列表部分
            # 保留用户编辑的 description
            pass

        if dry_run:
            print(f"  [DRY] {theme['title']} → _index/{slug}.md")
        else:
            index_file.write_text(content, encoding="utf-8")
            print(f"  ✅ {theme['title']} → _index/{slug}.md")
            created.append(slug)

    # 生成总索引页
    today = datetime.now().strftime("%Y-%m-%d")
    total_index_content = f"""---
title: 知识库主题索引
created: {today}
updated: {today}
type: summary
tags: [导航, 索引]
sources: []
confidence: high
---

# 知识库主题索引

> 按主题跨类型导航，而非按目录分类。

**收录：** {len(pages)} 个知识库页面 | {len(THEMES)} 个主题

---

## 核心主题

"""
    for theme in THEMES:
        matched = [
            s for s, p in pages.items()
            if set(p["tags"]) & set(theme.get("include_tags", []))
            and s not in theme.get("exclude_slugs", [])
        ]
        total_index_content += f"- [[_{theme['slug']}|{theme['title']}]] — {len(matched)} 个页面\n"

    total_index_content += f"""

---

## 按区域

### 🌐 西欧
[[_xiwang-quyu|西欧市场]] — 德国/英国/法国/荷兰/意大利/西班牙/波兰/匈牙利

### 🌏 东南亚
[[_dongnanya-quyu|东南亚市场]] — 越南/新加坡/泰国/马来西亚/印尼/菲律宾

## 按职能

### ⚖️ 合规
[[_hegui-zhengce|合规政策体系]] — 最低工资/社保/签证/劳动法/数据合规

### 👷 用工模式
[[_yonggong-moshi|用工模式全解]] — EOR/IC/自雇佣/外派

### 📊 出海阶段
[[_chuhai-jieduan|出海阶段与模式选择]] — 试水期/增长期/全球化

### 💰 薪酬社保
[[_xinchou-shebao|薪酬与社保]] — 属地化薪酬/外派薪酬包/社保合规

## 生态

### 🏢 用友生态
[[_yongyou-shengtai|用友薪福社生态]] — EOR/海猎/Payroll/签证

### 📱 自媒体运营
[[_zimeiti-yunying|自媒体运营]] — 抖音/视频号/知乎矩阵

---

*最后更新：{today}*
"""

    if not dry_run:
        (WIKI_ROOT / "_index.md").write_text(total_index_content, encoding="utf-8")
        print(f"  ✅ 总索引 → _index.md")

    # 记录 log
    if not dry_run and created:
        log_file = WIKI_ROOT / "log.md"
        log_entry = f"\n## {datetime.now().strftime('%Y-%m-%d')} — _index 主题索引完成\n"
        log_entry += f"- 创建主题索引：{', '.join(created)}\n"
        log_entry += f"- 总索引：_index.md\n"
        if log_file.exists():
            existing = log_file.read_text()
            log_file.write_text(existing.rstrip() + log_entry)
        else:
            log_file.write_text(log_entry)

    print(f"\n完成：{'[DRY-RUN] ' if dry_run else ''}{len(created)} 个主题索引已{'生成' if not dry_run else '待生成'}")


if __name__ == "__main__":
    main()
