# 场景、输出与工具方法增强的试跑

日期：2026-09-29。本记录只覆盖本轮材料变更的实际试跑；教学例、来源探针、原始生成、评审修订、独立消费、宿主加载和目标实现是不同证据。

## 固定输入与宿主

- 参考仓库：本地 `cangjie-skill`，HEAD `874eb414e6414dd6d399222a7e3925206dfdb585`；三次会话前后工作区干净。来源 `SKILL.md` 标注 `cangjie.version: 2.5.0`，HEAD 无同名 tag。
- 宿主：macOS 的 Codex CLI `0.158.0-alpha.2.1`；在隔离临时 `CODEX_HOME` 执行 `codex plugin marketplace add /Volumes/2T/dev/Repo-to-Spec-Plugin` 和 `codex plugin add repo-to-spec@repo-to-spec-local`，插件报告版本 `0.1.0`。每例都用新的 `codex exec --ephemeral` 会话和独立临时工作目录。仅复用本机登录认证；会话结束后断开临时认证链接，未修改用户配置。目标参考仓库只读，来源脚本先审查后复制到临时目录做安全探针。
- 首轮安装缓存与当时插件包逐文件一致，入口 `SKILL.md` 的 SHA-256 为 `af17e85b605f55d26bdcc6fd3474c5efd5984ad4333c8e43ee5def25d660cdad`；会话事件实际显示从**安装缓存**读取入口、场景、调查、吸收、行为、接口、解耦、输出和审查材料。不是只在开发聊天中提示方法。
- 首轮输入原文保存在[正例请求](method-enhancement-trial/positive-original/REQUEST.txt)和[缺输入请求](method-enhancement-trial/missing-original/REQUEST.txt)。执行者被要求不读本仓库开发记录/旧样例。它们同属真实仓库，但产品请求不同，不能互换结论。

## 输入充分的正例：只要评测报告

用户要吸收来源 trigger runner 的 split、prepare、score 确定性能力，外部提供逐例选择结果，产出供维护者阅读的报告；未授权真实选择器、发布门禁、新阈值或其他邻接能力。新会话退出 `0`，生成[原始 `SYSTEM_SPEC/`](method-enhancement-trial/positive-original/SYSTEM_SPEC/README.md)和[原始工作记录](method-enhancement-trial/positive-original/WORKLOG.md)。仓内副本与临时原件逐文件一致，未就地修稿。执行者报告 18 个来源探针、3 个补充检查与 72 组随机算法比对；这些是其工作记录中的观察，审查者没有重跑全部探针。

原始规格区分：来源 CLI 不调用真实选择器；`score` 缺结果不补 FN、未知 case 算入 `runs` 却不进分类、错误兄弟选择仍可记 TN、分数不控制退出状态。它保留这些已观察规则，没有发明门槛，也没有因目标选择器尚未实现而阻塞**报告能力**的规格。来源核查者只读请求、来源和原始输出，认为核心来源忠实，但指出两项低优先级精确兼容遗漏：长选项唯一前缀、超长十进制整数的来源运行时解析边界。另一位只拿正式套件与请求的独立接收者认为常规旅程可实施，但指出允许非字符串 ID/容器值后，文件名转换与报告引号/转义未定。来源核查不能证明套件自包含；只读消费不能证明来源忠实。

保留原稿，另存[评审修订稿](method-enhancement-trial/positive-reviewed/SYSTEM_SPEC/README.md)：规定可观察的长选项前缀、成功解析后的整数精度与超长文本解析限制的区别、非字符串文件名/报告文本的兼容语义及向量。两名原检查者分别复查自己的发现，均认为已闭合且未发现修订带来的实质问题。修订是**评审后工作**，不能倒写为原始自动生成已正确。目标工具未实施，上述验收向量未在目标实现上运行。

## 关键输入不足的对照：真实选择和发布准入

第二个新会话的请求包含真实 Skill 选择与发布决定，但目标产品未提供选择器接口、候选集合、通过阈值和发布策略。会话退出 `0`，产出[原始部分规格](method-enhancement-trial/missing-original/SYSTEM_SPEC/README.md)及[工作记录](method-enhancement-trial/missing-original/WORKLOG.md)，仓内副本与原件逐文件一致。工作记录记载 6 次临时来源 CLI 探针；没有运行真实模型或目标发布流程。

该套件恢复来源 split/prepare/score，另将真实评测所需的结果完整性和报告有效性写成有依据的目标设计；它没有把原始评分误称为发布规则。真实选择器、竞争候选、阈值、包级准入及支持环境列为受影响的未决，说明各自所需材料、责任和下一验收；已闭合核心仍可实施。它明确是**部分交付**，不称整个原请求完成。此例没有另做来源隔离的独立消费检查，作者工作记录中的自检不能替代它。

## 反馈后重新安装的窄范围复跑

正例发现促使插件[输出标准](../../plugins/repo-to-spec/skills/repo-to-spec/references/specification.md)、[工具指南](../../plugins/repo-to-spec/skills/repo-to-spec/references/tools.md)和[审查方法](../../plugins/repo-to-spec/skills/repo-to-spec/references/review.md)补上**仅在声称精确文本兼容时**核对所有接受值的文件名/报告表示、引号转义及解析器边界。这是可复用判断，不把 Python 或该 runner 的规则设为所有任务默认。变更分别经过独立内容补审。

重新在第二个隔离 `CODEX_HOME` 安装**修改后的当前包**；再次逐文件核对安装缓存与插件包一致。入口哈希未变，`specification.md` 哈希为 `986a98dd4c3a1839f17f67c1aea7b9d046ac7a661a74a04cf2f1588629515b79`。全新会话实际从第二缓存读取入口和修订后的输出、工具、审查资源，仅请求 score 报告能力。会话退出 `0`，生成[原始窄范围规格与向量](method-enhancement-trial/final-installed-original/SYSTEM_SPEC/README.md)及[工作记录](method-enhancement-trial/final-installed-original/WORKLOG.md)；仓内副本与原件逐文件一致。执行者报告 26 次受控 CLI 观察和作者自检，并把非字符串、引号/转义、数值比较单列为语言无关契约，未加入选择器、阈值或门禁。**这次窄范围输出尚未做独立来源核查或只读消费检查**；不能把前一份修订稿的审查结论自动移到它，也不能视作首轮完整 split/prepare/score 与缺输入对照在反馈后又完整重跑。

## 实际检查与限制

- 插件包内容审查曾发现合成例中的发布依赖、`404` 分支和隐式取消证据三处矛盾；修订后同一独立审查者补审通过。UI 与完整产品例子是**合成教学材料**，没有声称对真实 UI 或完整产品执行过逆向。
- `python3 scripts/ci_check.py --self-test`、`python3 scripts/ci_check.py`、`.venv/bin/python scripts/check_design.py --self-test`、`.venv/bin/python scripts/check_design.py`、Skill creator `quick_validate.py` 和完整 `git diff --cached --check` 均通过；另检查 58 个相关 Markdown 的本地链接，未发现断链。原始向量 `final-installed-original/SYSTEM_SPEC/fixtures/splitlines/results.jsonl` 故意含空白行和 CRLF，首次差异检查报警；仅对该路径在 `.gitattributes` 关闭尾随空白与空格后 TAB 的判定，保留原始字节与其他差异检查。包检查只验证结构、元数据、路径和链接，不能代表语义审查。
- 已验证的是 Codex CLI 的本地安装、安装缓存资源读取与上述三个明确范围的会话；未实测 Codex 桌面端加载、完整产品或真实 UI 来源、目标选择器、发布流程、目标实现、生产权限/运行条件。一次真实仓库案例不能外推为所有产品类型稳定支持。
