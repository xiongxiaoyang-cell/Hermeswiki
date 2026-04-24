# Session 隔离操作规范

> **目的**：避免长任务污染主 Agent context，将耗时操作隔离到 subagent 子会话中执行。

---

## 一、长任务 Spawn 规范

### 触发条件
- 任务预估耗时 **> 10 分钟**
- 任务涉及大量工具调用或上下文累积风险
- 用户明确要求"后台运行"或"异步执行"

### Spawn 执行流程

```
主 Agent                    Subagent
   |                            |
   |-- spawn (带清晰 task) ---->|
   |                            |-- 执行任务
   |                            |-- 写 tmp/T-YYYYMMDD-XXX/
   |                            |-- 写 logs/
   |<-- results auto-announce --|
   |                            |
```

### 命名规范（Task ID）
```
T-YYYYMMDD-XXX
```
- `YYYYMMDD`：任务日期
- `XXX`：当日序号，001 起算

**示例**：`T-20260324-001`

---

## 二、临时文件目录规范

### 标准目录结构
```
workspace/
├── tmp/
│   ├── T-YYYYMMDD-001/        # 单次任务工作区
│   │   ├── inputs/           # 原始输入文件
│   │   ├── outputs/          # 任务产出
│   │   └── meta.json         # 任务元信息（创建时间、状态、spawner）
│   ├── T-YYYYMMDD-002/
│   ├── drafts/                # 草稿文件（不纳入正式交付）
│   └── ...
├── logs/
│   ├── T-YYYYMMDD-001.log    # 任务执行日志
│   └── ...
└── scripts/
    └── cleanup_tmp.sh        # 定时清理脚本
```

### 文件命名
| 类型 | 命名规则 | 示例 |
|------|---------|------|
| 任务工作区 | `T-YYYYMMDD-NNN/` | `T-20260324-001/` |
| 输入文件 | `input_*.{ext}` | `input_data.csv` |
| 产出文件 | `output_*.{ext}` | `output_report.md` |
| 草稿文件 | `draft_*.{ext}` | `draft_v1.xlsx` |
| 日志文件 | `T-YYYYMMDD-NNN.log` | `T-20260324-001.log` |
| 元信息 | `meta.json` | 包含 task_id、created_at、status |

---

## 三、Subagent 任务元信息（meta.json）

每个独立任务工作区应包含 `meta.json`：

```json
{
  "task_id": "T-20260324-001",
  "created_at": "2026-03-24T13:45:00+08:00",
  "spawner": "agent:main:main",
  "description": "执行会话Context隔离优化",
  "status": "completed|failed|running",
  "deliverable": "docs/知识库/99_运营/Session隔离操作规范.md",
  "parent_session": "agent:main:subagent:xxxx"
}
```

---

## 四、交付物保留规则

以下文件**不受清理脚本影响**：

1. 所有 `docs/` 下的文件
2. `meta.json` 标记为 `status: completed` 且含 `deliverable` 路径的产出
3. `workspace/MEMORY.md`、`memory/` 下日常记录
4. `SOUL.md`、`USER.md`、`AGENTS.md`、`TOOLS.md`、`IDENTITY.md`

---

## 五、自动化清理脚本

见 `workspace/scripts/cleanup_tmp.sh`

### 执行方式
- **建议 cron**：每天 03:00 执行
- **手动执行**：`bash workspace/scripts/cleanup_tmp.sh --dry-run` 先预览

### 清理逻辑
1. 查找 `workspace/tmp/` 下 7 天前创建的目录
2. 跳过 `drafts/` 目录
3. 跳过含 `meta.json` 且 status 为 `completed` 且有 deliverable 的任务（需人工确认）
4. 删除符合条件的临时目录及日志

---

## 六、最佳实践

### 主 Agent 侧
- [ ] 分解任务时，预估耗时 > 10 分钟立即 spawn
- [ ] spawn 时提供**完整、明确的任务描述**，避免子任务反复提问
- [ ] 明确告知 subagent 交付物路径

### Subagent 侧
- [ ] 创建任务工作区时写入 `meta.json`
- [ ] 所有中间文件放在 `tmp/T-YYYYMMDD-NNN/` 内
- [ ] 最终交付物移动到 `docs/` 或其他稳定目录
- [ ] 完成后在 meta.json 写入 `status: completed` 和 `deliverable`
- [ ] 若任务失败，写入 `status: failed` 和 `error` 字段

---

*最后更新：2026-03-24*
