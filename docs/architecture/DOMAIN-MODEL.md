# 领域对象与语义关系

> 基线：DB-20260928 · 状态：已采纳 · 类型：目标设计
> 本文承接现有愿景，不表示能力已经实现；变更与采纳规则见文档入口。


## 1. 建模原则

对象用于表达交付责任，不以建立通用知识图谱为目标。正文中的英文是稳定代码标识；中文是首选术语。逻辑对象不要求各自有一张表、一个目录或一个独立文档。

区分两个“能力”：`ProductCapability` 是目标产品给用户的能力；`ToolCapability` 是插件完成工作时可调用的工具能力。二者不能使用同一字段含混表示。

## 2. 一等对象

| 对象 | 含义与最小信息 | 身份及拥有者 | 公开投影 |
| --- | --- | --- | --- |
| DeliveryScope | 目标版本、所选能力、环境、排除项、授权变更 | 范围 ID + 版本；交付编排持有 | 公开目标范围，不附源码定位 |
| ReferenceSnapshot | 输入仓库版本、脏工作树摘要、材料版本、观察环境 | 快照 ID；内部工作区持有 | 不进入实施包 |
| ProductCapability | 用户能完成什么、参与者与依赖 | 稳定产品 ID；产品设计持有 | 能力与组合规则 |
| DeliverySlice | 一项能力或工作流的交付任务、前置关系与验收 | 切片 ID；编排持有 | 不导出任务调度细节 |
| DesignElement | 规则、体验、数据、接口、逻辑设计或运行约束 | 元素 ID + 修订号；设计责任者持有 | 自包含规范元素 |
| SupportRecord | 对某结论的材料、观察或推导依据及限制 | 内部 ID；理解与设计持有 | 默认不导出；公开理由另行撰写 |
| OpenQuestion | 未知或矛盾、影响项、阻塞程度、下一步 | 问题 ID；产生者登记、编排分派 | 阻塞问题禁止混入最终包 |
| ImplementationFreedom | 可选实现轴、允许范围、不变结果及验收 | 自由项 ID；设计责任者持有 | 必须公开 |
| CoverageObligation | 范围内必须说明的维度、适用性与闭合依据 | 义务 ID；质量模块持有 | 可导出不含来源的覆盖摘要 |
| SpecArtifact | 承载元素的文件、格式、角色、版本和引用 | 产物 ID；规格组织持有 | 对应实际文件 |
| PackageRelease | 一次冻结的套件、清单、内容摘要、验收结果 | 套件 ID + 版本；导出器持有 | 发布包与公开清单 |
| ReviewFinding | 结构/语义/交接问题、严重性、影响与解决证据 | 问题 ID；审阅者持有 | 公开仅需交付相关摘要 |
| ToolCapability | 工作所需的操作语义与可用条件 | 能力键；能力适配持有 | 不成为下游依赖 |
| ProviderResult | 操作结果、实际范围、快照、限制及失败类型 | 调用 ID；能力适配持有 | 不直接进入实施包 |

## 3. 设计元素必须区分来源性质

`origin_kind` 取值为 `recovered`（已恢复事实）、`designed`（独立设计决策）、`user_authorized_change`（用户授权改动）。待验证推测不是一种最终规范来源；它通过 `status=draft` 与关联问题表示。

恢复事实关联材料或运行依据；独立设计关联所满足的规范、推导理由与被检查的不变量；授权改动关联用户决定及受影响范围版本。不能规定“每个设计元素都必须对应源码行”，否则必要的新逻辑设计无法成立；也不能让 `designed` 成为凭空发明目标产品规则的通道。

每个元素至少包含：身份、修订号、种类、规范性、所属能力、完整语义、适用条件、引用、状态、负责角色。内部还包含来源性质、依据与未决引用；公开投影不包含内部位置或符号映射。

## 4. 关系与约束

```text
DeliveryScope → selects → ProductCapability
DeliveryScope → pins → ReferenceSnapshot（仅内部）
DeliverySlice → delivers → DesignElement
DesignElement → satisfies → CoverageObligation
DesignElement → depends_on → DesignElement
SupportRecord → supports / contradicts → DesignElement
OpenQuestion / ReviewFinding → blocks → Element / Slice / Release
ImplementationFreedom → bounds_choices_for → DesignElement
SpecArtifact → contains → DesignElement
PackageRelease → freezes → SpecArtifact + ScopeVersion
```

身份不能用文件路径代替：文件移动不应使要求变成另一项要求。修订必须能区分语义改变与载体移动。公开 ID 与内部 ID 的映射保留在工作区；公开消费只需包内稳定 ID。

一个覆盖义务可由多个元素联合满足，一个元素也可支持多个义务。关系存在不代表语义已经完备，必须保留审阅状态。

## 5. 生命周期

设计元素：`draft → reviewed → accepted`；修改内容使当前修订回到 `draft`；旧修订可 `superseded`。这里 `accepted` 指当前任务的设计审阅接受，不代表已证明所有未来实现等价。

交付切片：`planned → active → review → closed`，过程中可 `blocked`；依据失效、共享约束变化或审阅发现缺口时从 `closed` 转为 `reopened`。切片关闭不等于整个产品已完成。

交付包：`draft → candidate → ready → exported`。`ready` 的前提由交付门决定，不允许直接从 `draft` 到 `exported`。新的源版本或范围变化产生新候选；既有发布快照不能被静默改写。

问题：`open → investigating → resolved` 或 `accepted_out_of_scope`。后一状态必须有明确范围决策，并不适用于范围内重要未决问题。文档状态、运行状态、产品能力成熟度分别维护，不能混用一个 done。

## 6. 两种视图而非两套产品语义

内部视图包含来源、工具限制和工作状态；公开视图包含完整设计、实现自由与验收。两者共享同一设计元素的内容版本，导出只做受控投影，不维护容易分叉的第二套产品规则。

对象序列化和兼容策略见 [状态模型](STATE-AND-PROVENANCE.md)；字段的强制约束见 [工作状态契约](../../contracts/workflow-and-state.md)。具体磁盘文件结构属于待评审实现选择，不在领域模型中固定。
