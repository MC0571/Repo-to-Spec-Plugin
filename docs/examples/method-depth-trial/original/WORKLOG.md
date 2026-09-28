# 工作记录

## 结果与状态

- 原始候选输出：`/tmp/repo-to-spec-method-trial.oPIcry/SYSTEM_SPEC/README.md`
- 候选状态：草案；四项阻塞列在规格末尾。没有目标产品 Skill 包、目标发布流程代码或本地选择器可供集成和实测。
- 本工作只定义“发布前、本地评估 Skill 触发选择”的能力。未扩展到内容蒸馏、编译、更新、实际 Skill 任务输出或发布实现。

## 参考版本与环境

- 参考仓库：`/Volumes/2T/dev/reference/cangjie-skill`
- 开始时 `git rev-parse --show-toplevel` 为该仓库，`git describe --tags --always --dirty` 返回 `874eb41`；`git status --short --branch` 显示 `main...origin/main` 且无工作区改动。
- `SKILL.md` frontmatter 标记 `cangjie.version: 2.5.0`；`git tag --points-at HEAD` 无输出，因此本记录用 metadata 版本和 commit SHA 共同识别，不声称有发行标签。
- 当前调查机 `python3 --version` 为 3.12.13。它只记录本次运行条件，不是目标系统的语言或运行时要求。
- CodeGraph 目录不存在；按仓库指引使用本地文件读取和 `rg`。

## 实际读取材料

### Repo-to-Spec 方法

开始前读取本仓库 `CONTRIBUTING.md` 和唯一入口 `plugins/repo-to-spec/skills/repo-to-spec/SKILL.md`。本任务按入口加载了：

- `references/investigation.md`：版本、范围、证据性质、从入口追踪用户结果。
- `references/capabilities.md`：所选能力的入口、相邻能力纳入/排除及共享规则。
- `references/absorption.md`：传递依赖、目标环境提供者与验收契约。
- `references/behavior.md`：超时、取消、部分结果和恢复状态。
- `references/contracts.md`：本地套件、执行器、报告和发布消费者的边界契约。
- `references/decoupling.md`：保留选择结果约束，避免继承来源语言、脚本或目录结构。
- `references/tools.md`：只用本地只读检索和在临时目录内受控执行。
- `references/specification.md`、`assets/spec-outline.md`：自包含套件内容、规则、依赖和验收场景。
- `references/review.md`：分别报告来源核对与独立消费；本次没有把作者自检称为独立消费审查。

### 参考产品材料

- `CONTRIBUTING.md`：读取仓库本地操作边界和本地验证说明。
- `SKILL.md`：读取产品范围、2.5.0 流程和触发/输出压力测试的入口。
- `methodology/06-stage4-pressure-test.md`：读取触发评测分类、盲测原则、交叉 Skill 混淆、验收和保留用例要求。没有读取 Stage 5 的内容蒸馏交付流程。
- `schemas/eval-suite.schema.json`：读取 trigger suite 字段及其与 `edge_case` 的表达。
- `scripts/run_trigger_evals.py`：读取 `split`、`prepare`、`score` 实际调用路径。
- `scripts/cangjie_common.py`：只核对 JSON 读写依赖；未把其余通用工具当作本次能力材料。

未读取被用户排除的示例目录、已有评测用例/结果或旧验证记录；未调用网络、外部服务，未安装依赖，未向外上传材料，未修改参考仓库。

## 操作和验证

1. 核对参考仓库根目录、HEAD、工作区状态、tag 和版本标记。开始与结束均未修改仓库文件。
2. 用 `rg --files` 查找触发评测方法、Schema 和 runner；检索时排除示例目录。随后只读取以上列出的源材料。
3. 检查 runner 依赖后，在操作系统临时目录创建**合成**套件并执行来源 runner 的 `split`、`prepare`、`score`。没有使用真实 Skill 内容、真实用户请求或现有样例答案。
   - 首次探针用了 runner 默认 train split；脚本三个子命令均返回 0，但外层检查器误以为随机 train 集必含指定用例，读取不存在的任务文件后退出。该错误来自探针断言，不是来源命令失败。
   - 更正后的探针使用 `--set all`，5 个准备任务全部生成。准备包字段为 `case_id`、`runs`、`prompt`、`instruction`、`installed_skills`，不含 suite 的 `expected` 或 `notes`；`installed_skills` 只传入 Skill slug 列表。
   - 计分探针提交 4/5 个计划用例结果：漏掉一个正例，且竞争 Skill 用例选错 Skill。来源 runner 仍输出 `TP 1 / FP 0 / FN 0 / TN 3`、precision/recall/F1 均 `1.000`、兄弟混淆率 `0/1`，退出 0。逐例表写出“未中兄弟”，但计分不把该错路由计为失败。此探针证明了本规格中“不完整或错路由不得放行”的要求有现实依据。
4. 没有运行本仓库全量 CI/插件包检查：改动仅在独立 `/tmp` 交付目录，且该仓库检查不验证目标产品的触发选择或发布集成。没有目标产品或授权选择器，未能运行目标环境模型/宿主测试，也没有声称实测成功。

## 重要结论的性质

### 已验证事实

- 来源方法把触发精度与触发后的任务输出区分；本范围只采纳前者。方法要求正例、负例、边界、相邻 Skill 混淆用例，盲测时隐藏预期，并保留未参与调优的用例。
- `run_trigger_evals.py` 提供确定性 split、盲测任务准备和结果计分；代码注释明确 runner 不替宿主运行模型。
- runner 的 `prepare` 只接收 Skill slug 清单并准备 prompt 包，不调用选择器，也不传完整候选 Skill 内容或描述。
- runner 对输入结果逐行计分，未发现本次缺失结果；错选兄弟 Skill 虽显示“未中兄弟”，仍进入 TN，未计入失败。Schema 没规定覆盖数量、评分阈值或必须完整提交结果。来源 runner 的结果模型是单个 Skill 或 `none`，目标宿主的选择基数未确认。
- Schema 将 `edge_case` 作为预期类别，runner 计分时无条件把 `edge_case` 算作“不触发”。这无法表达预期本应触发目标的边界用例。
- 来源方法与 runner/Schema 未形成可直接作为发布门禁的完整产品接口：方法要求宿主或独立 Agent 进行盲测，runner 只准备/计分，没有模型调用和发布流程 gate。

### 推导设计

- 若目标结果是检验实际 Skill 是否被触发，执行器须走目标产品发布后使用的同一 Skill 选择路径，输入实际候选元数据与竞争 Skill 环境。仅传 Skill 名称不足以证明真实触发效果。依据是触发行为取决于候选描述/选择上下文，而来源方法本身要求提供可竞争的 Skill 名称与描述。
- 用例类别与预期路由分离，边界用例直接声明目标 Skill / 竞争 Skill / `none` 的预期，解决来源 Schema 和计分代码的表达冲突。
- 评测应绑定实际发布的候选快照；不完整、错误或摘要不匹配的评测结果不能放行。否则检查的版本可能不是发布版本，或漏测被指标掩盖。此为目标用户结果要求，不是来源 runner 的已验证能力。
- 测试仅观察 Skill 选择，不执行被选 Skill 的任务；套件、候选包和报告保存在本地。若目标选择器按既有授权调用远端模型，只允许使用该授权路径；本能力不另行上传材料或回退使用未授权服务。

### 未决与阻塞

1. 目标产品是否具有可本地调用、能返回所选 Skill ID 的宿主/选择器接口；所用模型与 Skill 上下文如何提供。
2. 目标发布流程可否提供稳定待发布快照、内容摘要和前置门禁消费点；目前无法确认评测同发布一致。
3. 各类别的最小用例数、重复次数、通过阈值和保留集负责人。来源仅给覆盖建议、重复默认和部分零容错要求，没有目标产品已批准的完整门槛。
4. 实际 Skill 包格式、触发环境中的竞争 Skill 集合、单选/多选语义、宿主/模型版本管理及本地/远端数据授权政策未给出。

因此候选标为草案。已完成的自检不等于独立消费审查；目标环境也未实际运行。

## 本次使用的专项方法

使用 `repo-to-spec` 的调查与写作循环，并按缺口应用能力边界、选择性吸收/依赖闭合、行为与异常恢复、数据接口和必要技术约束、实现解耦、输出标准、工具使用和审查/交接方法。仅完成来源核查和作者自检，没有做来源隔离的独立实现者消费检查。
