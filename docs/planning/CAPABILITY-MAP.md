# 完整能力地图

> 基线：DB-20260928 · 状态：已采纳 · 类型：能力规划
> 本文承接现有愿景，不表示能力已经实现；变更与采纳规则见文档入口。


## 范围与状态

本地图覆盖愿景所需的目标能力，不把“增加更多工具”作为产品能力。S1—S6 的职责见 [目标架构](../../ARCHITECTURE.md)。下表给出稳定导航；**状态与依赖以 [设计登记表](design-baseline.json) 为准**，不在本文件维护第二套完成状态。

| 能力 | 目标 | 职责区 | 目标退出阶段 | 详细设计 | 验收 |
| --- | --- | --- | --- | --- | --- |
| C01 | 目标范围与输入条件 | S1 | M1 | [定义](../../docs/product/PRODUCT-DELIVERY.md) | A01 |
| C02 | 产品面发现与子系统分解 | S2 | M2 | [定义](../../docs/product/PRODUCT-DELIVERY.md) | A02 |
| C03 | 产品规则与工作流恢复 | S2 | M2 | [定义](../../docs/architecture/EXECUTION-PROTOCOL.md) | A03 |
| C04 | 完整体验恢复与设计 | S2 | M2 | [定义](../../docs/product/PRODUCT-DELIVERY.md) | A04 |
| C05 | 独立逻辑技术设计 | S2 | M2 | [定义](../../docs/architecture/DOMAIN-MODEL.md) | A05 |
| C06 | 接口、数据与运行契约 | S2 | M2 | [定义](../../docs/architecture/SYSTEM-SPEC.md) | A06 |
| C07 | 选择性吸收与依赖闭合 | S1 | M3 | [定义](../../docs/product/PRODUCT-DELIVERY.md) | A07 |
| C08 | 进度持久化与恢复 | S4 | M1 | [定义](../../docs/architecture/STATE-AND-PROVENANCE.md) | A08 |
| C09 | 内部依据与来源性质 | S4 | M1 | [定义](../../docs/architecture/DOMAIN-MODEL.md) | A09 |
| C10 | 覆盖驱动与缺口闭合 | S6 | M2 | [定义](../../docs/architecture/COVERAGE-AND-QUALITY.md) | A10 |
| C11 | 多格式规格组织 | S5 | M4 | [定义](../../docs/architecture/SYSTEM-SPEC.md) | A11 |
| C12 | 隔离交接与发布 | S5 | M4 | [定义](../../docs/architecture/SECURITY-AND-HANDOFF.md) | A12 |
| C13 | 原生能力与可选增强 | S3 | M1 | [定义](../../docs/architecture/PROVIDER-MODEL.md) | A13 |
| C14 | 可移植插件与宿主适配 | S3 | M5 | [定义](../../docs/architecture/PLUGIN-AND-SKILLS.md) | A14 |
| C15 | 版本影响与按需更新 | S4 | M5 | [定义](../../docs/architecture/STATE-AND-PROVENANCE.md) | A15 |
| C16 | 交付质量门 | S6 | M4 | [定义](../../docs/architecture/COVERAGE-AND-QUALITY.md) | A16 |
| C17 | 独立消费与结果评测 | S6 | M6 | [定义](../../docs/architecture/CONFORMANCE-MODEL.md) | A17 |
| C18 | 失败归因与经验回归 | S6 | M6 | [定义](../../docs/planning/VALIDATION-STRATEGY.md) | A18 |
| C19 | 权限与输入数据边界 | S3 | M1 | [定义](../../docs/architecture/SECURITY-AND-HANDOFF.md) | A19 |
| C20 | 整体成本与可用性 | S1 | M6 | [定义](../../docs/planning/VALIDATION-STRATEGY.md) | A20 |

阶段表示目标能力何时需要完整满足退出条件，不限制提前实验或并行建设。C18 的回归从第一项可执行行为开始，M6 表示全产品失败闭环的完成标准，不是到 M6 才写测试。

## 四条独立成熟度轴

`design_status`：proposed / accepted / superseded；`implementation_status`：not_implemented / partial / implemented；`verification_status`：not_run / partial / passed / failed；`regression_status`：not_established / partial / protected。

状态提升必须附上可定位的实现、测试或评审证据。现在的文档检查器只能证明登记表与文件没有特定结构错误，不会将任何产品能力自动标为 passed。单个已运行的正向样例也不能将整个能力标为 protected。

## 登记表合同

根字段记录登记表版本、基线身份、源提交、职责区、能力、里程碑和验收检查。能力必须关联定义文件、愿景章节、依赖、目标阶段、合同和验收；引用不得悬空；目标依赖不得成环。反馈关系不是硬前置，不能为了画闭环把依赖图写成循环。

里程碑完成要求退出检查已通过并有证据；被引用能力的设计、实现、验证和回归也必须达到声明要求。M0 是设计接受门，不由文件数量自动完成。

变更权威内容时先更新相应文档和合同，再同步登记表关联；该表不是用来偷偷创造新的产品承诺。机器检查只检查结构与状态一致性，不判断愿景章节引用是否语义恰当，后者仍需评审。
