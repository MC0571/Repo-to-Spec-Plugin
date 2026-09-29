# 评测规则

## S-1 用例与结果

一套 suite 评估一个目标选择 ID。输入为 UTF-8 JSON 对象：

| 字段 | 语义与默认 |
| --- | --- |
| schema_version | 必填，值为 1 |
| suite_id | 必填字符串，标识一套用例 |
| target | 必填字符串，实际选择结果中的目标 Skill/入口 ID |
| split_seed | 整数，缺省 42 |
| train_ratio | 数值，缺省 0.6 |
| trigger_cases | 非空数组，保留输入顺序 |
| case_id | 每例必填字符串 |
| prompt | 每例必填字符串，原文送给选择器 |
| expected | 必填，should_trigger / should_not_trigger / sibling / edge_case |
| sibling_target | sibling 时应选的兄弟 ID；来源 schema 没强制必填，真实评测按 R-1 强制 |
| runs | 每例整数，缺省 3；探索粗筛可显式用 1，不能冒充正式评测 |

suite 可含 output_cases 或其他字段，本能力不执行输出评测；不把其中断言送给选择器。来源 schema 对 train_ratio 未限定区间、对 runs 未限定正值、对 case_id 未要求唯一；来源命令也不自动调用 schema 校验。真实评测的输入有效域见 R-1。

原始结果为 UTF-8 JSONL，每个非空行一个对象：`{"case_id":"p","run":1,"selected_skill":"A"}`。selected_skill 是一个精确匹配、区分大小写的 ID，或字符串 `none`，不是多选列表。reason 可作受控诊断，但不参与来源评分。一次运行记录不等于一条用例：默认每例有 3 条独立运行记录。

旧式 `test_cases` 格式中的 id/type/expected_behavior 与这里不是同一接口，不能直接送入。迁移时须人工或受审核转换，把应选兄弟明确为 sibling，把边界意图明确为是否不选目标；旧式 edge 的自然语言理由不能无条件映射为本格式的负例。

## S-2 固定切分

复制 trigger_cases，按 split_seed 的确定性随机排列重排。来源兼容结果使用 Python 3 的 `Random(integer_seed).shuffle` 排列语义，然后计算 `k = round(n × train_ratio)`，round 为最近整数、恰好一半取偶数；前 k 条 train，其余 validation。没有按类别分层，不保证小集合两侧都有每种类别。all 是 train 接 validation，即重排后的顺序，不是原输入顺序。

精确兼容实现须复现该排列与舍入；可用不同语言的兼容算法或持久化相同切分清单，不能只声称“同 seed”而换成不同排列。验收给定 5 条按 p,n,e,s,q 顺序输入，seed 42、ratio 0.6 时 train 为 s,n,e，validation 为 q,p。相同输入与配置多次切分一致；用例内容或顺序变化须重新标识版本。

来源 split 输出包含 suite_id、seed、train ID 数组、validation ID 数组。该清单不隐藏验证集身份，更不构成权限隔离；R-3 负责盲测。

## S-3 准备与真实盲测要求

prepare 默认选 train，可显式选 validation/all；每例生成一个任务包，而不是每次重复各一个文件。任务包包含 case_id、runs、prompt、instruction、installed_skills。instruction 要求未参与制作的干净 agent 选择一个 Skill 或 none，输出 selected_skill 与 reason，每次独立且重复之间不携带记忆。不包含 expected、sibling_target、notes 或通过标准。

来源命令只把逗号分隔的 skills 字符串列表原样写为 installed_skills，不读取目录、不解析 name/description、不安装 Skill、不检查列表是否真的存在，也不生成真实结果。实际盲测必须具备 Skill 路径或内容，并提供整包所有候选的 name + description 来检测竞争；只传 slug 列表不足以证明真实宿主加载行为。目标的实际展示内容、顺序及选择调用由 U-1/U-2 核实。

测试应有正例、诱饵、边界，诱饵中至少一条应由兄弟 Skill 接手；晋级入口需包含应由来源路由入口接手的近邻负例（仅目标存在该结构时适用）。来源方法建议每 Skill 3–5 正例、2–3 诱饵、1–3 边界；这是用例设计指导，不是目标包的准入数值。正式查询至少 3 次，粗筛 1 次仅作探索。缺少诱饵的材料不具备来源方法声称的充分性。

只能在训练集调优。选版前保持 validation 隐藏；版本候选冻结后才做选择评估。看过失败用例再调优后，这些用例转回归材料，不能继续称为未见保留集。修改答案需独立理由和审计，不得为通过改答案。来源允许资源不足时主流程降级自测并标低可信度；本次目标为真实评测，降级结果只能作诊断，不能冒充真实选择运行。

## S-4 来源计数的精确定义

逐运行计数，不投票、不按 case 平均。triggered 表示 selected_skill 等于 suite.target。

| expected | 选择 | 原始判定 | 计数 |
| --- | --- | --- | --- |
| should_trigger | target | TP | TP +1 |
| should_trigger | 其他/none | FN | FN +1 |
| should_not_trigger 或 edge_case | target | FP | FP +1 |
| should_not_trigger 或 edge_case | 其他/none | TN | TN +1 |
| sibling | target | 混淆(FP) | FP +1，sibling_confused +1 |
| sibling | sibling_target | OK | TN +1 |
| sibling | 其他/none | 未中兄弟(selected) | TN +1 |

每个 sibling 结果均给 sibling_total 加 1。兄弟选错仍计 TN 是“没有误选当前目标”的二分类语义，不表示选对了兄弟。R-2 必须另行表示逐例是否匹配，保留两种结论。

precision = TP/(TP+FP)，recall = TP/(TP+FN)，F1 = 2×precision×recall/(precision+recall)，兄弟混淆率 = sibling_confused/sibling_total。任何分母为零时该指标为 0.0。展示固定三位小数；比较或存储用原始计数与未舍入值，不能用展示字符串判门槛。

报告包括 target、runs、TP/FP/FN/TN、precision/recall/F1、兄弟混淆分子分母及比率、逐行 case_id#rN / expected / selected / 判定。声明这些是计数与比率，不自动宣称统计非劣；非劣需要另行预注册界值、样本量和配对统计方法。本能力没有该检验。

## S-5 来源宽松处理与限制

以下行为用于恢复和兼容测试，不能作为真实门禁完整性契约：

- score 以整个 suite 查找结果，不接受 set 参数，也不核对是否按 train/validation 提交。
- 未知 case_id 被静默跳过，但仍计入报告头 runs；runs 是结果非空行数，可能大于混淆矩阵总数。
- 重复行逐条累计，run 不参与唯一性检查；缺 run 显示 1，缺 selected_skill 当 none。
- 缺失运行不会生成失败行，也不入任何分母；空结果仍输出零值报告。
- suite 重复 case_id 时后者覆盖前者供判分；非法 expected 落到 sibling 分支。null 不等于缺字段，不能默认成 none。
- 只要成功生成报告就退出 0，任意低分也一样；没有阈值、通过状态或发布动作。

真实评测走 R-1/R-2 的校验和计划集合检查；非法数据可以留作审计，但不得伪装为 completed。

## S-6 来源命令交互与文件副作用

这是来源兼容入口说明；目标可使用等价库或服务接口，不要求沿用命令名。

| 操作 | 参数与输出 | 状态 |
| --- | --- | --- |
| split suite.json | 写同路径改后缀的 suite.split.json；stdout 打印 train/validation 数及路径 | 成功退出 0 |
| prepare suite.json --skills A,B --out dir [--set train\|validation\|all] | 创建目录，写 case_id.json 和 README.md；stdout 打印用例数及目录 | 成功退出 0 |
| score suite.json --results results.jsonl --out report.md | 自动建报告父目录，写 Markdown 并全文打印 stdout | 写成即退出 0 |

相对路径基于工作目录，UTF-8；写入覆盖已有同名文件，prepare 不清理旧文件。split/prepare/score 无事务或恢复日志；中断和写入错误可能留下部分文件或旧报告。参数错误由解析器报 stderr 并非零退出；读写、JSON 和必要字段错误可直接异常终止，无稳定错误结构。来源 CLI 没有超时或取消协议，无自动重试。恢复需修复输入并在新输出目录整轮执行，不用旧报告存在性认定完成。安全实现不将 case_id 当任意文件路径（R-1）。
