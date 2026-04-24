# David 出海HR知识库 · Obsidian Vault

> 本目录是 llm-wiki 三层结构的 Layer 2（compiled wiki）。
> Layer 1 原始资料在 `raw/sources/`，Layer 3 索引在 `SCHEMA.md`。

## Vault 使用说明

1. 用 Obsidian 打开本目录（`File → Open vault → 选择此文件夹`）
2. 推荐插件：`Graph Analysis`（分析链接结构）、`Templater`（模板生成）
3. 核心快捷键：
   - `Ctrl/Cmd + O` — 搜索页面
   - `Ctrl/Cmd + Shift + F` — 全局搜索
   - `Ctrl/Cmd + G` — 打开图谱视图
   - `Ctrl/Cmd + E` — 切换编辑/预览

## 内容结构

| 目录 | 类型 | 说明 |
|------|------|------|
| `entities/` | 实体 | 15个国别/品牌/人物实体 |
| `concepts/` | 概念 | 19个方法论/流程/体系 |
| `comparisons/` | 对比 | 4个对比分析（报价/评估/案例/EOR）|
| `queries/` | 查询 | 1个选题库 |
| `raw/sources/` | 原始 | Layer 1 原始资料（不可变）|

## Wikilink 语法

- 页面链接：`[[页面名]]`
- 带别名：`[[页面名|显示文字]]`
- 跳转阅读：`Ctrl/Cmd + 点击` 链接

## frontmatter 属性（Obsidian Properties 面板）

```yaml
type: entity | concept | comparison | query
tags: [标签1, 标签2]
sources: [raw/sources/来源路径]
confidence: high | medium | low
created: YYYY-MM-DD
updated: YYYY-MM-DD
```

## 图谱导航建议

从以下页面开始浏览：
1. `index` — 全局目录
2. `zhongqi-chuhai-hr-tixi` — 出海HR全体系
3. `hr-policy-daily` — 政策监测核心池（22个出海目标国）
4. `eor-fuwu` — EOR四模式全对比
5. `yingguo` — 任意国别实体页
