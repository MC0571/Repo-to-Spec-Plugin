# 当前实现与验证记录

> 核对日期：2026-09-29

## 插件包

- 可移植插件位于 `plugins/repo-to-spec/`，根清单使用 Agent Plugins 1.0.0 schema，并提供唯一的 `repo-to-spec` Skill。
- 仓库本地市场由 `.agents/plugins/marketplace.json` 注册插件。仓库检查验证清单、Skill frontmatter、市场路径及插件包内 Markdown 本地链接；该检查不判断自然语言规格的充分性。
- 本地另用 Agent Plugins 1.0.0 官方 JSON Schema 验证了 `plugin.json`，并用 Skill 格式快速校验器检查入口 frontmatter；这些检查没有改变插件运行依赖。
- 将插件目录单独复制到临时目录后，包内结构与全部本地 Markdown 链接检查仍通过（1 个 Skill、9 份 Markdown）；该试验不等于宿主加载。
- Codex CLI 加载试探报告插件尚未安装、Skill 不可用。插件未在当前 Codex 桌面宿主实际加载；格式符合性不能替代宿主加载验证。

## 真实仓库样例

[样例规格](../plugins/repo-to-spec/examples/skill-pack-validation/SYSTEM_SPEC/)从本地参考仓库的提交 `874eb414e6414dd6d399222a7e3925206dfdb585`，选择性恢复“本地 Agent Skill 包只读静态预检查”能力。用户范围、执行观察、作者自查、独立接收者反馈、修正和局限记录见[样例运行记录](examples/SKILL-PACK-VALIDATION-RUN.md)。

独立接收者不访问来源代码，只消费 `SYSTEM_SPEC/`，发现了引用识别、符号链接、重复统计及读取失败等具体设计缺口；修订后再次复查，确认可在已声明静态校验范围内独立实施与验收。作者自查与独立消费结论分别记录。使用缺失仓库材料和范围信息的输入测试后，Skill 保留阻塞并拒绝标记最终交付。

这是一个无图形界面的单项能力样例。它不证明插件已在宿主加载、不证明完整 Agent Skills 标准合规，也不能外推到其他产品类型或参考仓库。

## 仓库检查

CI 保留标准库实现的本地仓库检查，并验证插件/市场元数据、单一 Skill 入口和包内本地 Markdown 链接。自检覆盖有效包、损坏 frontmatter、不受支持的清单 schema、非法名称、多个 Skill 入口和越出插件包的相对引用。

以上检查只证明其定义的结构条件；样例语义和独立消费结果见运行记录，宿主加载仍未验证。
