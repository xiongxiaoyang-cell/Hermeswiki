# Wiki Schema — 锴哥出海人力资源知识库

## Domain
出海HR/EOR（人力资源外包）咨询服务：中企全球化扩张的人力资源战略、合规政策、薪酬体系、招聘策略、区域政策。

## Conventions
- 文件名：小写、连字符、无空格（如 `china-eor-policy-2026.md`）
- 每个wiki页面以YAML frontmatter开头（见下方模板）
- 使用 `[[wikilinks]]` 链接其他页面（每个页面至少2个出站链接）
- 更新页面时必须更新 `updated` 日期
- 每个新页面必须添加到 `index.md` 正确section下
- 每个操作必须追加到 `log.md`
- 多来源（3+）综合页面，在段落末尾附加 `^[raw/sources/...]` 溯源标记

## Frontmatter
```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: [from taxonomy below]
sources: [raw/sources/path.md]
confidence: high | medium | low
contested: true
contradictions: [other-page-slug]
---
```

## Tag Taxonomy
- **市场/区域：** 中国大陆/西欧/东南亚/中东/北美/拉美/日韩
- **客户：** 出海阶段（0-1/1-10/成熟期/全球化）、客户规模（微/小/中/大）
- **HR职能：** 合规/招聘/薪酬/绩效/组织架构/劳动法/签证/EOR
- **产品/服务：** EOR服务/猎头/咨询/培训
- **竞品/生态：** 用友薪福社/名义雇主/竞争对手
- **内容类型：** 方法论/政策/案例/课程/运营/备忘

## Page Thresholds
- **创建页面：** 实体/概念出现在2+来源，或在一个来源中处于核心地位
- **追加现有页面：** 来源提到已覆盖的内容
- **不创建页面：** 临时提及、微不足道的细节、超出领域范围的内容
- **拆分页面：** 超过200行时拆分为子主题
- **归档页面：** 内容完全被取代时移至 `_archive/`

## Update Policy
新信息与现有内容冲突时：
1. 检查日期 — 新来源通常取代旧来源
2. 真正矛盾时，注明双方立场和来源日期
3. 在frontmatter标记：`contradictions: [page-name]`
4. 在lint报告中提交用户审核
