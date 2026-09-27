# 设计文档入口

> 基线：DB-20260928 · 状态：待评审提案 · 类型：设计治理
> 本文承接现有愿景，不表示能力已经实现；变更与采纳规则见文档入口。


## 这套文件是什么

这是一套面向完整愿景的目标设计与建设路径提案。它补齐愿景与实现之间的设计层，不把项目改成阶段性摘要生成器，也不宣称插件已经可安装。

阅读次序是：现有 [愿景](../VISION.md) → [目标架构](../ARCHITECTURE.md) → [建设路径](../ROADMAP.md)。审阅本次调整先看 [现状评估](reviews/BASELINE-REVIEW.md)。具体任务按下表进入，不要求每次加载全部文档。

| 需要回答的问题 | 权威位置 |
| --- | --- |
| 为什么存在、承诺什么 | [VISION.md](../VISION.md)，保持现有正文不变 |
| 当前代码实际具备什么 | [CURRENT-STATE.md](CURRENT-STATE.md)，固定提交的事实快照 |
| 完整系统如何分工 | [ARCHITECTURE.md](../ARCHITECTURE.md) |
| 交付哪些产品、体验与技术内容 | [PRODUCT-DELIVERY.md](product/PRODUCT-DELIVERY.md) |
| 使用哪些对象、术语与关系 | [DOMAIN-MODEL.md](architecture/DOMAIN-MODEL.md) |
| Agent 如何工作、何时停下或继续 | [EXECUTION-PROTOCOL.md](architecture/EXECUTION-PROTOCOL.md) |
| 工作状态、内部依据、版本如何保存 | [STATE-AND-PROVENANCE.md](architecture/STATE-AND-PROVENANCE.md) |
| 套件如何组织与表达 | [SYSTEM-SPEC.md](architecture/SYSTEM-SPEC.md) |
| 如何判断已足够、仍有何缺口 | [COVERAGE-AND-QUALITY.md](architecture/COVERAGE-AND-QUALITY.md) |
| 如何利用原生能力和外部工具 | [PROVIDER-MODEL.md](architecture/PROVIDER-MODEL.md) |
| 如何分发插件、组织技能、适配宿主 | [PLUGIN-AND-SKILLS.md](architecture/PLUGIN-AND-SKILLS.md) |
| 如何隔离参考材料与开发交接 | [SECURITY-AND-HANDOFF.md](architecture/SECURITY-AND-HANDOFF.md) |
| 如何进行独立消费和符合性验证 | [CONFORMANCE-MODEL.md](architecture/CONFORMANCE-MODEL.md) |
| 每个机制必须满足什么 | [契约目录](../contracts/README.md) |
| 怎样走向完整愿景 | [ROADMAP.md](../ROADMAP.md)、[能力地图](planning/CAPABILITY-MAP.md) |
| 依赖、状态和验收关联如何维护 | [设计登记表](planning/design-baseline.json) |
| 怎样评测与避免退化 | [VALIDATION-STRATEGY.md](planning/VALIDATION-STRATEGY.md) |
| 哪些决策尚需证据、谁来决定 | [OPEN-DECISIONS.md](decisions/OPEN-DECISIONS.md) |
| 为什么选择这条路线 | [ADR 索引](decisions/README.md) |
| 怎样拆成可执行工作 | [WORK-PACKAGES.md](planning/WORK-PACKAGES.md) |

## 权威与状态

现有 `VISION.md`、`README.md`、`AGENTS.md`、`CONTRIBUTING.md` 是读取到的仓库基础。新增设计的状态是**待评审提案**；讨论中曾出现的“六个平面”“规格编译器”“文件化状态”等，不自动等于已批准实现。

文件状态采用 `proposed / accepted / superseded`。只有维护者明确接受、并在 PR 或决策记录中留下依据后，才能标记 `accepted`；合入草案不自动意味着接受所有设计选择。能力是否实现、是否验证、是否具有回归保护，另行记录，不能从文档状态推导。

冲突处理不是简单“更底层或更严格的文件自动获胜”。目标设计不得静默修改愿景；契约不得静默推翻已接受设计；实现与契约不一致必须作为缺陷或正式变更处理。发现冲突时记录影响，停止受影响的发布判断，通过修订对应权威文件解决。

## 单一事实来源

领域概念的定义只在领域模型维护；可执行约束只在契约维护；能力、里程碑状态及其关联只在 `design-baseline.json` 维护。架构和路线图引用这些内容，不复制第二份状态表。

`SYSTEM_SPEC/` 是 Repo-to-Spec 将来生成的**目标产品交付物**，不是本仓库设计文档的根目录。`docs/` 描述 Repo-to-Spec 自己；两种规格不可混淆。内部来源追踪也不属于下游实施包。

## 本次附带的可执行能力

新增 `scripts/check_design.py` 只校验本设计包的文件、登记表引用、依赖环、状态证据及契约关联；它不是 Repo-to-Spec 的规格生成器或产品完备性证明器。使用方法与限制见 [验证策略](planning/VALIDATION-STRATEGY.md)。

没有为了填满目录而新增 `plugin.json`、`SKILL.md` 或 MCP 服务。真正实现并验证组件后再提供这些可执行入口。
