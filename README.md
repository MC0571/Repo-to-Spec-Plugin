# Repo-to-Spec Plugin

[English](./README_EN.md)

> 从已有代码仓库恢复一套可验证、可追溯、与具体实现解耦的 Canonical Spec，使独立实现者能够在不依赖原始实现细节的前提下重建系统，并依据 Spec 验收结果。

## 项目定位

Repo-to-Spec 面向已有代码仓库的逆向规格化。

它关注的不是“代码是怎么写的”，而是从源码、测试、配置、接口定义和可观察行为中恢复：

- 系统对外提供什么能力；
- 输入、输出和错误如何定义；
- 配置、状态和生命周期如何工作；
- 文件系统、持久化、网络等副作用是什么；
- 顺序、优先级、fallback、兼容性和安全边界如何约束行为；
- 哪些行为已被证据确认，哪些仍存在歧义或缺口。

最终产物应足以支持独立实现，而不要求复制参考仓库的内部结构。

## 核心原则

### Evidence-grounded

进入 Canonical Spec 的重要要求应尽可能追溯到可复核证据。

调查过程中需要区分：

- 已确认行为；
- 有一致证据支持的推断；
- 尚未确认的假设；
- 未覆盖区域；
- 相互冲突的证据。

无法确认的行为应保持显式不确定，而不是由分析者自行补全。

### Observable behavior first

优先规范外部可观察契约，例如：

- CLI、API 与协议表面；
- 配置和环境变量；
- 输入、输出、错误与退出行为；
- 状态转换与生命周期；
- 文件系统、持久化和网络副作用；
- ordering、precedence 与 fallback；
- compatibility 与 security boundaries；
- determinism、idempotency 等可观察约束。

### Implementation-independent

Canonical Spec 描述“必须成立什么”，而不是“必须怎样实现”。

除非某项实现细节本身属于兼容契约，否则不应把以下内容固化为规格要求：

- 原仓库目录结构；
- 内部类名或函数名；
- 私有数据结构；
- 偶然的模块边界；
- 可替换的算法细节；
- 非必要的技术选型。

### Coverage and closure

规格完整性不能只由文档长度判断。

调查需要持续识别：

- 已覆盖的行为面；
- 尚未调查的区域；
- 未解决的歧义；
- 相互矛盾的证据；
- 独立实现仍然缺失的信息。

只有在关键行为和约束达到足够闭合后，Spec 才能作为可靠的实现契约。

### Spec is normative

Canonical Spec 是行为与约束的规范性来源。

实现可以采用不同的内部设计，只要最终可观察行为满足同一份 Spec。

## 工作模型

```text
Reference Repository
        ↓
Repository Investigation
        ↓
Evidence + Coverage
        ↓
Canonical Spec
        ↓
Spec Validation
        ↓
Conformance Evidence
```

其中：

- **Repository Investigation**：定位和验证与行为相关的源码、测试、配置和运行证据；
- **Evidence + Coverage**：记录证据来源、置信度、覆盖范围和未决项；
- **Canonical Spec**：整理实现无关的行为、接口、约束和边界；
- **Spec Validation**：检查完整性、明确性、一致性、可验证性和实现独立性；
- **Conformance Evidence**：为后续实现验收提供可复核依据。

## 边界

Repo-to-Spec 不以以下事项为目标：

- 复制参考仓库的内部架构；
- 把代码结构直接改写成文档；
- 为独立实现预先指定目录、模块或算法；
- 用未经验证的假设填补规格空白；
- 把实现计划或任务分解当作 Canonical Spec 的一部分。

## 贡献

开始贡献前请阅读：

- [CONTRIBUTING.md](./CONTRIBUTING.md)：仓库开发流程与质量要求；
- [AGENTS.md](./AGENTS.md)：Coding Agent 在本仓库中的执行约束。

## License

仓库当前未包含 LICENSE 文件。在许可证明确之前，请不要假定存在默认的开源授权条款。
