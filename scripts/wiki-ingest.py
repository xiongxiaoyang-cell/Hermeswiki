#!/usr/bin/env python3
"""
Wiki Ingest — 通用文件 ingest 管道
每周扫描 raw/sources/，新 .md 文件自动建 wiki 页面
用法：python3 wiki-ingest.py [--dry-run]
"""
import re
import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime

WIKI_ROOT = Path("/home/b4ac5686610a4ae2/wiki")
RAW_SOURCES = WIKI_ROOT / "raw/sources"
PROCESSED_FILE = WIKI_ROOT / ".ingest-processed.json"

# 已知 entity 国家
KNOWN_ENTITIES = {
    "英国": "yingguo", "德国": "deguo", "法国": "faguo",
    "越南": "yuenan", "新加坡": "xinjapo", "泰国": "taiguo",
    "马来西亚": "malaixiya", "印度": "yindu", "日本": "riben",
    "沙特阿拉伯": "shate", "阿联酋": "ahlianda", "波兰": "bolan",
    "匈牙利": "xiongyali", "美国": "meiguo", "加拿大": "jianada",
    "墨西哥": "moxige", "韩国": "hanguo", "印度尼西亚": "yinni",
    "菲律宾": "feilvbin", "西班牙": "xibanya", "荷兰": "helan",
    "意大利": "yidali", "巴西": "baxi",
}

ENTITY_FILES = {v: True for v in KNOWN_ENTITIES.values()}  # yuenan, yingguo ...

# ============================================================
# LLM 分类接口（调用 MiniMax-M2.7）
# ============================================================
def llm_classify(content: str, filename: str) -> dict:
    """用 LLM 判断文件类型和元信息"""
    prompt = f"""你是一个出海HR知识库分类助手。根据文件内容，判断：

文件：{filename}
内容前500字：
{content[:500]}

输出格式（只输出JSON，不要其他文字）：
{{
  "type": "entity" | "concept" | "comparison" | "query",
  "slug": "小写英文slug（如yuenan/hr-policy-daily/eor-compare）",
  "title": "中文标题",
  "tags": ["标签1", "标签2", "标签3"],
  "summary": "2-3句中文摘要，说明这个页面是什么"
}}

规则：
- type=entity：涉及具体国家HR政策（越南/德国/英国…）
- type=concept：涉及方法论/概念（EOR/合规/招聘/薪酬/劳动法）
- type=comparison：涉及对比（vs/对比/比较/A vs B）
- type=query：常见问题解答
- slug 不能与现有 slug 重复：{list(ENTITY_FILES.keys())}
"""

    import urllib.request
    import urllib.parse

    payload = {
        "model": "MiniMax-M2.7",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 300,
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "http://localhost:8080/v1/chat/completions",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            content_out = result["choices"][0]["message"]["content"].strip()
            # 提取JSON
            json_match = re.search(r'\{[\s\S]+\}', content_out)
            if json_match:
                return json.loads(json_match.group())
    except Exception as e:
        print(f"    [WARN] LLM调用失败: {e}")

    # Fallback：基于文件名 heuristic
    fname_lower = filename.lower()
    for cn, code in KNOWN_ENTITIES.items():
        if cn in content or cn in filename:
            return {"type": "entity", "slug": code, "title": cn, "tags": ["国家"], "summary": "国家HR政策"}
    if "compare" in fname_lower or "对比" in content or "vs" in fname_lower:
        return {"type": "comparison", "slug": "new-compare", "title": filename, "tags": ["对比"], "summary": "对比页面"}
    return {"type": "concept", "slug": "new-concept", "title": filename, "tags": ["概念"], "summary": "概念页面"}


# ============================================================
# 核心逻辑
# ============================================================
def get_processed_hashes() -> set:
    """读取已处理文件哈希集合"""
    if PROCESSED_FILE.exists():
        try:
            data = json.loads(PROCESSED_FILE.read_text())
            return set(data.get("hashes", []))
        except Exception:
            pass
    return set()


def save_processed_hashes(hashes: set):
    """保存已处理文件哈希"""
    PROCESSED_FILE.write_text(json.dumps({
        "updated": datetime.now().isoformat(),
        "hashes": sorted(hashes),
    }, ensure_ascii=False, indent=2))


def compute_hash(content: str) -> str:
    return hashlib.md5(content[:2000].encode("utf-8")).hexdigest()[:12]


def scan_new_files(processed_hashes: set):
    """找出未处理的新 .md 文件"""
    new_files = []
    skip_dirs = {
        RAW_SOURCES / "03_区域政策/政策日报",  # backfill 处理
    }

    for md_file in RAW_SOURCES.rglob("*.md"):
        # 跳过特定目录
        skip = False
        for sd in skip_dirs:
            if str(md_file).startswith(str(sd)):
                skip = True
                break
        if skip:
            continue

        content = md_file.read_text()
        h = compute_hash(content)
        if h not in processed_hashes:
            new_files.append(md_file)

    return new_files


def create_wiki_page(page_type: str, slug: str, title: str, tags: list,
                     summary: str, source_file: Path, content: str):
    """创建 wiki 页面"""
    today = datetime.now().strftime("%Y-%m-%d")
    rel_path = str(source_file.relative_to(WIKI_ROOT))

    type_dirs = {
        "entity": WIKI_ROOT / "entities",
        "concept": WIKI_ROOT / "concepts",
        "comparison": WIKI_ROOT / "comparisons",
        "query": WIKI_ROOT / "queries",
    }
    target_dir = type_dirs.get(page_type, WIKI_ROOT / "concepts")
    target_dir.mkdir(parents=True, exist_ok=True)

    page_file = target_dir / f"{slug}.md"
    if page_file.exists():
        print(f"    [SKIP] {slug}.md 已存在")
        return False

    tags_str = ", ".join(sorted(set(tags)))

    page_content = f"""---
title: {title}
created: {today}
updated: {today}
type: {page_type}
tags: [{tags_str}]
sources: [{rel_path}]
confidence: medium
---

# {title}

{summary}

## 相关页面

- [[hr-policy-daily]] — 全球HR政策日报
- [[quyu-guihua]] — 区域合规政策
"""
    page_file.write_text(page_content)
    print(f"    [CREATE] {page_type}/{slug}.md ← {rel_path}")
    return True


# ============================================================
# 主流程
# ============================================================
def main():
    dry_run = "--dry-run" in sys.argv

    print(f"\n{'[DRY-RUN] ' if dry_run else ''}Wiki Ingest — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    processed_hashes = get_processed_hashes()
    print(f"  已处理：{len(processed_hashes)} 个文件哈希")

    new_files = scan_new_files(processed_hashes)
    print(f"  新文件：{len(new_files)} 个")

    if not new_files:
        print("  → 无新文件需要 ingest")
        return

    all_hashes = set(processed_hashes)
    results = {"created": [], "skipped": []}

    for md_file in new_files:
        print(f"\n  处理：{md_file.name}")
        content = md_file.read_text()
        h = compute_hash(content)
        all_hashes.add(h)

        classification = llm_classify(content, md_file.name)
        print(f"    → type={classification.get('type','?')} slug={classification.get('slug','?')}")

        created = create_wiki_page(
            page_type=classification.get("type", "concept"),
            slug=classification.get("slug", md_file.stem),
            title=classification.get("title", md_file.stem),
            tags=classification.get("tags", []),
            summary=classification.get("summary", ""),
            source_file=md_file,
            content=content,
        )
        if created:
            results["created"].append(classification.get("slug", md_file.stem))
        else:
            results["skipped"].append(md_file.name)

    # 保存哈希
    if not dry_run:
        save_processed_hashes(all_hashes)

    # 记录 log
    if results["created"] and not dry_run:
        log_file = WIKI_ROOT / "log.md"
        log_entry = f"\n## {datetime.now().strftime('%Y-%m-%d %H:%M')} — Wiki Ingest\n"
        log_entry += f"- 新建页面：{', '.join(results['created'])}\n"
        log_entry += f"- 跳过：{', '.join(results['skipped'])}\n"
        if log_file.exists():
            existing = log_file.read_text()
            log_file.write_text(existing.rstrip() + log_entry)
        else:
            log_file.write_text(log_entry)

    print(f"\n完成：创建 {len(results['created'])} | 跳过 {len(results['skipped'])}")


if __name__ == "__main__":
    main()
