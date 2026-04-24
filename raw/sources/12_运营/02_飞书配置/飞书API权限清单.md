# 飞书 API 权限清单

> 更新日期：2026-03-20
> 数据来源：飞书开放平台官方文档 + feishu_app_scopes 实际授权查询

---

## 一、当前已授权权限概览

| 类别 | 已授权数量 | 状态 |
|------|-----------|------|
| Bitable (多维表格) | 23 | ✅ 完整 |
| Calendar (日历) | 20 | ✅ 完整 |
| Drive (云盘) | 9 | ✅ 完整 |
| Docs (文档) | 20+ | ✅ 完整 |
| Wiki (知识库) | 14 | ✅ 完整 |
| IM (消息) | 30+ | ✅ 完整 |
| **总计** | **390** | ✅ |

---

## 二、Bitable（多维表格）API

### 2.1 权限清单

| 权限名称 | 说明 | 代码中的字段类型ID |
|---------|------|-------------------|
| `bitable:app` | 多维表格应用全权限 | - |
| `bitable:app:readonly` | 多维表格只读 | - |
| `base:app:create` | 创建多维表格应用 | - |
| `base:app:read` | 读取多维表格应用 | - |
| `base:app:update` | 更新多维表格应用 | - |
| `base:app:delete` | 删除多维表格应用 | - |
| `base:table:create` | 创建表格 | - |
| `base:table:read` | 读取表格 | - |
| `base:table:update` | 更新表格 | - |
| `base:table:delete` | 删除表格 | - |
| `base:field:create` | 创建字段 | - |
| `base:field:read` | 读取字段 | - |
| `base:field:update` | 更新字段 | - |
| `base:field:delete` | 删除字段 | - |
| `base:record:create` | 创建记录 | - |
| `base:record:read` | 读取记录 | - |
| `base:record:update` | 更新记录 | - |
| `base:record:delete` | 删除记录 | - |

### 2.2 字段类型（已验证）

| ID | 类型 | 创建参数示例 |
|----|------|-------------|
| 1 | Text | `type: 1` |
| 2 | Number | `type: 2` |
| 3 | SingleSelect | `type: 3, property: { options: ["A", "B"] }` |
| 4 | MultiSelect | `type: 4, property: { options: ["A", "B"] }` |
| 5 | DateTime | `type: 5` |
| 7 | Checkbox | `type: 7` |
| 11 | User | `type: 11` |
| 13 | Phone | `type: 13` |
| 15 | URL | `type: 15` |
| 17 | Attachment | `type: 17` |
| 18 | SingleLink | `type: 18` |
| 19 | Lookup | `type: 19` |
| 20 | Formula | `type: 20` |
| 21 | DuplexLink | `type: 21` |
| 22 | Location | `type: 22` |
| 23 | GroupChat | `type: 23` |
| 1001 | CreatedTime | `type: 1001` |
| 1002 | ModifiedTime | `type: 1002` |
| 1003 | CreatedUser | `type: 1003` |
| 1004 | ModifiedUser | `type: 1004` |
| 1005 | AutoNumber | `type: 1005` |

### 2.3 当前工具

| 工具名称 | 功能 |
|---------|------|
| `feishu_bitable_get_meta` | 解析Bitable URL，获取app_token和table_id |
| `feishu_bitable_list_fields` | 列出表格所有字段 |
| `feishu_bitable_list_records` | 列出表格记录（支持分页） |
| `feishu_bitable_get_record` | 获取单条记录 |
| `feishu_bitable_create_record` | 创建新记录 |
| `feishu_bitable_update_record` | 更新记录 |
| `feishu_bitable_create_app` | 创建新Bitable应用 |
| `feishu_bitable_create_field` | 创建新字段 |

---

## 三、Calendar（日历）API（新增）

### 3.1 权限清单

- **概览**: https://open.feishu.cn/document/server-docs/bitable-api-overview
- **API列表**: https://open.feishu.cn/document/server-docs/application-scope/scope-list (搜索 "bitable" 或 "base")

---

## 三、Calendar（日历）API

### 3.1 权限清单

| 权限名称 | 说明 |
|---------|------|
| `calendar:calendar` | 日历全权限 |
| `calendar:calendar:create` | 创建日历 |
| `calendar:calendar:read` | 读取日历 |
| `calendar:calendar:update` | 更新日历 |
| `calendar:calendar:delete` | 删除日历 |
| `calendar:calendar:readonly` | 日历只读 |
| `calendar:calendar.event:create` | 创建日历事件 |
| `calendar:calendar.event:read` | 读取日历事件 |
| `calendar:calendar.event:update` | 更新日历事件 |
| `calendar:calendar.event:delete` | 删除日历事件 |
| `calendar:calendar.event:reply` | 回复日历事件 |
| `calendar:calendar.acl:create` | 创建日历权限 |
| `calendar:calendar.acl:read` | 读取日历权限 |
| `calendar:calendar.acl:delete` | 删除日历权限 |
| `calendar:calendar.free_busy:read` | 读取忙闲状态 |
| `calendar:calendar:subscribe` | 订阅日历 |
| `calendar:timeoff` | 休假管理 |
| `calendar:time_off:create` | 创建休假 |
| `calendar:time_off:delete` | 删除休假 |
| `calendar:settings.workhour:read` | 读取工作时间 |

### 3.2 当前状态

- **工具**: 暂无专用 Calendar 工具
- **消息功能**: 支持通过 `feishu_chat` 获取日历相关群聊信息

### 3.3 官方文档

- **概览**: https://open.feishu.cn/document/server-docs/calendar-api-overview

---

## 四、Docs（文档）API

### 4.1 权限清单

| 权限名称 | 说明 |
|---------|------|
| `docx:document` | 文档全权限 |
| `docx:document:readonly` | 文档只读 |
| `docx:document:create` | 创建文档 |
| `docx:document.block:convert` | 块转换(表格) |
| `docx:document:write_only` | 文档只写 |
| `docs:doc` | 旧版文档 |
| `docs:doc:readonly` | 旧版文档只读 |
| `docs:permission.member` | 权限成员管理 |
| `docs:permission.member:create` | 添加成员 |
| `docs:permission.member:delete` | 删除成员 |
| `docs:permission.member:update` | 更新成员 |
| `docs:permission.member:readonly` | 成员只读 |
| `docs:permission.setting` | 权限设置 |
| `docs:document:import` | 导入文档 |
| `docs:document:export` | 导出文档 |
| `docs:document:copy` | 复制文档 |

### 4.2 当前工具

| 工具名称 | 功能 |
|---------|------|
| `feishu_doc` | 文档读取/写入/创建/表格操作 |

### 4.3 官方文档

- **概览**: https://open.feishu.cn/document/server-docs/document-api-overview

---

## 五、Drive（云盘）API

### 5.1 权限清单

| 权限名称 | 说明 |
|---------|------|
| `drive:drive` | 云盘全权限 |
| `drive:drive:readonly` | 云盘只读 |
| `drive:file` | 文件权限 |
| `drive:file:readonly` | 文件只读 |
| `drive:file:upload` | 文件上传 |
| `drive:file:download` | 文件下载 |
| `drive:drive:version` | 版本管理 |
| `drive:drive.search:readonly` | 搜索只读 |

### 5.2 当前工具

| 工具名称 | 功能 |
|---------|------|
| `feishu_drive` | 云盘文件管理（列表/创建文件夹/移动/删除） |

### 5.3 官方文档

- **概览**: https://open.feishu.cn/document/server-docs/drive-api-overview

---

## 六、Wiki（知识库）API

### 6.1 权限清单

| 权限名称 | 说明 |
|---------|------|
| `wiki:wiki` | 知识库全权限 |
| `wiki:wiki:readonly` | 知识库只读 |
| `wiki:node:create` | 创建节点 |
| `wiki:node:read` | 读取节点 |
| `wiki:node:update` | 更新节点 |
| `wiki:node:delete` | 删除节点 |
| `wiki:node:move` | 移动节点 |
| `wiki:space:read` | 读取空间 |
| `wiki:space:write_only` | 空间只写 |
| `wiki:space:retrieve` | 获取空间信息 |
| `wiki:member:create` | 创建成员 |
| `wiki:member:update` | 更新成员 |
| `wiki:member:retrieve` | 获取成员 |

### 6.2 当前工具

| 工具名称 | 功能 |
|---------|------|
| `feishu_wiki` | 知识库节点管理（列表/创建/移动/重命名） |

### 6.3 官方文档

- **概览**: https://open.feishu.cn/document/server-docs/wiki-api-overview

---

## 七、其他常用 API

### 7.1 IM（消息）

| 权限名称 | 说明 |
|---------|------|
| `im:message` | 消息发送 |
| `im:message:send_as_bot` | 以机器人发送 |
| `im:chat:create` | 创建群聊 |
| `im:chat:update` | 更新群聊 |
| `im:chat:delete` | 删除群聊 |
| `im:chat.members:read` | 读取群成员 |
| `im:chat.members:write_only` | 管理群成员 |

### 7.2 Contacts（通讯录）

| 权限名称 | 说明 |
|---------|------|
| `contact:user.base:readonly` | 用户基本信息只读 |
| `contact:user.basic_profile:readonly` | 用户基本资料只读 |
| `contact:user.id:readonly` | 用户ID只读 |
| `contact:user.phone:readonly` | 用户手机号只读 |
| `contact:user.email:readonly` | 用户邮箱只读 |

---

## 八、官方资源汇总

| 资源 | 链接 |
|------|------|
| API概览 | https://open.feishu.cn/document/server-docs/api-call-guide/server-api-list |
| 权限列表 | https://open.feishu.cn/document/server-docs/application-scope/scope-list |
| Bitable API | https://open.feishu.cn/document/server-docs/bitable-api-overview |
| Calendar API | https://open.feishu.cn/document/server-docs/calendar-api-overview |
| Drive API | https://open.feishu.cn/document/server-docs/drive-api-overview |
| Docs API | https://open.feishu.cn/document/server-docs/document-api-overview |
| Wiki API | https://open.feishu.cn/document/server-docs/wiki-api-overview |
| 开发者后台 | https://open.feishu.cn/app |

---

## 九、权限申请步骤

1. 登录 [飞书开发者后台](https://open.feishu.cn/app)
2. 创建或选择应用
3. 进入「权限管理」
4. 搜索需要的 API 权限
5. 申请并等待管理员审批
6. 使用 `feishu_app_scopes` 工具查询已授权权限

---

*更新：2026-03-20*
