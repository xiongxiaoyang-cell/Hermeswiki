#!/usr/bin/env python3
"""
Wiki Lint — 死链/孤立页扫描
每周定期运行，维护 wiki 健康度
"""
import re
import sys
from pathlib import Path
from datetime import datetime

WIKI_ROOT = Path("/home/b4ac5686610a4ae2/wiki")

def lint():
    """扫描 wiki，返回 (errors, warnings, orphans)"""
    errors = []   # 死链
    warnings = [] # 警告
    orphans = []   # 孤立页（无入站链接）

    entities_dir = WIKI_ROOT / "entities"
    concepts_dir = WIKI_ROOT / "concepts"
    comparisons_dir = WIKI_ROOT / "comparisons"
    queries_dir = WIKI_ROOT / "queries"

    # Step 1: 建立所有 wikilink 的目标集合
    all_pages = set()
    for d in [entities_dir, concepts_dir, comparisons_dir, queries_dir]:
        if d.exists():
            for f in d.glob("*.md"):
                slug = f.stem  # yuenan, hr-policy-daily
                all_pages.add(slug)

    # Step 2: 扫描所有 wikilink
    wikilinks_found = set()

    for d in [entities_dir, concepts_dir, comparisons_dir, queries_dir]:
        if not d.exists():
            continue
        for f in d.glob("*.md"):
            content = f.read_text()
            # 匹配 [[page]] 和 [[page|alias]]
            links = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content)
            for link in links:
                link = link.strip()
                # 跳过外部链接和锚点
                if '/' in link or '#' in link or link.startswith('http'):
                    continue
                wikilinks_found.add(link)

    # Step 3: 找死链（wikilink指向不存在的页面）
    for link in wikilinks_found:
        if link not in all_pages:
            errors.append(f"  🔴 死链：[[{link}]]")

    # Step 4: 建立入站链接映射（谁链接到了这个页面）
    inbound = {page: [] for page in all_pages}
    for d in [entities_dir, concepts_dir, comparisons_dir, queries_dir]:
        if not d.exists():
            continue
        for f in d.glob("*.md"):
            slug = f.stem
            content = f.read_text()
            links = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content)
            for link in links:
                link = link.strip()
                if '/' in link or '#' in link or link.startswith('http'):
                    continue
                if link in inbound:
                    inbound[link].append(slug)

    # Step 5: 找孤立页（无入站链接的页面，排除首页和特殊页）
    special = {"index", "SCHEMA", "log", "README"}
    for page, refs in inbound.items():
        if not refs and page not in special:
            orphans.append(f"  🟡 孤立页：{page}.md（无入站链接）")

    return errors, warnings, orphans


def main():
    dry_run = "--dry-run" in sys.argv

    print(f"\n{'[DRY-RUN] ' if dry_run else ''}Wiki Lint — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    errors, warnings, orphans = lint()

    print(f"\n结果：")
    if errors:
        print(f"  🔴 死链 {len(errors)} 条：")
        for e in errors:
            print(e)
    else:
        print("  ✅ 无死链")

    if warnings:
        print(f"  🟡 警告 {len(warnings)} 条：")
        for w in warnings:
            print(w)

    if orphans:
        print(f"  🟡 孤立页 {len(orphans)} 条：")
        for o in orphans:
            print(o)
    else:
        print("  ✅ 无孤立页")

    total = len(errors) + len(warnings) + len(orphans)
    print(f"\n健康度：{'✅ 通过' if total == 0 else f'⚠️ {total}个问题'}")

    if not dry_run and total > 0:
        log_file = WIKI_ROOT / "log.md"
        log_entry = f"\n## {datetime.now().strftime('%Y-%m-%d %H:%M')} — Wiki Lint\n"
        log_entry += f"- 死链：{len(errors)} | 孤立页：{len(orphans)} | 警告：{len(warnings)}\n"
        if errors:
            for e in errors:
                log_entry += f"- {e.strip()}\n"
        if orphans:
            for o in orphans:
                log_entry += f"- {o.strip()}\n"

        if log_file.exists():
            existing = log_file.read_text()
            log_file.write_text(existing.rstrip() + log_entry)
        else:
            log_file.write_text(log_entry)

    return 0 if total == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
