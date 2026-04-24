#!/usr/bin/env python3
"""
Wiki Link Auto-Associate — 高置信度页面自动补充 wikilink
逻辑：confidence=high|medium 的页面之间，按共享 tag ≥2 自动建 wikilink
用法：python3 scripts/wiki-link-auto.py [--dry-run]
"""
import re
import yaml
from pathlib import Path
from datetime import datetime
from collections import Counter

WIKI_ROOT = Path.home() / "wiki"
TYPES = ["entities", "concepts", "comparisons", "queries"]

# ============================================================
# 加载页面
# ============================================================
def load_pages():
    pages = {}
    for d in TYPES:
        for f in (WIKI_ROOT / d).glob("*.md"):
            raw = f.read_text(encoding="utf-8")
            try:
                fm, content = raw.split("---", 2)[1], raw.split("---", 2)[2]
                meta = yaml.safe_load(fm) or {}
            except Exception:
                meta = {}
                content = raw

            slug = f.stem
            pages[slug] = {
                "title": meta.get("title", slug),
                "type": meta.get("type", d),
                "tags": set(meta.get("tags", [])),
                "confidence": meta.get("confidence", "medium"),
                "file": f,
                "raw": raw,
                "content": content.strip(),
            }
    return pages


def get_existing_links(content: str) -> set:
    """提取页面中已有的所有 wikilink slug"""
    return set(re.findall(r"\[\[([a-z0-9\-]+)\]\]", content))


def split_related_section(content: str) -> tuple:
    """将 content 拆分为 [before, related_block, after]"""
    pattern = r"(^## 相关页面\s*\n)"
    m = re.search(pattern, content, re.MULTILINE)
    if not m:
        return content, "", ""

    before = content[:m.start()]
    after_start = m.end()

    # 找 after：下一个 ## 标题（非相关页面）或文件末尾
    rest = content[after_start:]
    after_m = re.search(r"^\#{2,}", rest, re.MULTILINE)
    if after_m:
        related_block = rest[:after_m.start()]
        after = rest[after_m.start():]
    else:
        related_block = rest
        after = ""

    return before, related_block, after


def get_generic_tags(pages, entity_threshold=10):
    """返回过于泛化的 tag 集合（entity中出现>entity_threshold次），排除这些tag不参与关联判断"""
    entity_tags = Counter()
    for page in pages.values():
        if page["type"] == "entity":
            for tag in page["tags"]:
                entity_tags[tag] += 1
    return {tag for tag, cnt in entity_tags.items() if cnt > entity_threshold}


def build_related_links(slug: str, page: dict, pages: dict,
                         generic_tags: set, threshold: int = 2) -> list:
    """计算应补充的 wikilink，按共享 tag 数排序"""
    candidates = []
    existing = get_existing_links(page["content"])
    # 不包括自己
    existing.add(slug)

    for other_slug, other in pages.items():
        if other_slug in existing:
            continue
        if other["confidence"] == "low":
            continue
        # 排除过于泛化的 tag 后再计算共享数
        shared = (page["tags"] - generic_tags) & (other["tags"] - generic_tags)
        if len(shared) >= threshold:
            candidates.append((other_slug, other["title"], len(shared), other["confidence"]))

    # 按共享 tag 数降序
    candidates.sort(key=lambda x: -x[2])
    return candidates


def insert_related_links(page: dict, candidates: list) -> str:
    """在相关页面 section 插入新链接（去重+追加）"""
    if not candidates:
        return None

    before, related_block, after = split_related_section(page["content"])

    # 解析已有链接
    existing_in_block = set(re.findall(r"\[\[([a-z0-9\-]+)\]\]", related_block))

    # 合并，去重
    new_links = []
    for slug, title, shared, conf in candidates:
        if slug not in existing_in_block:
            conf_mark = "🔴" if conf == "high" else "🟡"
            new_links.append(f"- [[{slug}]] {conf_mark} ← {', '.join(sorted(page['tags'] & pages[slug]['tags']))}")

    if not new_links:
        return None

    conf_mark = "🔴" if page["confidence"] == "high" else "🟡"
    new_block = related_block.rstrip() + "\n" + "\n".join(new_links) + "\n"

    new_content = before + "## 相关页面\n" + new_block + after
    return new_content


# ============================================================
# 主流程
# ============================================================
def main():
    dry_run = "--dry-run" in __import__("sys").argv
    threshold = 2  # 共享 tag ≥2 才建 link

    prefix = "[DRY-RUN] " if dry_run else ""
    print(f"\n{prefix}Wiki Link Auto-Associate — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  阈值：共享 tag ≥ {threshold} | 仅 confidence ≠ low")
    print("=" * 60)

    pages = load_pages()
    print(f"  加载：{len(pages)} 个页面")

    high_medium = {s: p for s, p in pages.items() if p["confidence"] != "low"}
    print(f"  高置信度：{len(high_medium)} 个（high/medium）")

    # 排除 entity 中出现>10次的过于泛化的 tag
    generic_tags = get_generic_tags(pages, entity_threshold=10)
    print(f"  排除泛化 tag：{sorted(generic_tags)}")

    global_candidates = {}  # slug → [(target_slug, title, shared, conf), ...]

    for slug, page in high_medium.items():
        cands = build_related_links(slug, page, pages, generic_tags, threshold)
        if cands:
            global_candidates[slug] = cands

    print(f"  有关联候选项：{len(global_candidates)} 个页面")

    # 统计
    total_new_links = 0
    modified = []

    for slug, cands in global_candidates.items():
        page = pages[slug]
        new_links = []
        existing = get_existing_links(page["content"])

        for cand_slug, title, shared, conf in cands:
            if cand_slug not in existing:
                new_links.append((cand_slug, title, shared, conf))

        if not new_links:
            continue

        conf_mark = "🔴" if page["confidence"] == "high" else "🟡"
        print(f"\n  {conf_mark} [[{slug}]] — 新增 {len(new_links)} 条 wikilink：")
        for cslug, ctitle, shared, conf in new_links[:5]:
            print(f"    + [[{cslug}]] ({shared} shared tags)")
        if len(new_links) > 5:
            print(f"    ... +{len(new_links)-5} more")

        if not dry_run:
            before, related_block, after = split_related_section(page["content"])
            conf_mark2 = "🔴" if page["confidence"] == "high" else "🟡"
            new_items = []
            for cslug, ctitle, shared, conf in new_links:
                new_items.append(f"- [[{cslug}]] {conf_mark2} ← {', '.join(sorted(page['tags'] & pages[cslug]['tags']))}")
            new_block = related_block.rstrip() + "\n" + "\n".join(new_items) + "\n"

            # 重建 frontmatter
            raw = page["raw"]
            fm_raw = raw.split("---", 2)[1]
            new_fm_raw = fm_raw
            # 更新时间戳
            import yaml
            fm = yaml.safe_load(fm_raw) or {}
            fm["updated"] = datetime.now().strftime("%Y-%m-%d")
            fm_lines = []
            for k, v in fm.items():
                if isinstance(v, list):
                    fm_lines.append(f"{k}: [{', '.join(v)}]")
                else:
                    fm_lines.append(f"{k}: {v}")
            new_fm_raw = "---\n" + "\n".join(fm_lines) + "\n---\n"

            new_raw = new_fm_raw + before + "## 相关页面\n" + new_block + after
            page["file"].write_text(new_raw, encoding="utf-8")
            modified.append(slug)

    modified_count = len(modified) if not dry_run else 0
    print(f"\n{prefix}完成：{len(global_candidates)} 个页面有关联 | {modified_count} 个已写入")

    if modified and not dry_run:
        log_file = WIKI_ROOT / "log.md"
        log_entry = f"\n## {datetime.now().strftime('%Y-%m-%d')} — wikilink 自动关联（⑧）\n"
        log_entry += f"- 阈值：共享 tag ≥ {threshold} | confidence ≠ low\n"
        log_entry += f"- 关联了：{', '.join(modified[:10])}{'...' if len(modified) > 10 else ''}\n"
        log_entry += f"- 新增链接总数：{sum(len(global_candidates[s]) for s in modified)} 条\n"
        if log_file.exists():
            existing = log_file.read_text()
            log_file.write_text(existing.rstrip() + log_entry)
        else:
            log_file.write_text(log_entry)


if __name__ == "__main__":
    main()
