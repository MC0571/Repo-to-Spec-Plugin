# score 规格调查记录

## 请求与边界

用户请求原文：

> 使用已安装的 $repo-to-spec。参考仓库为 /Volumes/2T/dev/reference/cangjie-skill（以实际 HEAD 定版）。本次只恢复 scripts/run_trigger_evals.py 的 score 报告能力：目标环境从本地 suite JSON 和外部逐例选择结果 JSONL 生成供维护者阅读的原始报告，保持当前可观察规则及已接受输入的输出文本兼容。不要设计真实选择器、发布准入、通过阈值或 split/prepare 的实现；只写 score 必需的输入契约与依赖。目标语言、框架和操作系统不限定。交付独立可实施的 SYSTEM_SPEC/，调查记录另放 WORKLOG.md。只读取已安装插件资源与指定参考仓库，不读取 Repo-to-Spec-Plugin 开发工作区或此前样例；参考仓库只读，安全探针在本临时目录。

调查日期：2026-09-29。参考 HEAD：`874eb414e6414dd6d399222a7e3925206dfdb585`；开始时 `git status --short` 为空。无仓库内 AGENTS.md（文件搜索及 tracked 文件检查）。读取本地 README、CONTRIBUTING 作为使用/指引材料，未执行其中安装、构建或网络命令。

技能：已安装的 `/private/tmp/repo-to-spec-method.m8D40z/home-final/plugins/cache/repo-to-spec-local/repo-to-spec/0.1.0/skills/repo-to-spec/SKILL.md`。读取其 investigation、scenarios、absorption、specification、contracts、decoupling、review、behavior 方法及 spec-outline；未访问插件开发工作区或此前样例。方法文档中的合成教学内容未作为被调查仓库事实。

参考仓库只读。安全探针与输出都在本目录 `probes/`；正式自包含样本在 `SYSTEM_SPEC/fixtures/`。以 `python3 -B` 执行指定参考脚本，禁用字节码写入；未安装依赖、未调用模型或联网。调查解释器为 CPython 3.12.13，Unicode 数据 15.0.0；这是观察条件，不是目标技术栈要求。shell 环境出现 mise 缓存写入被沙箱拒绝的警告，未影响子进程判分或黄金 stdout 捕获。

## 证据与结论

| 问题 | 性质与依据 | 结论/正式位置 |
|---|---|---|
| 真正入口 | 已验证事实，静态：scripts/run_trigger_evals.py:140–164；scripts/cangjie.py:240–259 | 原主工具仅转发 eval/trigger 调用，不补验证；目标只需独立 score 入口。CONTRACT C1。 |
| suite 读取依赖 | 已验证事实，静态：scripts/cangjie_common.py:61–62；run_trigger_evals.py:80–84 | UTF-8+json.loads；没有 Schema 校验、没有 YAML 处理。C2 纳入这些语义，无需整个 common 模块。 |
| Schema 与实际接受域 | 已验证事实，静态比较 schemas/eval-suite.schema.json 与 score；受控运行 empty、values、empty_object_cases 等 | Schema 声称的 suite_id/prompt、枚举和最小数组长度不是 score 的拒绝条件；以当前可观察路径恢复宽松域。 |
| 计数/配对 | 已验证事实，静态：run_trigger_evals.py:83–116；运行 branches、duplicates、defaults | 最后 case 覆盖；未知结果计 runs 不计分类；缺失/重复运行不完整性校验；未知 expected 走 sibling。S1。 |
| 兄弟分支 | 已验证事实，静态及 branches/containers | 目标优先混淆；错选非目标也 TN；missing sibling_target 为 null。未按方法示例擅自改成门禁。 |
| 比率与报告 | 已验证事实，静态：run_trigger_evals.py:118–135；全部成功探针 | binary64 顺序运算、三位小数；固定模板；stdout 比磁盘报告多一个 LF；成功总退出 0。S2/S3。 |
| 非字符串文本 | 已验证事实，静态 f-string 路径及 values/numeric/unicode_repr/nonfinite/nan_identity 运行 | 不能改用 JSON dumps；需 D/R、引号选择、控制字符转义、NaN/inf、数值布尔相等和 NaN 容器语义。V1–V3。 |
| 全量解析先于匹配 | 已验证事实，静态：results 列表构造先于循环；bad_line 运行仅证明 JSON 错误终止 | 正式补 A3 混合错误优先级验收；未声称该组合已运行。 |
| 失败副作用 | 已验证事实，静态写序；missing_expected/unhashable/bad_result_id/missing_result_id/bom/scalar_result 等运行 | 写出前失败不产生正常报告；existing_failure 重跑验证已有报告保留；surrogate_write 验证编码失败文件可能截断。C3。 |
| 语言与平台 | 推导设计，依据用户不限定与外部结果兼容要求 | 解析/比较/文本语义为约束；解释器、库、CLI launcher、内部模块可替换。字符文本兼容，允许宿主 CRLF 转换；黄金文件固定 LF。 |
| 外供与所有权 | 推导设计，依据用户指定本地 suite 与外部 JSONL | 外供稳定输入，调用者文件权限，score 内部只做确定性处理；提供者尚未实现不阻碍规格闭合。README 依赖表。 |
| 非范围 | 用户明确排除 | 不设计 selector、split、prepare、阈值、发布或非劣检验；固定尾注保留，不要求访问 §10.3。 |

读取同版本 docs/reports/2026-08-25-v2.1-implementation-report.md 的 Phase 3 描述，声称 precision/recall/F1/兄弟混淆率，与当前路径一致；未将其盲测与统计意图扩大为 score 实际承诺。tests 搜索未找到该触发 score 的专门单元测试；输出评测的测试属于另一能力，未作为本次 score 行为证据。

## 受控观察

- `probes/observe.py`：19 个独立 CLI 调用，12 成功、7 失败；`probes/summary.json` 保存退出码、输出存在性及错误类别，逐项目录保留输入与 stdout/stderr。成功报告全部验证 stdout=report+LF。
- `probes/extra.py`：7 次 CLI 调用，包括 4 个额外成功向量、解析失败后预置 KEEP 文件的再次失败、未配对代理码点写出失败。`probes/extra-summary.json` 记录结果。黄金夹具共 16 组。
- 分母为零、未知/重复、非字符串/容器、数值格式、半偶舍入、Unicode 转义和扩展非有限值均有可区分反例。
- 未做真实无权限身份切换、断电/信号注入、stdout 断管、不同操作系统运行或下游替代实现；相应行为由静态调用顺序和普通文件/通道语义定界，并列为目标验收，不冒称运行通过。
- 调查只验证指定 HEAD、上述输入和运行条件；未推论整个原产品或所有宿主已通过。

## 审查与交接

作者自检分两轴进行，不称独立接收者检查：

1. 来源忠实性：逐项核对入口、索引、缺省、分支、公式、固定文本和写入顺序；特别检查未引入 Schema 限制、run 完整性、错兄弟改判、通过阈值、目标技术栈限制。用受控反例消除非字符串输出、NaN 容器相等和编码失败截断的缺口。
2. 自包含可实施性：仅从正式文档的入口→输入→比较→判分→格式→失败恢复顺序复读；所有需要原仓库的定位/调查记录留在此文件，正式套件给出值语义和精确文本而非“参考源码”。A1 黄金文件用于全文比较，A2/A3 覆盖变体和恢复。独立接收者审查未安排，下游目标实现未编写。

普通浮点最短转换与 Unicode 可打印定义已经在兼容层定值，未将“转成字符串”留作各语言默认。必要技术设计以职责和执行顺序给出，不引入数据库、锁或事务承诺。已确认范围无影响实施的重要未决；最终交付为文档规格与验收输入/预期输出，不是已实现或已集成的软件。

最终结构检查：16 组夹具各含 suite.json、results.jsonl、report.md；正式文档内部链接全部可解析，报告末尾换行符合模板，正式文档无参考仓库绝对路径。此检查仅证明载体完整，不替代语义验收。结束时再次核对 HEAD 未变，参考仓库工作树仍无改动。
