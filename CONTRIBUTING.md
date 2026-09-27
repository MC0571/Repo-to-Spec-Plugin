# Contributing

感谢对 Repo-to-Spec Plugin 的贡献。

本文件定义所有贡献者共同遵守的仓库开发流程与质量要求。Coding Agent 还必须同时遵守 [AGENTS.md](./AGENTS.md)。

## 1. 基本原则

所有改动应满足：

- 与当前任务或 Issue 直接相关；
- 尽量保持改动小而完整；
- 不把无关重构混入功能修改；
- 新行为应有可验证依据；
- 行为变化应同步更新测试和文档；
- 不为尚未确认的需求提前引入复杂依赖或抽象；
- 核心行为不得依赖未声明的外部环境才能成立。

## 2. 分支策略

`main` 是主分支，日常开发通过任务分支和 Pull Request 集成。

除明确的仓库管理操作外：

1. 从最新 `main` 创建任务分支；
2. 在任务分支完成实现和验证；
3. 通过 Pull Request 合入 `main`；
4. 不直接向 `main` 推送功能性修改；
5. 不进行与当前任务无关的 force-push 或 history rewrite。

分支名称采用：

```text
feat/<short-name>
fix/<short-name>
docs/<short-name>
refactor/<short-name>
test/<short-name>
chore/<short-name>
```

仓库初始化操作可使用 `init` 分支。

## 3. Pull Request 与合并

仓库执行以下合并约定：

- `main` 通过分支保护或等价规则保护；
- 变更通过 PR 进入 `main`；
- 仅使用 Squash Merge；
- Contributor 或 Agent 不得绕过 branch protection、required checks 或 review gate。

PR 应保持单一目的，标题应直接说明改动。

commit / PR 标题采用 Conventional Commits 风格：

```text
feat: add evidence model
fix: handle missing repository metadata
docs: clarify specification boundaries
refactor: isolate investigation capability
test: cover configuration precedence
chore: update repository metadata
```

由于主分支使用 squash merge，中间 commit 可以服务开发过程，但应避免无意义噪声。

## 4. 开发前检查

开始修改前：

1. 阅读本文件；
2. Coding Agent 额外阅读 `AGENTS.md`；
3. 确认当前分支不是受保护的 `main`；
4. 阅读与改动区域相邻的文档、测试和配置；
5. 从 manifest、脚本和 CI 确认真实的 lint、typecheck、test、build 入口；
6. 不要因为个人偏好引入与现有工具链重复的工具。

如果仓库尚未定义语言或构建系统，不要自行补一套“默认”技术栈。

## 5. 代码与设计要求

### 保持职责边界

本项目区分：

- Repository Investigation；
- Evidence；
- Coverage；
- Canonical Spec；
- Spec Validation；
- Conformance。

实现时应保持这些职责可识别、可验证，避免把调查、推断、规范和实现决策混在同一不可检查流程里。

### Evidence over assumption

影响规格的行为必须优先由源码、测试、配置、schema、运行结果或其他明确证据支持。

不要因为某种行为“通常如此”就把它写成项目要求。

### Implementation independence

Canonical Spec 应描述必须成立的行为和约束，而不是复制参考实现。

除非本身属于兼容契约，否则不要把原仓库的目录、内部符号、私有数据结构、偶然模块边界或可替换算法写成规范要求。

### 插件与技能格式

提供可安装插件时，遵循 [Agent Plugins 规范](https://agent-plugins.org/specification)：在插件根目录提供 `plugin.json`，设置必需的 `$schema` 和 `name`；技能放在 `skills/<skill-name>/SKILL.md`，MCP 服务配置放在根目录的 `mcp.json`（仅在提供服务时需要）。客户端专有内容使用规范定义的扩展机制，不替代可移植格式。

每个技能遵循 [Agent Skills 规范](https://agentskills.io/specification)：`SKILL.md` 包含 YAML frontmatter 和正文，至少声明与目录名一致的 `name`，以及说明能力和适用场景的 `description`。

新增或修改插件、技能时，按所声明版本的规范验证实际包结构和元数据；如声称支持某个客户端，还需验证该客户端能加载。尚未提供的组件无需创建占位文件。

## 6. 测试要求

任何可执行代码进入仓库后，改动应根据影响范围运行仓库实际定义的验证，例如：

- unit tests；
- integration tests；
- lint；
- typecheck；
- build；
- schema / fixture validation；
- conformance tests。

新增或修复行为时，应补充能够证明该行为的测试。

如果某项验证无法运行，PR 中说明：

- 未运行的检查；
- 原因；
- 风险；
- 替代验证证据。

不要在没有说明的情况下用“没有测试”接受行为性变更。

## 7. 文档要求

以下变化通常需要同步更新文档：

- 用户可观察行为；
- CLI / API / config contract；
- Spec schema；
- Evidence / Coverage 语义；
- 安装或运行方式；
- 开发流程；
- breaking change。

README 描述稳定的项目定位、边界和公开使用方式；详细实现设计进入专门文档。

## 8. 安全与敏感信息

禁止提交：

- API key；
- access token；
- 私钥；
- 密码；
- 未脱敏的用户数据；
- 本地 `.env`；
- 其他秘密或凭证。

如果发现凭证曾进入 Git 历史，不要只删除文件；应停止继续传播，并按对应平台流程旋转凭证与清理历史。

## 9. Pull Request 检查清单

提交 PR 前确认：

- [ ] 改动范围与 PR 目标一致；
- [ ] 没有无关格式化或重构；
- [ ] 新行为具有测试或可复核证据；
- [ ] 适用的 test / lint / typecheck / build 已通过；
- [ ] 文档已同步；
- [ ] 没有提交秘密、生成物或本地环境文件；
- [ ] Canonical Spec 与实现细节的边界保持清晰；
- [ ] PR 可以通过 squash merge 形成一个清晰的主分支 commit。

## 10. Agent 贡献

Coding Agent 的仓库级硬约束见 [AGENTS.md](./AGENTS.md)。

当本文件与 Agent 自身默认行为冲突时，以本仓库明确写出的贡献流程为准。
