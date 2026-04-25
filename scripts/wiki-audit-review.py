#!/usr/bin/env python3
"""
Wiki Audit Review — 审核修正工作流
用法：python3 wiki-audit-review.py <wiki-root> [--open]
      python3 wiki-audit-review.py <wiki-root> --resolve <audit-file> --decision accept|reject|defer

工作流：
1. audit/inbox/ 收集反馈文件（feedback）
2. review 脚本展示每个反馈，等待决策
3. 决策执行后归档到 audit/resolved/
"""
import sys
import json
import re
from pathlib import Path
from datetime import datetime

WIKI_ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "/home/b4ac5686610a4ae2/wiki")
INBOX = WIKI_ROOT / "audit" / "inbox"
RESOLVED = WIKI_ROOT / "audit" / "resolved"
INBOX.mkdir(exist_ok=True)
RESOLVED.mkdir(exist_ok=True)


def read_audit_file(path: Path) -> dict:
    """解析 audit 文件，返回结构化 dict"""
    content = path.read_text()
    # 支持 YAML frontmatter 或纯 Markdown
    frontmatter = {}
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm_text, body = parts[1], parts[2]
            for line in fm_text.strip().splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    frontmatter[k.strip()] = v.strip()
    return {
        "file": path.name,
        "frontmatter": frontmatter,
        "body": body.strip(),
        "raw": content,
    }


def get_wiki_target(frontmatter: dict, body: str) -> tuple:
    """从反馈中提取目标页面和位置"""
    page = frontmatter.get("page", "")
    line = frontmatter.get("line", "")
    # 尝试从正文提取 [[wikilink]] 引用
    links = re.findall(r"\[\[([^\]]+)\]\]", body)
    return page, line, links


def show_audit_item(item: dict):
    print(f"\n{'='*60}")
    print(f"📋 反馈文件: {item['file']}")
    fm = item['frontmatter']
    print(f"   来源: {fm.get('reporter', '未知')}")
    print(f"   页面: {fm.get('page', '未知')}")
    print(f"   类型: {fm.get('type', '内容修正')}")
    print(f"   时间: {fm.get('date', '未知')}")
    print(f"\n--- 反馈内容 ---")
    print(item['body'].strip())
    print(f"{'='*60}")


def apply_decision(item: dict, decision: str, notes: str = ""):
    """将决策应用到 wiki"""
    fm = item['frontmatter']
    page_name = fm.get("page", "")
    action = fm.get("action", "edit")

    result = {"decision": decision, "notes": notes, "resolved_at": datetime.now().isoformat()}

    if decision == "reject":
        result["action"] = "无操作"
        return result

    if decision == "defer":
        # 移入 defer 子目录
        defer_dir = INBOX / "deferred"
        defer_dir.mkdir(exist_ok=True)
        import shutil
        src = INBOX / item["file"]
        dst = defer_dir / item["file"]
        shutil.move(str(src), str(dst))
        result["action"] = f"延期 → audit/inbox/deferred/"
        return result

    # accept 或 partially_accept：执行修改
    if page_name:
        page_path = None
        for subdir in ["entities", "concepts", "comparisons", "queries"]:
            candidate = WIKI_ROOT / subdir / f"{page_name}.md"
            if candidate.exists():
                page_path = candidate
                break

        if page_path and action == "edit":
            # 简单替换逻辑：找到 <!-- AUDIT: old -->...<!-- /AUDIT: old --> 块并替换
            old_marker = f"<!-- AUDIT: {item['file']} -->"
            new_marker = f"<!-- AUDIT: {item['file']} -->"
            old_content = page_path.read_text()

            # 查找并替换标记内容
            pattern = rf"{re.escape(old_marker)}[\s\S]*?<!-- /AUDIT: {re.escape(item['file'])} -->"
            if re.search(pattern, old_content):
                new_content = re.sub(pattern, notes.strip(), old_content)
                page_path.write_text(new_content)
                result["action"] = f"已修改 {page_path.relative_to(WIKI_ROOT)}"
            else:
                # 在文件末尾追加
                append_note = f"\n\n<!-- AUDIT: {item['file']} -->\n{notes}<!-- /AUDIT: {item['file']} -->"
                page_path.write_text(old_content + append_note)
                result["action"] = f"已追加到 {page_path.relative_to(WIKI_ROOT)}"
        else:
            result["action"] = f"目标页面不存在: {page_name}"
    else:
        result["action"] = "无目标页面"

    return result


def archive_audit(item: dict, result: dict):
    """归档到 audit/resolved/"""
    resolved_file = RESOLVED / item["file"]
    fm = item["frontmatter"]
    content = f"""---
file: {item['file']}
date: {fm.get('date', '')}
reporter: {fm.get('reporter', '')}
page: {fm.get('page', '')}
type: {fm.get('type', '内容修正')}
decision: {result['decision']}
resolved_at: {result['resolved_at']}
action: {result['action']}
---

# 原始反馈

{item['raw']}

---

# 处理结果

**决策:** {result['decision']}
**时间:** {result['resolved_at']}
**操作:** {result['action']}

**备注:**
{result.get('notes', '')}
"""
    resolved_file.write_text(content)
    # 从 inbox 删除
    (INBOX / item["file"]).unlink()
    print(f"  ✅ 已归档: audit/resolved/{item['file']}")


def interactive_review(item: dict):
    """交互式审核流程"""
    show_audit_item(item)

    while True:
        print("\n操作选项:")
        print("  [a]cept   — 接受，修正 wiki")
        print("  [p]artial — 部分接受，执行部分修改")
        print("  [r]eject  — 拒绝，无需修改")
        print("  [d]efer  — 延期，暂不处理")
        print("  [v]iew   — 查看目标页面当前内容")
        print("  [q]uit   — 退出")
        choice = input("\n请选择: ").strip().lower()

        if choice == "q":
            return None

        if choice == "v":
            page = item['frontmatter'].get("page", "")
            if page:
                for subdir in ["entities", "concepts", "comparisons"]:
                    p = WIKI_ROOT / subdir / f"{page}.md"
                    if p.exists():
                        print(f"\n--- {p.relative_to(WIKI_ROOT)} ---")
                        print(p.read_text()[:500])
                        break
                else:
                    print(f"  页面不存在: {page}")
            else:
                print("  未指定页面")
            continue

        if choice in ("a", "accept"):
            notes = input("修改说明（直接回车确认）: ").strip()
            result = apply_decision(item, "accept", notes)
            archive_audit(item, result)
            return result

        if choice in ("p", "partial"):
            notes = input("部分修改说明: ").strip()
            result = apply_decision(item, "partially_accept", notes)
            archive_audit(item, result)
            return result

        if choice in ("r", "reject"):
            notes = input("拒绝原因: ").strip()
            result = apply_decision(item, "reject", notes)
            archive_audit(item, result)
            return result

        if choice in ("d", "defer"):
            result = apply_decision(item, "defer")
            archive_audit(item, result)
            return result


def main():
    if "--resolve" in sys.argv:
        # 非交互模式：直接处理指定文件
        idx = sys.argv.index("--resolve")
        audit_file = sys.argv[idx + 1]
        decision = "accept"
        notes = ""
        if "--decision" in sys.argv:
            idx2 = sys.argv.index("--decision")
            decision = sys.argv[idx2 + 1]
        if "--notes" in sys.argv:
            idx3 = sys.argv.index("--notes")
            notes = sys.argv[idx3 + 1]
        item = read_audit_file(INBOX / audit_file)
        result = apply_decision(item, decision)
        archive_audit(item, result)
        print(f"Done: {result}")
        return

    if "--open" in sys.argv:
        # 交互式审核 inbox
        inbox_files = sorted(INBOX.glob("*.md"))
        if not inbox_files:
            print("📪 inbox 为空，无待处理反馈")
            return

        print(f"\n📪 待审核反馈: {len(inbox_files)} 条")
        results = []
        for f in inbox_files:
            item = read_audit_file(f)
            result = interactive_review(item)
            if result is None:
                print("\n已退出")
                break
            results.append(result)

        print(f"\n{'='*60}")
        print(f"✅ 审核完成: {len(results)} 条已处理")
        return

    # 默认：显示帮助
    print(__doc__)


if __name__ == "__main__":
    main()
