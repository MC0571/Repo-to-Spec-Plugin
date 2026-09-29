# 当前实现与验证记录

> 核对日期：2026-09-29

## 插件包

- 可移植插件位于 `plugins/repo-to-spec/`，根清单使用 Agent Plugins 1.0.0 schema，并提供唯一的 `repo-to-spec` Skill。入口按实际问题加载专项方法，并以场景指导组合完整产品、UI、CLI/API、异步批量、SDK 与选择性吸收的调查起点。方法补充了请求结果、来源行为/声称、材料冲突、依赖必要性及停止状态的判断；输出标准提供可填写的规则、状态、接口、依赖表达和合成教学例。工具指南按证据问题给出操作及解释边界。
- 仓库本地市场由 `.agents/plugins/marketplace.json` 注册插件。包检查器用本地保存的 Agent Plugins 1.0.0 Schema 检查清单，解析 Skill 的 YAML frontmatter，并检查清单、Skill、资源和 Markdown 链接的真实路径没有越出插件包；它不判断自然语言规格的充分性。
- 包检查器使用隔离开发环境中的 PyYAML 与 jsonschema；分发插件没有这两项运行依赖。此前手写解析器的类型、合法引号/多行和符号链接反例已加入自检。
- Codex CLI `0.158.0-alpha.2.1` 已在临时用户目录实际安装 `0.1.0`，新会话读取安装缓存中的 Skill 和按需资源。早期加载与缺材料案例见[安装记录](examples/INSTALLED-PLUGIN-VALIDATION-RUN.md)；本轮修订后重新安装并运行较窄评分报告场景见[增强方法试跑](examples/METHOD-ENHANCEMENT-VALIDATION-RUN.md)。Codex 桌面端尚未实测。

## 真实仓库样例

[样例规格](../plugins/repo-to-spec/examples/skill-pack-validation/SYSTEM_SPEC/)从本地参考仓库的提交 `874eb414e6414dd6d399222a7e3925206dfdb585`，选择性恢复“本地 Agent Skill 包只读静态预检查”能力。用户范围、执行观察、作者自查、独立接收者反馈、修正和局限记录见[样例运行记录](examples/SKILL-PACK-VALIDATION-RUN.md)。

独立接收者不访问来源代码，只消费 `SYSTEM_SPEC/`，发现了引用识别、符号链接、重复统计及读取失败等具体设计缺口；修订后再次复查，确认可在已声明静态校验范围内独立实施与验收。作者自查与独立消费结论分别记录。使用缺失仓库材料和范围信息的输入测试后，Skill 保留阻塞并拒绝标记最终交付。

早期安装后新会话另产出[规格套件](examples/installed-cli-run/SYSTEM_SPEC/README.md)；独立接收者只读正式套件并复查修订。该会话发现把调查环境误升为目标运行依赖的问题，已修正样例并反馈到插件方法；那次修订**当时**没有再做完整新会话生成。后续本轮的不同范围试跑见下文。各次结果都不能外推到其他产品类型或参考仓库。

深化后的方法用同一真实仓库的“发布前 Skill 触发评测”能力做了[首次独立执行者试跑](examples/METHOD-DEPTH-VALIDATION-RUN.md)。本轮又以[已安装插件的新会话](examples/METHOD-ENHANCEMENT-VALIDATION-RUN.md)分别生成报告能力的完整局部规格与发布准入的部分草案；前者经来源核查和只读独立消费发现文本兼容缺口，保留原稿并修订复查。反馈到方法后重新安装、窄范围复跑 score，未重跑完整首例和缺输入对照。目标产品集成仍未验证。

## 仓库检查

CI 保留标准库实现的仓库检查；插件包检查另安装 `scripts/check-requirements.txt` 的固定版本开发依赖。自检覆盖合法引号/多行 YAML、错误类型与非法 YAML、清单字段类型、多个 Skill 入口、越界链接及指向包外的清单/Skill/资源符号链接。

以上检查只证明其定义的结构条件；样例语义、独立消费和宿主加载结果分别见运行记录。
