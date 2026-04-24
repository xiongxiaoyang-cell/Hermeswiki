# Git / GitHub / Gitee 配置与存储规则

> 本文件为单一真相源（SSOT），包含 Git 配置、LFS 使用、存储分层规范。

---

## 一、仓库地址

| 平台 | 地址 | 说明 |
|------|------|------|
| **GitHub** | https://github.com/xiongxiaoyang-cell/lobster | LFS 正常，1GB 免费额度 |
| **Gitee** | https://gitee.com/stuardyang/lobster | 免费版不支持 LFS push，文件以指针形式存在 |

**Gitee LFS 解决方案**：
```bash
GIT_LFS_SKIP_PUSH=1 git push origin master
# 推送时跳过 LFS Upload，Gitee 仅存指针文本，GitHub 存真实文件
```

**Gitee 免费版 LFS 限制**：
- Gitee 不支持 LFS push（报错 `cannot push lfs objects to server`）
- 解决：始终使用 `GIT_LFS_SKIP_PUSH=1` 绕过
- GitHub LFS 正常存储（推荐作为主要备份）
- 二进制文件在 Gitee 上为 LFS 指针文本（非真实内容），不影响使用

---

## 二、文件存储分层（永久规则）

| 内容类型 | 存储位置 | 上传规则 |
|---------|---------|---------|
| **知识库文本文件** | `docs/知识库/`（Git） | ✅ 强制上传 |
| **二进制文件（PPT/PDF/XLSX）** | 飞书云盘 | 本地不存储，只存链接 |
| **output/ 生成物** | `output/`（Git） | ✅ 每日 08:00 定时推送 |
| **飞书云盘文件** | ❌ 本地不存储 | 仅引用链接，不下载到仓库 |
| **memory/ 日志/状态** | ❌ 不上传 | .gitignore 保护 |
| **.env / node_modules** | ❌ 不上传 | .gitignore 保护 |
| **.gitignore 保护范围** | memory/*.json, memory/cache/, memory/.proactive_action_needed, .env, node_modules/, *.bak, *.log, 知识库/ |

---

## 三、知识库唯一路径规范

```
docs/知识库/     ← 唯一正确的知识库存储位置（强制）
知识库/          ← 禁止在仓库根目录创建，已加入 .gitignore
```

**原因**：
- 根目录 `知识库/` 曾因被 .gitignore 忽略而无法追踪，导致在 docs/知识库/ 重建，形成两个重复目录
- 合并后统一为 `docs/知识库/` 单一路径

**防范双知识库规则**：
1. ❌ 禁止在仓库根目录创建 `知识库/` 文件夹
2. ✅ 新文件添加前必须验证追踪状态：
   ```bash
   git add <文件路径>
   git status --short | grep <文件>
   # 如果不出现 → 路径在 .gitignore，先排查再继续
   ```
3. ✅ 定期检查：
   ```bash
   # 确认 git 追踪的知识库文件数量
   git ls-files | grep "docs/知识库" | wc -l
   # 检查本地未追踪的知识库文件
   git status -u | grep "知识库"
   ```

---

## 四、output/ 定时推送机制

- **推送时间**：每日 08:00 自动推送
- **触发条件**：有变更时自动 push，无变更则跳过
- **文件内容**：`output/slides/`（PPT）、`output/reports/`（报告）
- **已纳入**：08:00 cron 任务中 `git add -A`

---

## 五、飞书云盘文件规则（永久规则）

> **飞书云盘文件不存储到本地仓库**，只在知识库中保留下载链接。
> 飞书云盘路径：`https://zcnznz2njhia.feishu.cn/drive/`

---

## 六、知识库目录结构（2026-03-31 合并后）

```
docs/知识库/
├── 00_索引/          ← 知识库总览/目录索引/主题检索
├── 01_战略方法论/    ← 战略框架/方法论
├── 01_行业研究/      ← 行业研究
├── 02_区域政策/      ← 国家/地区政策
├── 03_人力资源/      ← HR合规/劳动法
├── 04_行业案例/      ← 客户案例
├── 05_课程运营/      ← 课件/PPT（二进制，GitHub LFS）
├── 06_自媒体/        ← 选题/IP运营
├── 07_咨询方法论/    ← 咨询框架
├── 07_用友薪福社/    ← 客户案例/报价体系
├── 08_合作生态/      ← 生态合作
└── 99_运营/          ← 运营规范/话术规范
```

---

## 七、出现重复时的判断与处理

| 现象 | 原因 | 处理 |
|------|------|------|
| `git ls-files` 显示 0 条知识库文件 | 文件未被追踪 | 检查 .gitignore，排除后再 `git add -f` |
| Gitee 显示空文件（二进制） | Gitee 免费版不支持 LFS | 正常现象，GitHub LFS 正常存储 |
| 根目录出现 `知识库/` | 误操作创建 | 立即删除并加入 .gitignore |
| `git add` 无响应 | 文件在 .gitignore | 检查 .git/info/exclude 和全局 excludes |

---

## 八、gitignore 防屏蔽规范（2026-03-31 新增）

### 危险模式（禁止使用）
```
知识库/        ❌ 会匹配 docs/知识库/、workspace/知识库/ 等所有路径级别
```

### 安全模式（必须使用）
```
/知识库/       ✅ 仅匹配仓库根目录的 知识库/
```

### 添加新 ignore 规则前必查
在 `.gitignore` 添加任何路径前，先验证：
```bash
# 验证不会误屏蔽重要目录
git check-ignore -v docs/知识库/某个文件.md
# 如果显示被忽略 → 路径有问题，需要加前缀 /
```

### 提交前强制检查清单（永久规则）
每次 `git add` 后、提交前，必须执行：
```bash
# 检查知识库文件是否被意外忽略
git status --short | grep "docs/知识库" | wc -l
# 结果为0且本地有文件 → 已被ignore，需要排查
```
