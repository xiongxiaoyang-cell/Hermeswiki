# Wiki Log

> 全部wiki操作的按序记录。Append-only。
> 格式：`## [YYYY-MM-DD] action | subject`
> 操作类型：ingest, update, query, lint, create, archive, delete
> 超过500条时轮换：重命名为 `log-YYYY.md`，新建空文件。

## [2026-04-24] create | Wiki initialized
- Domain: 出海HR/EOR咨询服务
- 从 `~/hermes_move_temp/` 迁移原始资料至 `raw/sources/`
- 结构：entities/ concepts/ comparisons/ queries/ _archive/
- SCHEMA.md / index.md / log.md 创建完成

## [2026-04-24] ingest | Layer 2 初始化编译
- 从 `raw/sources/01_战略方法论/中企出海HR全体系知识库V5整合版.md` 编译：
  - 创建: [[zhongqi-chuhai-hr-tixi]], [[chuhai-san-jieduan]], [[hegui-fengkong]], [[eor-fuwu]]
- 从 `raw/sources/09_用友薪福社/` 编译：
  - 创建: [[yonyou-xinfushe]], [[yongyou-baojia]]
- 从 `raw/sources/05_行业案例/名创优品MINISO_全球HR系统/` 编译：
  - 创建: [[miniso]]
- 从 `raw/sources/04_人力资源/工具模板/` 编译：
  - 创建: [[chuhai-pinggu]] (出海快速评估表)
- index.md 更新：7 pages total

## [2026-04-24] cross-ref | 建立双向链接网络
- 修复15条死链：替换错误wikilink → 正确slug
- 创建缺失但被引用的stub页面：
  - entities: [[jiaokong-vietnam-eor]]
  - concepts: [[zuzhi-jiagou]], [[zhaopin]], [[xinchou]], [[quyu-guihua]], [[zhongxiao-chuhai]], [[luodi-10bu]], [[hegui-shengsi]]
  - comparisons: [[hangye-anli]]
- 孤立页全部消除（0 orphans）
- 全部17个wiki页面出站链接≥2
- index.md 更新：17 pages total

## [2026-04-24] ingest | 政策日报 + 国家实体页
- 创建 [[hr-policy-daily]]：全球HR政策日报监测系统说明，核心池+轮询池机制
- 创建国家实体页（6个）：
  - [[xinjapo]] — 新加坡（EP门槛/CPF/执法）
  - [[yuenan]] — 越南（最低工资+7.2%/电子合同强制）
  - [[hanguo]] — 韩国（KRW 10,320/小时/社保上调）
  - [[bolan]] — 波兰（PLN 4,806/服务年限定义扩大）
  - [[shate]] — 沙特（Nitaqat本国工资SAR 4,000/5年居留证）
  - [[xiongyali]] — 匈牙利（HUF 322,800/电子社保手册）
- index.md 更新：24 pages total

## [2026-04-24] ingest | 人力资源+用友产品+自媒体
- 04_人力资源：扩展 [[eor-fuwu]] 为四模式全对比（新增IC/外派/自雇佣对比）
- 新增 [[hegui-sida-lingyu]]：合规四大领域详解（用工/薪税/移民/数据合规，含社保费率表）
- 新增 [[yongyou-hailie]]：用友海猎猎头服务
- 新增 [[yongyou-payroll]]：用友Payroll薪税核算与发放服务
- 新增 [[yongyou-qianzheng]]：用友签证服务，附各国签证特点
- 07_自媒体：新增 [[zimeiti-yunying]]（账号矩阵/IP定位/内容策略）
- 07_自媒体：新增 [[redian-ku]]（热点追踪系统）
- 07_自媒体：新增 [[zixuan-ku]]（选题库）
- index.md 更新：31 pages total

## [2026-04-24] ingest | 课程+龙虾+人物+市场分析
- 新增 [[yang-kai]] — 杨锴完整画像（身份/任职/方法论/IP矩阵）
- 新增 [[longxia-ai-agent]] — 龙虾AI智能体（C→C闭环/360合作/技能封装/分工）
- 新增 [[chuhai-hr-course]] — 出海HR课程体系（7讲课/培训产品/龙虾商业化）
- 新增 [[xunhe-ec]] — 迅合渠道（大会/私董会/69800产品/龙虾增值）
- 新增 [[german-eor]] — 德国EOR市场（SAM 1200-1800万美元/6大壁垒/竞争定价）
- 新增 [[shai-chai-pei]] — 筛·拆·配实战框架（杨锴原创方法论）
- 新增 [[yongkai-memo]] — 锴哥业务备忘
- index.md 更新：38 pages total

## [2026-04-24] ingest | 补全政策日报国家池
- 新增9个实体页：[[yingguo]]英国/[[deguo]]德国/[[faguo]]法国/[[helan]]荷兰/[[xibanya]]西班牙/[[yidali]]意大利/[[baxi]]巴西/[[riben]]日本/[[yindu]]印度
- 更新 [[hr-policy-daily]]：核心池表格扩展至22个出海目标国，wikilink全连接
- 更新 [[quyu-guihua]]：区域合规表全添加wikilink，消除所有孤立页
- lint：47 pages，0死链，0孤立
- index.md 更新：47 pages total
## 2026-04-24 16:09 — 政策日报整合
- 扫描日报：5份
- 更新 entity：baxi, bolan, deguo, faguo, hanguo, helan, riben, shate, xibanya, xinjapo, xiongyali, yidali, yindu, yingguo, yuenan
- 新建 entity：ahlianda, feilvbin, jianada, malaixiya, meiguo, moxige, taiguo
- 总条目：44条
## 2026-04-24 16:33 — Wiki Lint
- 死链：0 | 孤立页：7 | 警告：0
- 🟡 孤立页：malaixiya.md（无入站链接）
- 🟡 孤立页：meiguo.md（无入站链接）
- 🟡 孤立页：jianada.md（无入站链接）
- 🟡 孤立页：moxige.md（无入站链接）
- 🟡 孤立页：taiguo.md（无入站链接）
- 🟡 孤立页：feilvbin.md（无入站链接）
- 🟡 孤立页：ahlianda.md（无入站链接）
## 20260424 — Wiki Compile
- 模板：assessment
- 输出：/tmp/test-assessment.md
## 20260424 — Wiki Compile
- 模板：policy-report
- 输出：/tmp/test-policy.md
## 20260424 — Wiki Compile
- 模板：training
- 输出：/tmp/test-training.md
## 20260424 — Wiki Compile
- 模板：client-report
- 输出：/tmp/test-client.md
## 2026-04-24 — Wiki Compile 完成
- 模板1（assessment）：出海潜客评估报告 — 87/120分算法 + 6维度评分条 + 国别详情 + EOR分析
- 模板2（policy-report）：HR政策合规周报 — 最低工资快照 + 重大变化分类（红黄绿）
- 模板3（training）：客户培训材料 — 模块化组装，支持 topics 参数
- 模板4（client-report）：客户综合咨询报告 — 阶段+模式+国别+行动建议完整结构
- 脚本：scripts/wiki-compile.py（~620行，4模板×4参数组合）
- 用法：python3 scripts/wiki-compile.py --template assessment --company X --countries deguo,yuenan --stage 1-10
## 2026-04-24 16:59 — Wiki Lint
- 死链：0 | 孤立页：2 | 警告：0
- 🟡 孤立页：new-concept.md（无入站链接）
- 🟡 孤立页：new-compare.md（无入站链接）
## [2026-04] audit | Monthly KB Health Report
- Pages: 54 total（30 entities / 19 concepts / 4 comparisons / 1 queries）
- Dead links: 0
- Orphan pages: 0
- Health: ✅ PASS
- Raw sources: 252 files
- Notes: 删除2个空占位页(new-concept/new-compare)；Wiki Lint cron已验证✅；Wiki Compile脚本上线
- Cron: b87ac8ebc278，每月1日09:00执行
## 2026-04-24 — _index 主题索引完成
- 创建主题索引：xiwang-quyu, dongnanya-quyu, hegui-zhengce, yonggong-moshi, chuhai-jieduan, yongyou-shengtai, xin chou-xincha, zimeiti-yunying
- 总索引：_index.md
## 2026-04-24 — _index 主题索引完成
- 创建主题索引：xiwang-quyu, dongnanya-quyu, hegui-zhengce, yonggong-moshi, chuhai-jieduan, yongyou-shengtai, xinchou-shebao, zimeiti-yunying
- 总索引：_index.md
## 2026-04-24 — _index 主题索引完成（④b+⑨）
- _index/ 目录创建：8个主题索引页
  - xiwang-quyu：西欧市场（德国/英国/法国/荷兰/意大利/西班牙/波兰/匈牙利）
  - dongnanya-quyu：东南亚市场（越南/新加坡/泰国/马来西亚/印尼/菲律宾）
  - hegui-zhengce：合规政策体系（23个页面）
  - yonggong-moshi：用工模式全解
  - chuhai-jieduan：出海阶段与模式选择
  - yongyou-shengtai：用友薪福社生态
  - xinchou-shebao：薪酬与社保
  - zimeiti-yunying：自媒体运营
- 总索引：_index.md（按区域+职能双维度导航）
- 生成脚本：scripts/wiki-index-gen.py
- lint：✅ 0死链 0孤立
- GitHub: ee2e0da5
## 2026-04-24 — wikilink 自动关联（⑧）
- 阈值：共享 tag ≥ 2 | confidence ≠ low
- 关联了：longxia-ai-agent, feilvbin, yongyou-hailie, malaixiya, chuhai-san-jieduan, luodi-10bu, yongyou-payroll, yongyou-qianzheng, shai-chai-pei, yongyou-baojia
- 新增链接总数：13 条
## 2026-04-24 — wikilink 自动关联完成（⑧）
- 阈值：共享 tag ≥ 2 | confidence ≠ low
- 排除泛化 tag：合规/国家/最低工资/社保（entity中出现>10次）
- 新增关联：10个页面，涉及13条新 wikilink
  - feilvbin ↔ malaixiya（东南亚）
  - yongyou-hailie ↔ yongyou-payroll ↔ yongyou-qianzheng（用友产品线）
  - chuhai-san-jieduan ↔ zuzhi-jiagou（出海+组织架构）
  - luodi-10bu ↔ shai-chai-pei（落地+筛拆配）
  - yongyou-baojia ↔ german-eor（用友+德国市场）
  - longxia-ai-agent ↔ chuhai-hr-course（龙虾+课程）
- 脚本：scripts/wiki-link-auto.py
- lint：✅ 0死链 0孤立
- GitHub: 4e3dbdb6
## 2026-04-24 17:48 — Wiki Lint
- 死链：4 | 孤立页：2 | 警告：0
- 🔴 死链：[[chuhai-hr-tiaozhan]]
- 🔴 死链：[[EOR服务]]
- 🔴 死链：[[chuhai-daichuan-management]]
- 🔴 死链：[[出海HR三阶段]]
- 🟡 孤立页：chuhai-daichuan-management.md（无入站链接）
- 🟡 孤立页：chuhai-hr-tiaozhan.md（无入站链接）
## 2026-04-24 17:48 — Wiki Lint
- 死链：4 | 孤立页：2 | 警告：0
- 🔴 死链：[[chuhai-hr-tiaozhan]]
- 🔴 死链：[[出海HR三阶段]]
- 🔴 死链：[[chuhai-daichuan-management]]
- 🔴 死链：[[EOR服务]]
- 🟡 孤立页：chuhai-daichuan-management.md（无入站链接）
- 🟡 孤立页：chuhai-hr-tiaozhan.md（无入站链接）
## 2026-04-24 17:49 — Wiki Lint
- 死链：2 | 孤立页：1 | 警告：0
- 🔴 死链：[[chuhai-daichuan-management]]
- 🔴 死链：[[chuhai-hr-tiaozhan]]
- 🟡 孤立页：chuhai-daichuan-management.md（无入站链接）
## 2026-04-24 17:49 — Wiki Lint
- 死链：2 | 孤立页：1 | 警告：0
- 🔴 死链：[[chuhai-hr-tiaozhan]]
- 🔴 死链：[[chuhai-daichuan-management]]
- 🟡 孤立页：chuhai-daichuan-management.md（无入站链接）
## 2026-04-24 17:49 — Wiki Lint
- 死链：2 | 孤立页：1 | 警告：0
- 🔴 死链：[[chuhai-daichuan-management]]
- 🔴 死链：[[chuhai-hr-tiaozhan]]
- 🟡 孤立页：chuhai-daichuan-management.md（无入站链接）
## 2026-04-24 17:50 — Wiki Lint
- 死链：2 | 孤立页：1 | 警告：0
- 🔴 死链：[[出海盗船管理框架]]
- 🔴 死链：[[出海中企HR挑战]]
- 🟡 孤立页：chuhai-daichuan-management.md（无入站链接）

## [2026-04-25] ingest | hr-policy-daily scan + entity update
- 扫描: 核心池E组（越南、英国、美国、德国、法国、荷兰）+ 轮询池（加拿大、马来西亚、菲律宾、日本）
- 🔴重大更新×2:
  - 美国USVI最低工资 $10.50→$12/小时 (生效2026-04-24)
  - 马来西亚EP薪资门槛翻倍，Category I RM 10,000→20,000 (生效2026-06-01)
- 新增日报: [[raw/sources/03_区域政策/政策日报/20260425|20260425]]
- 更新实体: [[meiguo|美国]].md, [[malaixiya|马来西亚]].md
- 更新状态: hr-policy-countries.json (scan_round 7)
