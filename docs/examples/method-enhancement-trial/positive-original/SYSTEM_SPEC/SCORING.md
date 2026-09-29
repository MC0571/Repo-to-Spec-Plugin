# R：评分和报告

## R1 输入与匹配次序

读取 suite，访问 target，然后按 suite 原序建立 case_id→case 映射，同 ID 的后一个覆盖前一个。读取整个 results 文件，按文本行拆开，忽略 strip 后为空的行，其余每行解析一个 JSON 值；全部解析完成后才开始判分。行首尾空白允许。一个 JSON 对象横跨多行不属于 JSONL；任一非空行解析失败使整次命令失败，不提供部分新报告。

常规行形态为 `{"case_id":"c1","run":1,"selected_skill":"T"}`。case_id 在每行必须可访问，run 缺失默认 1，selected_skill 缺失默认字符串 `none`。null 不使用默认。run 原样用于展示，不校验整数、正数、范围或顺序。reason、时间、模型、其他字段均忽略。

逐行按文件顺序处理：取 case_id，查映射；找不到则跳过，既不产生表行也不分类，但仍计入报告 runs。找到后再读取 selected_skill 和 case.expected。未知 ID 行即使没有 selected_skill 也可跳过；行没有 case_id、行非对象、键不可用则报错。suite 中未收到任何结果的 case 不产生行、不计 FN，也不报错；缺 expected 的 case 仅在匹配到结果时失败。

每一匹配行独立计数；不按 case_id+run 去重、不投票、不对多次结果求平均、不检查 suite.runs，也不要求所有候选或 train/validation 全量完成。重复结果行、重复 run 标签、缺失 run、超出 runs 的 run 都按一行计数。score 不读取任何任务包、split 文件或已安装技能清单；任意 selected_skill 可进入比较。

## R2 唯一判定表

先令 triggered = (selected_skill == suite.target)，相等语义见 CONTRACT。TP/FP/FN/TN、sibling_total/sibling_confused 均从零开始。

| case.expected | 条件 | 表中判定 | 计数 |
|---|---|---|---|
| should_trigger | triggered | TP | TP+1 |
| should_trigger | 非 triggered | FN | FN+1 |
| should_not_trigger 或 edge_case | triggered | FP | FP+1 |
| should_not_trigger 或 edge_case | 非 triggered | TN | TN+1 |
| 其他任何值（含 sibling、未知字符串、null） | triggered | 混淆(FP) | sibling_total+1，sibling_confused+1，FP+1 |
| 同上 | 非 triggered 且 selected_skill == sibling_target（缺省 null） | OK | sibling_total+1，TN+1 |
| 同上 | 非 triggered 且不等于 sibling_target | 未中兄弟({selected_skill展示文本}) | sibling_total+1，TN+1 |

兄弟分支先看 triggered，故 sibling_target 与 target 相同且选中它时仍为混淆(FP)。选错其他 Skill 或选 none，尽管表中不是 OK，仍是 TN，不记 FN，不增加 sibling_confused。兄弟分母是匹配到兄弟分支的**结果行数**。没有 sibling_target 且 selected_skill 显式 null 时，如果 target 非 null，则判 OK；selected_skill 缺失则为字符串 none，通常判未中兄弟(none)。target 若本身为 null 等非字符串，也按同一比较规则处理，不先验证 slug。

## R3 指标

```text
precision = TP/(TP+FP)，分母为零时 0.0
recall = TP/(TP+FN)，分母为零时 0.0
F1 = 2*precision*recall/(precision+recall)，分母为零时 0.0
兄弟混淆率 = sibling_confused/sibling_total，分母为零时 0.0
runs = 解析成功的全部非空结果行数量（包括未知 ID）
```

先以 binary64 计算未舍入的 precision、recall，再算 F1；仅展示时固定三位小数，最接近舍入、中点取偶。不得用已展示的三个小数回算 F1。分类计数之和等于已匹配行数，可小于 runs。TN 不进入 precision/recall/F1。空结果是有效输入：所有计数和比率为零、仍写报告、退出 0。低分、未中兄弟或未知行不会改变退出状态。

## R4 报告格式

按下列顺序生成 UTF-8 Markdown；不创建 JSON 评分文件、完成率、pass/fail 字段、告警列表或新阈值。配对指“结果行与对应 case 配对”，不是两个模型的统计检验。

```text
# 触发评测判分 — {target}

- runs: {runs}（TP {TP} / FP {FP} / FN {FN} / TN {TN}）
- precision {precision:.3f} / recall {recall:.3f} / **F1 {F1:.3f}**
- 兄弟混淆率: {confusion:.3f}（{sibling_confused}/{sibling_total}）

| case | expected | selected | 判定 |
|---|---|---|---|
{每个匹配结果的一行}

> 本报告只给原始配对计数与比率；统计非劣需预注册界值 + McNemar/配对 Bootstrap（§10.3），不在此自动宣布。
```

每行是 `| {结果case_id}#r{run或缺省1} | {case.expected} | {selected_skill或缺省none} | {判定} |`。结果顺序不排序；重复标签重复输出。无匹配行时表只有两行表头，接一个空行和结尾引用，文件最后有换行。结尾 `§10.3` 是固定历史文案，本套件不要求查阅其他文档，也不提供该统计检验。

字符串原文嵌入，不作 Markdown 转义、换行清洗、slug 正规化或 HTML 过滤。case_id、expected、selected、target 含 `|`、换行等会原样影响表格。JSON 非字符串值以 Python 风格展示：null→`None`，true→`True`，false→`False`；数值为通常十进制（浮点整数带 `.0`）；容器使用方括号/花括号表示，内部字符串以带引号的转义表示，元素以逗号加空格、键值以冒号加空格分隔。这是文本兼容要求，不要求以 Python 实现。常规字符串之外的浮点展示采用最短可往返 binary64 表示；指数绝对值至少两位，指数为正带 `+`，科学计数使用小写 `e`；绝对值小于 1e-4（非零）或不小于 1e16 时使用科学计数。NaN/无穷展示为 `nan`/`inf`/`-inf`。

最终报告完全形成后才递归创建报告父目录并覆盖写入；然后 stdout 打印完整报告。读取失败、解析失败或匹配/计算错误时不覆盖旧报告。写入非事务，见 CONTRACT 的失败恢复表。
