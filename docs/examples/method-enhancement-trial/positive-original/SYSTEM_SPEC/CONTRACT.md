# 接口、数据与工作流

## C1 命令边界

```text
trigger-eval split <suite>
trigger-eval prepare <suite> --skills <comma-separated-skills> --out <directory> [--set train|validation|all]
trigger-eval score <suite> --results <results.jsonl> --out <report.md>
```

`--set` 默认 train。命令同步完成，无配置文件、环境变量默认或隐式网络调用。相对路径以调用时工作目录解析。帮助显示用法并退出 0；缺少必需参数、未知命令/选项、非法 set 值为参数错误，stderr 说明用法和原因，退出 2，不开始文件处理。正常操作退出 0。读取、解析、字段访问、运算和写入异常退出 1，stderr 给出错误类别和原因；不要求复刻某语言的 traceback 路径或堆栈文案。不存在“低分导致非零退出”。

## C2 输入模型与实际验证

面向生产者的常规 suite 形态如下；命令本身**不执行 schema 验证**，不能增加全局必填、枚举、唯一性、非空或数值范围校验。字段仅在相应路径访问时产生效果。

| 字段 | 常规格式、含义 | 实际使用 |
|---|---|---|
| schema_version | 1 | 三命令均忽略；缺失、不为 1 不报 schema 错误。 |
| suite_id | 字符串 | 仅 split 必须访问，原样输出。 |
| target | Skill 标识字符串 | 仅 score 必须访问，精确比较，不裁剪、不大小写折叠。 |
| split_seed | 整数，缺省 42 | split/prepare 使用；score 忽略。显式 null 不使用默认，见 SPLIT。 |
| train_ratio | 数值，缺省 0.6 | split/prepare 使用，不限制为 [0,1]。 |
| trigger_cases | case 对象数组 | 三命令访问；空数组可运行。 |
| output_cases、其他顶层字段 | 任意 JSON | 忽略。 |
| case.case_id | 字符串标识 | split 输出 ID，prepare 用于文件名，score 用于查找；不校验唯一。 |
| case.prompt | 字符串 | 仅 prepare 访问并原样复制。 |
| case.expected | should_trigger / should_not_trigger / edge_case / sibling | 仅 score 对匹配到的 case 访问；其他值也进入兄弟分支。 |
| case.sibling_target | 可选字符串 | 仅兄弟分支比较；缺失按 null。 |
| case.runs | 整数，缺省 3 | 仅 prepare 原样复制，不展开成多份包；0、负数、null、字符串也不拒绝。score 忽略。 |
| case.notes、其他 case 字段 | 任意 JSON | 不复制到任务包，也不参与评分。 |

JSON 按 UTF-8 读取；不执行内容。对象重复键以后出现的值为准。缺失与 null 严格区分，默认只补缺失。JSON null/布尔/数值/字符串/数组/对象保留类型，不把 null 自动变成字符串 `none`。相等比较采用值相等：字符串精确匹配，null 只等于 null，数值按值比较，布尔 true/false 与数值 1/0 相等；数组按位置递归比较，对象按键值比较而非序列化文本。ID 作为映射键时字符串、数值、布尔、null 可用，布尔与相等数值共用键；数组/对象 ID 在 score 建索引或查找时为不可用键错误。常规生产者应使用字符串 ID，但工具不自动转换 score 的键。

类型不适用于所需操作时在该操作报错，不提前拒绝未使用字段。例如 prepare 不需要 target/expected/suite_id；split 不需要 prompt/expected/target；score 不需要 prompt/runs/split_seed。suite 非对象、case 非对象、缺少所访问字段、不可迭代 trigger_cases 等分别在访问/迭代时失败。`trigger_cases` 若是对象或字符串，在 split/prepare 会先迭代其键/字符，非空时通常在访问 case 字段失败；空对象/空字符串可作为空序列继续。score 同样迭代元素建索引。不能因异常输入不合 schema 而用统一的 schema 拒绝覆盖这些结果。

浮点运算采用 IEEE 754 binary64，JSON 整数字段支持任意精度。兼容读取扩展值 NaN、Infinity、-Infinity：比例在 round 时分别发生无法转整数/溢出错误；NaN seed 与 null seed 一样无可重复性承诺。此扩展不是常规生产者所需格式。UTF-8 BOM 不作为合法 JSON 前缀去除；坏编码、坏 JSON、尾随垃圾失败。

## C3 split 工作流

读取 suite → 按 SPLIT 复制并乱序 case 序列 → 切分 → 访问 suite_id 和两部分全部 case_id → 写 JSON → stdout 成功行。

输出位置为 suite 路径最后一个文件后缀替换成 `.split.json`，无后缀则追加；例如 `a.json → a.split.json`，`a.v1.json → a.v1.split.json`，`a → a.split.json`。输出对象按以下键序：`suite_id`、`seed`、`train`、`validation`；seed 为输入原值或缺省 42，train/validation 为各自有序 ID 数组。不会写出完整 case。空 suite 得到两个空数组。JSON 输出采用 UTF-8、非 ASCII 字符原文、两空格缩进、末尾换行，数组/对象保留插入顺序。

成功 stdout 一行：`train {训练条数} / validation {验证条数} → {输出路径}`。生成 split 不修改 suite 内容；输入输出路径实际指向同一文件等别名冲突不受保护。再次调用直接覆盖旧 split。

## C4 prepare 工作流和可见性

读取 suite → **重新计算** SPLIT（不读取已有 `.split.json`）→ 根据 set 选 train、validation 或 train+validation → 递归创建输出目录 → 按所选顺序逐 case 写包 → 写 README.md → stdout 成功行。

all 的顺序为完整乱序后的顺序，不是 suite 原顺序。每个 case 只生成一个 `<case_id>.json`，键序及内容为：

```json
{
  "case_id": "例子",
  "runs": 3,
  "prompt": "用户提示",
  "instruction": "你是一个未参与蒸馏的干净 agent。给定用户 prompt 与已安装 skill 清单，判断该激活哪一个 skill（或 none）。输出 JSON: {\"selected_skill\": \"<slug>|none\", \"reason\": \"...\"}。每条 prompt 独立判断，重复运行之间不携带记忆。",
  "installed_skills": ["target", "sibling"]
}
```

case_id、prompt、runs 原样复制；instruction 为上述固定字符串；installed_skills 来自 CLI 字符串按每个 ASCII 逗号拆分，保留顺序、空项、重复和空白。不检查安装状态、不读 Skill 目录、不补充 name/description。例如 `T, B,,T` 得到 `["T"," B","","T"]`，空字符串得到 `[""]`。

包不包含 expected、notes、sibling_target、target、schema_version、划分标签及任意额外 suite/case 字段。保留 case_id 与 prompt 中原本已有的信息；不会对它们做匿名化、内容脱敏或泄漏检测。隐藏是字段投影，不是加密或访问控制；维护者仍持有 suite 和 split 中的全部 ID。没有选版时机检查，validation/all 可直接请求。验证集能否对调优者保密由维护者管理文件可见性；工具不保证保留集未曝光。

README.md 精确内容（花括号替换变量，最后有换行）：

```text
# 盲测任务包（{set}, {所选case条数} 条）

每个 JSON 是一条盲测任务：把 prompt + installed_skills 交给干净 sub-agent，按 instruction 输出;结果按行追加到 results.jsonl:
`{"case_id": ..., "run": 1, "selected_skill": ...}`

**不要**把 suite 中的 expected/notes 给 sub-agent。
```

README 中的执行建议不会被本能力执行。外部结果生产者自行安排重复次数，把 case_id、run、selected_skill 汇成 JSONL；reason 可提供但评分忽略。输出成功行：`已生成 {所选case条数} 个盲测任务包 → {out目录}`。条数按输入 case 数，重复 ID 覆盖后实际文件数可能更少。空所选集合仍建目录并写 README。

## C5 路径、持久化、失败与恢复

文件 IO 以本地路径语义执行；不扩展 `~` 为用户目录，不自动锁定目录，不给文件附加权限隔离。prepare 把 case_id 转成文本再追加 `.json` 并与 out 拼接；**没有 basename 清洗或目录边界校验**。路径分隔符可以产生子目录，`../` 可以走到父目录，绝对路径可覆盖 out 基准，符号链接按文件系统常规行为跟随。嵌套父目录自动创建。异常字符和保留文件名按目标文件系统报 IO 错误；不声称各 OS 对不可表示路径行为相同。常规跨平台输入应使用普通相对文件名。复现边界验收须将解析后的目标都限制在测试临时目录。

所有 JSON 输出均在写之前创建父目录，然后直接覆盖目标；prepare 的 README 和 score 的报告也是直接覆盖，没有临时文件提交、事务、writer lock、清理旧文件、回滚或续跑记录。输出文件与输入别名冲突不检测；用户负责提供互不覆盖的正常路径。并发写相同路径没有一致性保证，调用方应顺序调用或给独立输出位置。

| 阶段 | 失败和留存 | 恢复 |
|---|---|---|
| 参数或输入读取/解析 | 不产生本次正常输出；已存在旧输出不删除。 | 修正参数、文件或权限，整次重跑。 |
| split 运算/字段访问 | 构造完整对象前不写输出。 | 修复输入后重跑。 |
| prepare 某 case 缺字段/写失败 | 前面写成的包保留；当前文件可能部分写入；后续包不写；README 最后写，可能仍留旧版或不存在。 | 修复后重跑会覆盖同名包；陈旧额外包须由维护者另行清理或改用新目录。 |
| score 读取/解析/匹配/计算失败 | 在完整报告形成之前不创建报告父目录或写报告，旧报告保留。 | 修复结果或 suite 后整次重跑；旧报告不是本次成功结果。 |
| 任一写入失败、中断 | 无回滚；可能保留目录、截断文件或之前完成的文件。无自动取消协议和恢复点。 | 维护者检查终端状态，使用同输入重跑或新输出目录。 |
| 文件写成后 stdout 失败 | 可能已有完整产物但调用报失败。 | 检查产物或重跑；不能从未收到成功行推断无写入。 |

成功命令写完产物才输出成功反馈。score 将完整报告打印到 stdout（文件末尾换行后打印再加一个换行），其余命令只打印成功行。标准输出不是机器 JSON。退出码和本次产物共同确认操作完成，不存在常驻“评测状态”或自动删除策略。

## C6 必要依赖闭合

| 依赖 | 所有者、输入输出与时序 | 失败及验收 | 集成状态 |
|---|---|---|---|
| 本地 suite | 目标环境在启动前提供稳定可读 UTF-8 文件；维护者保管答案；工具只读，路径别名例外见 C5。 | 缺失/不可读/坏 JSON 报错，不当空 suite。 | 用户声明可提供；具体适配尚未实现。 |
| 外部逐例结果 | 目标环境在 score 前提供完整可读 JSONL 快照；生产者写入，评分只读；不要求此工具生成结果。 | 解析失败退出；少行、重复、未知行按 SCORING，不变成新的失败条件。 | 用户声明可提供；无需真实选择器作为规格前提。 |
| 本地文件系统、进程和终端 | 环境提供读取、写输出、创建父目录与命令执行；沿当前身份权限；工具承担同步命令和错误传播。 | 读写失败退出非零，部分文件按 C5 留存；权限修复后重跑。 | 用户已给环境能力；特定 OS 集成待实现验收。 |
| 技能清单 | 维护者传入字符串；工具只负责逗号拆分与投影。 | 空白、空项不报错，见 C4。 | 无 Skill 安装系统依赖。 |
| 随机与计分语义 | 纳入本套件 SPLIT/SCORING；实现可内置或选等价库。 | 验收向量必须相符；不能换 RNG 只保留 seed。 | 下游实现职责。 |

一条完整旅程为：维护者提供 suite → split 阅读 ID 划分 → prepare 默认训练包或显式验证包 → 外部提供结果文件 → score → 阅读完整报告。三个命令独立，score 不依赖 split 文件、包目录、候选清单或某次 prepare 的 set；不隐式按 train/validation 过滤。
