# 依据与参考资料

## 当前仓库：本次判断的首要依据

本次读取的默认分支提交为 `adb63ae16dd79e3c3d4907fe33570ebe00a3389b`，提交时间为 2026-09-27 23:11:13（UTC+08:00）。全部九个文件均按该固定快照核对，文件内容的 Git blob 摘要与树摘要已在本地校验一致。

| 资料 | 用途 |
| --- | --- |
| [固定提交](https://github.com/MC0571/Repo-to-Spec-Plugin/commit/adb63ae16dd79e3c3d4907fe33570ebe00a3389b) | 本次基准与变更范围 |
| [README](https://github.com/MC0571/Repo-to-Spec-Plugin/blob/adb63ae16dd79e3c3d4907fe33570ebe00a3389b/README.md) | 公开定位与交付边界 |
| [VISION](https://github.com/MC0571/Repo-to-Spec-Plugin/blob/adb63ae16dd79e3c3d4907fe33570ebe00a3389b/VISION.md) | 产品、体验、技术设计、独立交接、渐进披露与路径原则 |
| [AGENTS](https://github.com/MC0571/Repo-to-Spec-Plugin/blob/adb63ae16dd79e3c3d4907fe33570ebe00a3389b/AGENTS.md) | Agent 硬约束与真实命令 |
| [CONTRIBUTING](https://github.com/MC0571/Repo-to-Spec-Plugin/blob/adb63ae16dd79e3c3d4907fe33570ebe00a3389b/CONTRIBUTING.md) | 格式标准、贡献与文档治理 |
| [CI](https://github.com/MC0571/Repo-to-Spec-Plugin/blob/adb63ae16dd79e3c3d4907fe33570ebe00a3389b/.github/workflows/ci.yml) | 当前自动检查入口 |
| [检查脚本](https://github.com/MC0571/Repo-to-Spec-Plugin/blob/adb63ae16dd79e3c3d4907fe33570ebe00a3389b/scripts/ci_check.py) | 当前检查的实际范围与局限 |

## 外部标准：沿用仓库已经选择的路线

2026-09-28 核对 [Agent Plugins specification](https://agent-plugins.org/specification)：页面声明版本 1.0.0，状态 Working Draft。根清单、技能发现位置及客户端扩展模型按所声明版本处理；支持标准不自动意味着某客户端已经加载成功。

同日核对 [Agent Skills specification](https://agentskills.io/specification)：用于技能目录、SKILL.md 和 frontmatter 规则。正式实现时应记录实际声明的标准与客户端版本并验证，不把这个核对日期视为永久兼容保证。

## 已有讨论与研究：作为设计参考而非当前实现事实

此前提供的《深入调研 reverse skill》使用 `zhaoxuya520/reverse-skill` 的历史源码快照 `cab634bd855fc287f6e420c1f36fd1a6b9245960`。本次只借鉴其中的契约驱动、渐进披露、状态恢复和回归构建方法；没有重新审计该项目当前 main，也没有复制其源代码或安全领域流程。

此前关于 Spec Kit 的讨论仅用于理解下游规格消费、计划与实现的区分；本设计没有把 Spec Kit 集成设为依赖，也不使用其某个模板替代现有 VISION 的完整设计交付。

## 事实与提案的区分

CURRENT-STATE 与此处固定链接记录来源事实；ARCHITECTURE、ROADMAP、contracts 与 ADR 的机制原作为设计提案提出，采纳范围见 [M0 维护者记录](reviews/M0-ADOPTION.md)。新的对象划分、工作包、验收编号和存储建议不是现有源码已经实现的事实；未采纳的工程选择仍须按开放决策验证。
