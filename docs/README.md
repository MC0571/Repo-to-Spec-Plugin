# 文档与验证入口

## 当前有效材料

| 需要了解 | 位置 |
| --- | --- |
| 当前插件与样例验证结果、限制 | [CURRENT-STATE.md](CURRENT-STATE.md) |
| 产品目标、完整规格边界与长期原则 | [VISION.md](../VISION.md) |
| 当前 Skill-led 执行边界 | [ARCHITECTURE.md](../ARCHITECTURE.md) |
| 可安装插件及统一 Skill | [插件清单](../plugins/repo-to-spec/plugin.json)、[Skill 入口](../plugins/repo-to-spec/skills/repo-to-spec/SKILL.md) |
| 按需逆向方法、工具使用、规格标准与审查清单 | Skill 入口引用的 `plugins/repo-to-spec/skills/repo-to-spec/references/` 与 `assets/` |
| 仓库贡献、标准格式与质量检查要求 | [CONTRIBUTING.md](../CONTRIBUTING.md)、[AGENTS.md](../AGENTS.md) |
| 仓库结构检查和插件包检查 | `python3 scripts/ci_check.py`；插件包检查的隔离环境命令见 [AGENTS.md](../AGENTS.md) |

插件包检查验证完整 manifest Schema、Skill YAML 字段、包内真实路径、仓库本地市场及 Markdown 本地引用。结构格式检查不证明宿主加载或规格语义完整；两者分别进行实际验证。

真实仓库样例及结论见[包内样例规格](../plugins/repo-to-spec/examples/skill-pack-validation/SYSTEM_SPEC/)和[首次运行记录](examples/SKILL-PACK-VALIDATION-RUN.md)；Codex CLI 实际安装后的[新会话规格](examples/installed-cli-run/SYSTEM_SPEC/README.md)与[运行记录](examples/INSTALLED-PLUGIN-VALIDATION-RUN.md)另行保存。作者自查与独立接收者检查分别记录。目前仅验证了一个选择性吸收的无图形界面能力；桌面宿主与其他产品类型仍未验证。

## 历史设计档案

`docs/architecture/`、`docs/product/`、`docs/planning/`、`docs/decisions/`、`docs/reviews/` 与 `contracts/` 中带有 `DB-20260928` 的材料记录了此前的设计基线。基线中的 S1–S6 分区、Cxx 能力、M0–M6 阶段、Axx 验收、B-* 评测集、Provider 生命周期及持久化状态模型现已过时；保留它们是为追溯设计过程，不构成当前插件必须实现的模块、服务或流程。

仍有效的产品判断已归纳到当前 `VISION.md`、`ARCHITECTURE.md` 和插件 Skill：忠实恢复声明范围、同时设计产品体验和必要逻辑技术、处理选择性吸收的传递依赖、标注事实/推导/批准改动/未知、保持正式套件自包含、按实际宿主能力使用工具，以及区分结构检查、作者自查和独立消费检查。安全、隐私、授权和贡献约束以当前 [AGENTS.md](../AGENTS.md) 与 [CONTRIBUTING.md](../CONTRIBUTING.md) 为准。

[M0-ADOPTION.md](reviews/M0-ADOPTION.md) 记录旧基线曾获采纳；原 [设计登记表](planning/design-baseline.json) 的顶层状态现为 `superseded`。[能力地图](planning/CAPABILITY-MAP.md)、[验证策略](planning/VALIDATION-STRATEGY.md) 和 ADR 仅供历史回顾，不再控制开发步骤或产品验收。旧文件内的“已采纳”指当时状态，不表示其机制仍是当前实现要求。
