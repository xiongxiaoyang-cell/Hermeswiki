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
