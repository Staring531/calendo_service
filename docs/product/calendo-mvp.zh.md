# Calendo MVP 产品文档（官网 / 后端 / MCP）

> 本文由 `calendo-mvp.docx`（同目录，原始文档）于 2026-11-05 转换而来，此后以本文为准维护。原文的架构图与里程碑图未随 .docx 导出，下文以说明代替。

## 概览

Calendo 是面向 AI agent 的节假日与工作日服务，建立在开源库 vacanza/holidays 之上。MVP 的取舍：中国先行，逐日核对到国务院放假通知；其他国家用同一套接口提供，但明确标注「未核验」。三个产品共用一个核心，各管一层。

| 产品 | 一句话 | 主要用户 | MVP 交付物 |
|---|---|---|---|
| 后端 | 核心库 + HTTP API：包装 holidays，补上状态标注与日期类型判定 | 官网、开发者 | Python 核心 + 7 个只读接口 |
| MCP | 面向 LLM 客户端的原生 MCP 服务，直接调用核心 | AI agent、Claude/Cursor 等客户端 | 公共远程端点 + 7 个工具 |
| 官网 | calendo.day：介绍、接入指南、在线试用 | 开发者、潜在客户 | 单页站点 + 接入文档 + 在线查询 |

部署形态：容器化的 Python 服务，托管位置待定（见待决问题）。

MVP 不做：私有化/离线部署（已定为 backlog）、信创与信通院认证、服务端机器翻译、交易所休市日历、账号与计费。

## 用户与场景

MVP 不绑定任何内部系统，验证靠一份有标准答案的问题集。

| 优先级 | 用户 | 典型问题 | 对应能力 |
|---|---|---|---|
| P0 | AI agent（经 MCP） | 「2025-10-11 要上班吗？」「9 月 26 日之后的第 3 个工作日是哪天？」 | get_day_info、add_workdays |
| P1 | 开发者（经 HTTP API） | 「2025-09-29 到 10-12 有几个工作日？」「2026 年有哪些连休？」 | count_workdays、list_long_breaks |
| P2 | 官网访客 | 选一个国家和日期，试一次 | 在线试用，调用 HTTP API |

上表三个示例的答案（要上班、2025-09-30、5 天）取自库 v0.108 的实测输出，尚未与国务院通知逐日核对，核对由夹具完成（见「数据状态与校验」）。

## 库的能力边界（v0.108）

下表来自对 holidays 0.108 的实测和官方文档，决定了 Calendo 要在库之上补哪几层。

| 事项 | 事实 | 来源 | 对设计的影响 |
|---|---|---|---|
| 覆盖面 | 250 个国家/地区实体，214 个带本地化；en_US 覆盖 214 个，zh_CN 只有 5 个 | 实测 | 多数国家没有中文名，返回 en_US 名称 + 本地名，翻译交给 LLM 客户端 |
| 中国数据 | 无子区划；类别为 public 与 half_day；语言为 en_US、th、zh_CN、zh_TW | 实测、文档 | 中文名称可直接用 |
| 中国年份 | 特殊假期表覆盖 2001–2026，依据国务院办公厅通知；2027 年没有补班日；任意年份（1950–2100）都会给出结果且不提示 | 文档、实测 | 年份白名单 + 状态标注，2027 标 provisional |
| 调休 | 补班日在 weekend_workdays（2025 年 5 个、2026 年 6 个）；调休出来的休息日以节日条目出现，名称形如「休息日（由 2026-01-04 调休）」 | 实测 | 日期类型由 Calendo 判定：法定节日、调休休息日、补班日、周末、工作日 |
| 工作日判定 | is_working_day 已计入补班日；get_working_days_count 为闭区间，2025-09-29 到 10-12 返回 5；各国周末不同（沙特为周五、周六） | 实测 | 工作日工具可对所有国家开放 |
| N 个工作日后 | get_nth_working_day 从非工作日出发时，n=0 与 n=1 结果相同（2025-10-02 都得到 10-09） | 实测 | 工具描述写明这一语义，并用测试固定 |
| 下一个节日 | get_closest_holiday 逐日返回，不跳过正在进行的连休（2025-10-02 向前得到 10-03） | 实测 | 要「下一个连休」用 list_long_breaks |
| 连休 | list_long_breaks 返回连续的节日段；2026 年中国 7 段，最长为 2 月 15 日至 23 日共 9 天 | 实测 | 作为第 7 个工具 |
| 半天假 | half_day 类别含 2026-03-08、06-01、08-01；启用后这些日子的 is_working_day 为 False | 实测 | 默认不启用，避免把半天假当整天休息 |
| 语言 | 请求不支持的语言时静默退回原文（fr 得到中文名）；language=None 时读环境变量推断 | 实测、文档 | 内部一律显式传 language，并回传实际使用的语言 |
| 同日多名称 | get 用分号拼接多个名称，get_list 返回列表 | 文档 | 一律用 get_list |
| 交易所日历 | financial_holidays 覆盖多家交易所，上交所 XSHG 2026 年返回 22 条 | 实测 | 不进 MVP，列入后续 |

## 整体架构与产品边界

*原文此处为整体架构图，未随 .docx 导出。*

两个入口（MCP、HTTP API）调用同一个核心，核心是唯一的数据出口，官网只调用 HTTP API。核心做四件事：显式指定语言、只放行白名单年份、按校验清单给每个（国家, 年份）标注状态、判定日期类型。清单由 CI 生成，运行时只读；库本身固定版本、本地调用、不联网。

## 产品一：后端（核心 + HTTP API）

后端 = Calendo 核心（Python 包，位于 src/calendo/）+ 一层只读 HTTP API。核心把 holidays 的 dict 式接口包装成带类型的返回值（类型先行：schemas 在实现之前定义），MCP 与 HTTP API 都只是它的适配器。

### 每条日期的返回字段

- date、country、subdiv（可选）
- type：statutory_holiday（法定节日）/ shifted_rest_day（调休休息日）/ adjusted_workday（补班日）/ weekend / workday
- is_working_day：直接取库的判定
- name（按请求语言；库不支持时退回 en_US，再不行用本地语言）、name_local、lang_used（实际使用的语言）
- status：official / cross_checked / unverified / provisional（定义见「数据状态与校验」）
- data_version：该（国家, 年份）数据块的内容哈希

### MVP 接口（全部只读，/v1 前缀）

| 接口 | 作用 | 关键参数 | 库接口 |
|---|---|---|---|
| GET /countries | 支持的国家、语言、子区划 | 无 | list_supported_countries、list_localized_countries |
| GET /holidays | 某国某年的节日与调休 | country、year、lang、subdiv、include_half_day | country_holidays(years=…)、get_list |
| GET /days/{date} | 某天的类型与名称 | country、lang、subdiv | get_list、weekend_workdays、is_working_day |
| GET /workdays/count | 区间内工作日数（含两端） | country、from、to | get_working_days_count |
| GET /workdays/add | 从某日起加（减）N 个工作日 | country、from、days | get_nth_working_day |
| GET /holidays/next | 下一个（上一个）节日 | country、from、direction | get_closest_holiday |
| GET /breaks | 某年的连休 | country、year、min_length | list_long_breaks |

### 验收要求

- 数据：中国 2025–2026 的每个节日、调休休息日、补班日与夹具逐日一致；2027 标 provisional，且返回中带说明。
- 语义：区间含两端；add_workdays 从非工作日出发的行为有测试固定；next 逐日返回。
- 年份：白名单（暂定 2025–2027）之外返回明确的 year_not_supported，不返回空数组。
- 其他错误：未知国家码、非法日期、disputed 数据块（data_under_review）均返回明确错误码。
- 离线：运行时没有任何外部网络调用，测试在断网环境下运行。

## 产品二：MCP Server

MCP 是首发产品，也是最薄的一层：原生实现 MCP 协议，工具与核心函数一一对应，直接调用核心，不经过 HTTP API，不是 REST 到 MCP 的转译壳。部署为公共远程端点，客户端填一个 URL 即可接入。

| 工具 | 回答的问题 | 主要入参 |
|---|---|---|
| list_supported_countries | 支持哪些国家、语言、子区划 | 无 |
| list_holidays | 某国某年有哪些节日与调休 | country、year、lang、include_half_day |
| get_day_info | 某天是节日、调休休息日、补班日、周末还是工作日 | date、country、lang |
| count_workdays | 区间内（含两端）有几个工作日 | country、from、to |
| add_workdays | N 个工作日后（前）是哪天 | country、from、days |
| next_holiday | 下一个（上一个）节日是哪天 | country、from、direction |
| list_long_breaks | 某年有哪些连休（小长假） | country、year、min_length |

### 设计要求

- 工具描述写给模型读：何时该用、日期用 ISO（YYYY-MM-DD）、国家用 ISO 3166-1 alpha-2、区间含两端、返回字段含义。
- add_workdays 的描述写明：起点不是工作日时，days=0 与 days=1 都返回下一个工作日。
- 每次返回带 status 与 data_version；provisional、unverified 时附一句自然语言说明，供模型转述给用户。
- 语言：lang 缺省 zh_CN；库不支持该语言时退回 en_US，并写明 lang_used，另附 name_local，翻译交给 LLM 客户端。
- 无状态、无鉴权；错误信息用自然语言写明原因与修正方式。

验收：在 Claude 与至少一个其他 MCP 客户端中，用 10 条有标准答案的中文问题（含调休、跨年、跨国、半天假、2027 年尚未发布）全部调用到正确工具，答案与核心一致。

## 产品三：官网

官网的 MVP 只做一件事：让开发者在 2 分钟内完成接入并相信数据是对的。它是静态单页站点，只调用后端的公开 HTTP API，托管位置待定。

| 模块 | 内容 | 必要性 |
|---|---|---|
| 首屏 | 一句话定位 + 「复制 MCP 地址」按钮 | 必须 |
| 接入指南 | Claude、Cursor 等客户端的配置片段与示例提问 | 必须 |
| 在线试用 | 选国家、日期，调用后端展示类型、名称、status | 必须 |
| 工具与接口说明 | 7 个工具与 7 个接口的参数、返回示例 | 必须 |
| 数据说明 | 数据来源（vacanza/holidays）、状态含义、年份范围、已知限制 | 必须 |
| 中英文切换 | 站点自身中英双语 | 必须 |
| 变更日志 | 数据版本与发布记录 | 可选 |

验收：新用户从打开官网到在自己的客户端里成功问出一次「某天是不是工作日」不超过 2 分钟。

不做：账号、API Key、计费、博客、私有化部署销售页。

## 数据状态与校验

运行时只用 holidays（固定版本）。数据对不对，由 CI 里的两道检查决定，结果写进校验清单；运行时据清单给每个（国家, 年份）标注状态。

| 层 | 来源 | 作用 | 冲突时 |
|---|---|---|---|
| 权威层 | 中国：国务院放假通知，人工录入为夹具（附通知链接） | 决定 official；逐日比对库的输出 | 以夹具为准；库与夹具不一致则 CI 失败 |
| 基线层 | vacanza/holidays（MIT），固定版本，本地调用 | 运行时的数据与计算 | 被夹具校验；升级版本时对比各块哈希 |
| 校验层 | Nager.Date 公开 API，仅在 CI 拉取 | 按（国家, 年份）比对基线层 | 不一致标 disputed，裁决前不对外提供 |

| 状态 | 含义 | MVP 范围 |
|---|---|---|
| official | 与已录入的政府通知夹具逐日一致 | 中国 2025–2026 |
| cross_checked | 库与 Nager.Date 在该（国家, 年份）一致，但没有官方夹具 | CI 能比对到的国家 |
| unverified | 只有库的数据，没有做过校验 | 其余国家与年份 |
| provisional | 该年份没有已发布的官方安排，库按规则推算 | 中国 2027 |
| disputed | 库与 Nager.Date 不一致 | 不对外提供，返回 data_under_review |

| 事项 | MVP 决定 |
|---|---|
| 数据源 | vacanza/holidays，版本写入 uv.lock；不调用任何在线 API |
| 禁用来源 | 不引用、不抓取 Calendarific 的假日描述文本（版权风险） |
| 仅作接口参考 | HolidayDB / World Data API、TimeAndDate、holidays.rest，不取其数据 |
| Nager.Date 使用边界 | 只保留比对报告；不入库、不分发；不使用其自托管包（需赞助获取 license key） |
| 版本粒度 | 每个（国家, 年份）一个内容哈希，存入清单；升级库时对哈希做 diff，看哪些块变了 |
| 快照 | 只用于测试与变更检测，不作为运行时数据源 |
| 语言 | 核心内部一律显式传 language，不依赖环境变量 |
| 更新流程 | 数据变更走 PR：夹具 + 清单 + 测试 + 变更日志同 PR 合入 |

数据不依赖 LLM 实时生成：模型只负责理解问题并调用工具，日期事实来自库与夹具。

## 里程碑与验收

*原文此处为里程碑图，未随 .docx 导出。*

流程沿用已定规则：设计 PR（ADR）先合入并标记 Accepted，再提交代码、测试与变更日志的实现 PR。各产品的验收标准见前几节；阶段不设时间估计，待你按可投入时间安排。

## 风险与待决问题

| 风险 | 影响 | 应对 |
|---|---|---|
| 库对 2027 年中国只按规则推算，且不提示 | 工作日数错误 | 年份白名单 + provisional 标注；官方通知发布后录入夹具 |
| 官方通知先于库更新：库文档写明中国数据每年需在年底前约三周复查，存在空窗期 | 一段时间内库与官方不一致 | 夹具比对失败时 CI 报警；补丁方式待决；同时向上游提 PR |
| 调休休息日靠名称模式识别（实测 zh_CN 名称形如「休息日（由 … 调休）」） | 库改名称格式后分类出错 | 内部固定用 zh_CN 判定，加回归测试，升级时对比哈希 |
| holidays 仍是 0.x 版本，文档称 language 的行为会在 v1 正式化 | 升级引入行为变化 | 固定版本；升级走 PR，对比各块哈希 |
| Nager.Date 的数据再分发条款与对中国 2025–2026 的覆盖均未核实 | 校验层不可用或有授权风险 | 只在 CI 拉取比对；先读许可文件，并查中国覆盖 |
| 两个社区数据源可能互相参考，一致不等于正确 | 校验形同虚设 | 以官方通知夹具为对错标准；Nager.Date 只用来发现分歧 |
| 差异化被通用 LLM、现有 Nager 封装与已有的中国调休 MCP 削弱 | 无人使用 | 聚焦调休正确、状态诚实标注、连休工具；以问题集实测 |
| 公共端点被滥用或无人发现 | 成本与零使用量 | 应用层限流，数据静态可强缓存；上架主流 MCP 目录 |

### 待决问题

- 部署形态与托管位置：容器化 Python 服务放在哪？官网与 MCP/API 是否同域（calendo.day），API 用子域名？
- 官方通知先于库更新时怎么补：用库的 update()/pop() 改节日、改 weekend_workdays 属性，还是等上游发版？
- 年份白名单：所有国家统一 2025–2027，还是按国家分别定义？
- HTTP 框架与 MCP SDK 选型（走 ADR）
- Nager.Date 的许可是否允许在 CI 中缓存其响应用于比对？
- disputed 块由谁、按什么依据裁决（官方通知之外的国家怎么办）？
- 服务端翻译层何时做：MVP 之后，还是客户端 LLM 翻译已足够？
