# 调查记录

## 请求与边界

用户请求：使用已安装的 $repo-to-spec。参考仓库是 /Volumes/2T/dev/reference/cangjie-skill，参考版本以实际 HEAD 为准。本次只选择性吸收其本地 Skill 触发评测的确定性能力：从 suite 生成训练/验证划分和盲测任务包，并依据外部提供的逐例选中结果生成评分报告，供维护者阅读。请忠实恢复当前可观察规则，包括边界和异常；没有授权改变评分规则。不要求调用真实 Skill 选择器、作发布决定或设计新通过阈值，也不吸收蒸馏、编译、更新能力。目标环境能提供本地 suite 文件、逐例结果、文件读取及命令执行；目标实现语言、框架和操作系统未限定。交付可脱离来源仓库实施的 SYSTEM_SPEC/，调查依据另放 WORKLOG.md。只按已安装插件读取方法；不要读 Repo-to-Spec-Plugin 开发工作区、已有样例和验证记录。参考仓库只读；运行任何来源脚本前先审查副作用，安全探针仅在本临时目录执行。

- 版本：`874eb414e6414dd6d399222a7e3925206dfdb585`；开始调查时 `git status --porcelain` 为空。
- 方法：仅读取已安装缓存 `/private/tmp/repo-to-spec-method.m8D40z/home/plugins/cache/repo-to-spec-local/repo-to-spec/0.1.0/skills/repo-to-spec/` 内入口、调查/场景/选择性吸收/输出/审查/数据契约/解耦/异常方法及提纲；未读取插件开发工作区或其样例、验证记录。
- 本地指引：查找来源及父目录 AGENTS.md、仓库 CLAUDE.md，无命中；阅读 README.zh-CN.md 产品入口、CONTRIBUTING.md。
- 未获准改变任何评分行为；图形界面、模型调用、发布判断、输出评测、蒸馏/编译/更新均不纳入。

## 依据与已确认规则（静态核对）

| 问题 | 依据 | 结论 |
|---|---|---|
| 三个入口 | scripts/run_trigger_evals.py:32–164 | split/prepare/score；无模型执行。 |
| 统一 CLI 是否必要 | scripts/cangjie.py:243–258 | eval 默认及 eval trigger 仅透传到触发脚本；完整宿主 CLI 非依赖。 |
| 划分 | run_trigger_evals.py:32–47 | Random(seed) shuffle、round(n*ratio)、切片；默认 42/0.6；prepare 重算不读 split 文件。 |
| 任务包 | 同文件:50–77 | 白名单字段、runs 默认 3 原样复制、技能按逗号拆分；逐例覆盖写入，最后写 README。 |
| 评分 | 同文件:80–133 | 对所有非空结果行计 runs；未知 ID 跳过；重复计数；不核齐全；兄弟选错但非目标计 TN；任意其他 expected 走兄弟分支。 |
| 共享 IO | scripts/cangjie_common.py:53–60 | UTF-8，JSON 无 schema 验证；父目录递归创建、直接覆盖，非原子写。其余缓存、锁、发布函数不被所选入口调用。 |
| 声明格式与执行差异 | schemas/eval-suite.schema.json | 声明 minItems=1、expected 枚举等，但三个命令不调用 schema；不得把声明约束增加为运行拒绝。 |
| 文档原则与执行差异 | methodology/06-stage4-pressure-test.md:14–32,78–87 | 文档强调缺失样本不排除及独立盲测；触发脚本实际不做覆盖率检查，不调用 agent；按用户要求恢复脚本可观察语义。 |

## 运行前副作用审查

完整阅读 run_trigger_evals.py 与其唯一来源导入 cangjie_common.py。后者顶层只导入标准库、尝试导入 yaml、定义常量和函数，无顶层发布/删除/网络动作；本次只调用 load_json/dump_json。split 写 suite 同目录的替换后缀文件；prepare 可按 case_id 路径写文件且无路径防护；score 写指定报告。均无来源文件自动更新。复制这两个文件至本工作目录 `.investigation/` 后才运行；设置 PYTHONDONTWRITEBYTECODE=1，所有 suite、results、输出和路径边界夹具均限定在此临时目录；不运行完整宿主、真实选择器或来源测试套件。

## 受控运行（已验证事实，范围限于以下输入）

运行环境为本临时目录、Python 3.12.13；无真实宿主或选择器。共 18 个来源副本命令探针，输入及完整 stdout/stderr/产物保存在 `.investigation/observations.json`，驱动在 `.investigation/probe.py`。另有 3 个补充检查记录于 `.investigation/extra-check.json`。

| 观察 | 实际结果 | 正式规则 |
|---|---|---|
| 默认 seed=42、5 case | 排列 3,1,2,4,0，train 3/validation 2 | S1/S4 |
| ratio=-0.4/0/0.5/1/2/null | 依次 3/2、0/5、2/3、5/0、5/0、TypeError 退出 1 | S1/A2 |
| 空 cases；seed=[] | 空集正常输出；数组 seed 类型错误 | S1/S3 |
| prepare all + `T, B,,T` | 包只有 5 字段，技能保留空白/空项，runs=3 | C4/A1 |
| 10 行含重复、未知 ID、兄弟选错与 null | runs=10，TP2/FP2/FN1/TN4，P=.500/R=.667/F1=.571，混淆 1/4 | R/A1 |
| 空白结果 | 退出 0，零分完整报告 | R3/A4 |
| 坏 JSONL/缺 case_id | 退出 1，无新报告 | R1/A4 |
| 缺 selected / run=null | none 默认、#rNone；不校验 run | R1/R4 |
| suite 重复 case_id | 后定义覆盖；正例后是 edge_case 则计 FP | R1/A4 |
| prepare 第二 case 缺 prompt | 第一包保留，退出 1，无新 README | C5/A3 |
| ID=../escaped | 写到 out 父目录内（仍在本临时目录） | C5/A3 |
| sibling_target=target 且选 target | 混淆(FP)，不判 OK | R2/A4 |
| 坏 JSONL 前已有旧报告 | 旧报告原样保留 | C5/A5 |
| 参数缺失/非法 set | 参数错误退出 2 | C1/A5 |

从规格所写 MT19937、播种及拒绝采样步骤独立编写 `.investigation/verify_algorithm.py`（无来源函数调用），对 12 种 seed × 6 种长度共 72 组排列与调查环境的 random.Random 比较，全部一致；含负数、大整数、字符串、正负浮点和 1000 元素，记录在 `.investigation/algorithm-check.json`。这验证了规格算法表达与本次观察环境的兼容性，不是目标实现或所有平台的验证。

## 推导设计、依赖与冲突处理

- **推导设计**：用可替换启动器 `trigger-eval` 表达三个独立命令；不将原 Python 文件名、完整 cangjie CLI、PyYAML、操作系统锁定为目标依赖。错误堆栈布局由实现决定，但保留错误类别、退出状态和写入时点。固定随机算法语义而不是固定语言。
- **推导设计**：将维护者、外部结果生产者、文件系统提供者的所有权与失败恢复汇合成 C5/C6；目标未编码不是规格阻塞，亦不宣称现有集成已可用。相同路径并发不获一致性保证，建议独立目录/顺序调用，不增内部锁。
- **已验证事实（静态）**：来源没有校验 schema、结果齐全、候选集、run 唯一性、路径边界、事务写入。不能把其他模块的锁、缓存或发布保护移植为本能力已有行为。
- **冲突已解释**：方法文档要求完整结果和更广的盲测流程，触发评分器不强制执行；本请求明确恢复当前可观察规则，因此保留不完整也可成功报告，不新增拒绝/告警阈值。输出评测的缺失样本修正不能外推到触发评分。
- **边界**：盲测只投影字段，不承诺 case_id/prompt 脱敏，不执行模型隔离；validation 可随时导出，保密由维护者文件可见性承担。无需把选版/发布机制纳入。
- **用户批准的改动**：仅用户明确的选择性吸收边界与独立实施交付；没有任何新评分、通过阈值或发布策略获授权，也未加入。

## 最终审查与交接

候选 v1 为 SYSTEM_SPEC/ 下 README、CONTRACT、SPLIT、SCORING、ACCEPTANCE 五份文档。

1. **来源忠实性作者核对**：沿三个入口与共享 IO 逐分支比对字段访问、默认、排序、切片、计数、异常、覆盖/残留。特别核对未知/重复/缺失结果、兄弟错误仍 TN、schema 不执行、all 为乱序、prepare 重算划分、直接写非事务。无未授权评分变化。非整数 seed 与错误类型等边界补写到正式契约，避免只写正常 schema。
2. **自包含作者自检**：仅按文档推导正常旅程、第二包失败、坏结果保留旧报告、重跑等路径；用正文写独立随机算法验证；验收包含完整 suite/JSONL 与精确计数，无需来源材料。职责、环境契约和语言/平台自由均有对应不变结果。此项是作者自检，**未安排独立接收者消费检查**。
3. **结构检查**：五文档 Markdown 围栏成对、相对链接有效、正式套件没有来源绝对路径或 `.investigation` 依赖。检查只证明结构，不代替语义核对。
4. **版本与只读复核**：结束时 HEAD 仍为 `874eb414e6414dd6d399222a7e3925206dfdb585`、来源工作区仍干净。两个来源副本与来源字节一致，SHA-256：run_trigger_evals.py=`06dadfc102fbe94ee0bbc637e433428062af9d0f5f29f81ee48367072a0b64e7`；cangjie_common.py=`f320eaa1e72361cc521de0c36e646273467c3762d0e4e01fbbf867f124053e2e`。

限制：未运行真实选择器、目标实现或完整宿主；权限拒绝、中断、磁盘写失败、并发等以静态 IO 顺序分析为依据，未做故障注入；不宣称全异常动态覆盖。调查环境启动 Python 时 mise 尝试写其缓存被沙箱拒绝，命令正常继续；未修改环境权限或安装依赖。正式规则无已知影响声明范围实施的未决项，交付状态为规格完成；后续是目标实现及其验收，不是本次请求剩余工作。
