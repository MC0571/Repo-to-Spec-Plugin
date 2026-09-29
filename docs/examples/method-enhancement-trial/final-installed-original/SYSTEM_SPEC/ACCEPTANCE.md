# 验收

## A1 黄金报告

对每个 `fixtures/<名称>/`，将 `suite.json` 与 `results.jsonl` 作为输入，以新的临时路径作为输出。必须退出 0、stderr 为空，报告与同目录 `report.md` 在仅归一 CRLF 后逐字符一致；stdout 与报告相比恰好多一个末尾换行。不要只比较渲染后 Markdown 或数值摘要。输入在输出路径不重叠时不变。

| 夹具 | 必须区分的行为 | 对应规则 |
|---|---|---|
| [branches](fixtures/branches/report.md) | 七种判定分支、未知 expected、未知 case；N=11，TP=1、FP=3、FN=1、TN=5、C/B=1/4 | C2、S1–S3 |
| [empty](fixtures/empty/report.md) | 空 suite、空结果仍成功；0.000，表头保留 | C2、S2–S3 |
| [duplicates](fixtures/duplicates/report.md) | 同键 case 后者生效；相同 run 重复计数；缺失计划运行不补行；未知结果增加 runs | C2、S1 |
| [defaults](fixtures/defaults/report.md) | 缺失 selected 默认字符串 none；显式 null 不默认；缺失 sibling_target 为 null；target 可为字符串 none | C2、S1、V1 |
| [values](fixtures/values/report.md) | 对象 target、非字符串 expected/run/selected、真假键匹配、嵌套引号、控制字符及 Markdown 原样换行 | V1–V2、S3 |
| [numeric](fixtures/numeric/report.md) | 1/1.0/true 键覆盖、数值与布尔相等、负零、普通/指数浮点格式 | V1、V3 |
| [containers](fixtures/containers/report.md) | 数组及对象值递归比较，容器 expected 走兄弟分支 | V1、S1 |
| [nonfinite](fixtures/nonfinite/report.md) | NaN、无穷和指数溢出被接受，非有限值转文本 | C2、V1、V3 |
| [nan_identity](fixtures/nan_identity/report.md) | NaN case 键匹配；容器内 NaN 相等，标量 NaN 不相等 | V1 |
| [unmatched_missing_expected](fixtures/unmatched_missing_expected/report.md) | 未命中 case 缺 expected 不报错，未知行仍计入 N | C2 |
| [empty_object_cases](fixtures/empty_object_cases/report.md) | trigger_cases 为 {} 时兼容空索引，不做额外类型校验 | C2 |
| [splitlines](fixtures/splitlines/report.md) | 空白行、CRLF、NEL、Unicode 行分隔符 | C2 |
| [duplicate_keys](fixtures/duplicate_keys/report.md) | JSON 对象重复字段取末值 | C2 |
| [unicode_repr](fixtures/unicode_repr/report.md) | 嵌套字符串的引号选择、控制/格式/私用/代理码点转义、emoji 原样显示 | V2 |
| [rounding_1](fixtures/rounding_1/report.md) | precision=1/16→0.062，不用一般“逢五进一” | S2 |
| [rounding_3](fixtures/rounding_3/report.md) | precision=3/16→0.188，F1 从未舍入值计算 | S2 |

## A2 边界变体

以下均从一个有效夹具修改，使用新输出路径：

1. 将 empty 的 trigger_cases 改为 `""`，仍与 empty 报告完全一致；改为非空字符串、非空对象或 null，则结构失败。
2. suite 中添加任意 suite_id、schema_version、prompt、runs 或 split 配置，报告不改变；删除未使用的这些字段也不改变。
3. sibling_target=target 且 selected=target：输出 `混淆(FP)`，不是 `OK`。
4. 调换结果行顺序：报告行跟随交换，计数不变。结果 run 改为任意 JSON 值仅改变标签；删除 run 显示 `#r1`。
5. 数值 case_id=1 不匹配字符串 case_id=`"1"`；true 则匹配。整数 9007199254740993 不等于浮点 9007199254740992.0。
6. 两对象键顺序不同但值相等，应判相等；报告仍按各自插入顺序显示。重复对象键的最后值应显示在该键首次出现的位置。
7. JSONL 仅空白行与空文件结果一致。含字面 U+2028 的 JSON 字符串先被断行并解析失败；改为 `\u2028` 转义可解析，报告直接字符串中出现真实行分隔符。
8. 重复执行相同输入到相同输出，内容相同且不追加；旧输出放置任意文本应被完全覆盖。缺失的多级父目录自动创建。

## A3 错误与恢复

每项单独运行。输入错误应退出 1、stdout 为空；若故障发生在输出阶段之前，预置报告 `KEEP\n` 必须原封不动，原本不存在的输出父目录不得被创建。移除故障后整次重跑，必须恢复到相应黄金报告。

| 场景 | 输入/故障 | 预期 |
|---|---|---|
| 必需参数 | 不给 --results 或 --out，或给未知选项 | stderr 用法诊断、退出 2、无报告副作用 |
| 文件/编码 | 不存在文件、不可读文件、非法 UTF-8 | 输入读取或解码失败；不是零分成功 |
| JSON 语法 | suite 带 UTF-8 BOM；JSONL 非空坏行或多值同行 | 解析失败，不跳过坏行 |
| suite 根及必需字段 | 根为 null；缺 target 或 trigger_cases | 结构失败；不能补默认目标或默认为空 suite |
| case 索引 | case 缺 case_id，或 case_id 为 [] / {} | 建索引失败，即使 results 为空 |
| result 结构 | 行为数字、数组或 null；对象缺 case_id；case_id 为 [] / {} | 结构/键失败，不当作未知 case 跳过 |
| expected 延迟访问 | case 有 case_id 但无 expected，且存在命中结果 | 失败；去掉命中行则可成功 |
| 解析优先 | 第一行 `{}`，第二行 `{broken` | 先报告 JSON 解析失败，而不是第一行缺 case_id；全部非空行先解析 |
| 输出父路径 | 父目录某层为普通文件 | 输出路径失败；无完整 stdout |
| 输出文件 | 输出路径是目录、或无写权限 | 写出失败，非零退出；若打开未成功，原内容保留 |
| UTF-8 输出 | target 为 JSON `"\ud800"`，空 case 与空结果 | 写出编码失败；文件可已创建/截断；不许假称成功 |
| 输出通道 | 文件可写但 stdout 关闭或编码不支持 | 非成功，允许文件已完整、stdout 部分输出 |
| 路径别名 | 输出路径与输入路径相同，使用可丢弃输入副本 | 先读取再覆盖，按原输入产生报告；不引入同路径拒绝 |
| 中断/并发 | 写出中断，或同一路径多进程写出 | 不要求原子报告/回滚；维护者检查并串行重跑，不把残留文件当本轮成功 |

stdout/stderr 故障、真实权限失败及中断的测试需要目标平台适当夹具；文件系统依赖按宿主权限执行，不要求提权才能验收。性能无固定 SLA；测试环境应保证输入可在可用资源内处理。
