# 验收场景

这些场景检验实现语义，不运行真实 Skill 选择器。所有文件放在一个独立临时目录；路径越界案例的解析结果也必须留在该临时目录。每次同时观察退出状态、stdout/stderr 和实际文件；不得把旧文件存在当作本次成功。

## A1 完整旅程与精确计分（C1–C4、R1–R4）

suite.json：

```json
{
  "suite_id": "S",
  "target": "T",
  "trigger_cases": [
    {"case_id":"0","prompt":"P0","expected":"should_trigger"},
    {"case_id":"1","prompt":"P1","expected":"should_not_trigger"},
    {"case_id":"2","prompt":"P2","expected":"edge_case"},
    {"case_id":"3","prompt":"P3","expected":"sibling","sibling_target":"B"},
    {"case_id":"4","prompt":"P4","expected":"weird"}
  ]
}
```

执行 split，退出 0；suite.split.json 为下列对象，按 C3 缩进输出：

```json
{"suite_id":"S","seed":42,"train":["3","1","2"],"validation":["4","0"]}
```

执行 `prepare suite.json --skills "T, B,,T" --out pack --set all`。退出 0，成功行条数 5；五包 prompt 对应 P0…P4，runs=3，installed_skills=`["T"," B","","T"]`，只有 C4 五个字段；4.json 不含 expected。README 标 all、5 条。修改 split 文件的 ID 不影响再次 prepare。

由外部提供 results.jsonl（没有 run 时表中都为 #r1）：

```jsonl
{"case_id":"0","selected_skill":"T"}
{"case_id":"0","selected_skill":"T"}
{"case_id":"0","selected_skill":"none"}
{"case_id":"1","selected_skill":"T"}
{"case_id":"2","selected_skill":"other"}
{"case_id":"3","selected_skill":"B"}
{"case_id":"3","selected_skill":"other"}
{"case_id":"3","selected_skill":"T"}
{"case_id":"4","selected_skill":null}
{"case_id":"unknown","selected_skill":"T"}
```

执行 `score suite.json --results results.jsonl --out report.md`，退出 0；runs=10，TP=2、FP=2、FN=1、TN=4；precision=0.500、recall=0.667、F1=0.571、兄弟混淆率=0.250（1/4）。表含 9 行，依次判定 TP、TP、FN、FP、TN、OK、未中兄弟(other)、混淆(FP)、OK；最后一条 unknown 无表行。第九行 selected 显示 None。stdout 与报告相同但多一个末尾换行。不输出通过/失败决定。

## A2 划分边界（S1–S4）

| 输入/操作 | 预期 |
|---|---|
| 初始 ID 0…9，依次使用 S4 六种 seed | 完整排列与 S4 一致，默认 6/4；负整数与其绝对值相同。 |
| A1，ratio=0.5 | train=[3,1]、validation=[2,4,0]（这里 ID 仍为字符串）；2.5 取偶数 2。 |
| A1，ratio=-0.4 | train=[3,1,2]、validation=[4,0]；不是空 train。 |
| A1，ratio=0、1、2、-2 | 分别 0/5、5/0、5/0、0/5。 |
| 单 case，缺省 ratio | 1/0；prepare validation 只写 README，0 条。 |
| 空 trigger_cases、suite_id=E | split 为两个空数组；prepare all 建目录写 0 条 README。 |
| ratio=null；seed=[] | 都退出 1；不产生新 split。即使空集，seed=[] 仍失败。 |
| seed=null | 接受，split.seed=null；不要求重复运行同一顺序。 |
| 相同整数 seed 重跑，修改 prompt/expected 但保持位置和 ID | split 完全相同。 |

## A3 包内容、默认及覆盖（C2、C4、C5）

1. 单 case 的 runs 分别缺失、0、-1、null、"x"：包中分别为 3、0、-1、null、"x"，每次仅一包，均不调用执行者。
2. suite 仅有 trigger_cases，case 仅有 case_id/prompt 仍能 prepare。加入 notes、expected、sibling_target、自定义答案字段后包仍只有五字段。skills 空字符串得到 `[""]`；空白/重复原样保留。
3. 两个相同 ID 的 case 使用不同 prompt，按 S 排列确定后写者；最终同名包为后写者，README 条数仍为 2。不因重复拒绝，也不追加后缀。
4. 先写入 out/stale.json，再 prepare 小集合；stale.json 保留。再 prepare validation，旧训练包仍留在同一目录，不视作此命令生成。
5. seed=0，原序 case 为 `{"case_id":"first","prompt":"ok"}`、`{"case_id":"bad"}`，set=all：排列不变，first.json 写成后因 bad 缺 prompt 退出 1。新 README 不出现；若原本已有 README，其内容不变。
6. 单 case ID=`../escaped`，out=`临时目录/pack`：产生 `临时目录/escaped.json`。ID=`nested/x` 会建子目录。已有同名文件直接覆盖。符号链接测试仅链接到临时目录内。
7. prompt、case_id 内带答案暗示仍原样保留；本能力只过滤字段，不承诺文本完全盲化。

## A4 评分异常与计数陷阱（C2、R1–R3）

以下均可用 target=T 与最少相应 case 构造；除明确错误外均退出 0。

| 输入 | 预期 |
|---|---|
| 空 results 或仅空白行，suite 有正例且 runs=3 | runs=0，全部计数/比率为零；无逐例行，仍有报告；不补三个 FN。 |
| 正例只收到一行 selected=T，suite.runs=3 | runs=1，TP=1、F1=1.000；缺两次不阻止成功。 |
| 同一个已知 case+run 两行 selected=T | 两行均判分；无去重/拒绝。 |
| 两个定义同 case_id，先 should_trigger 后 edge_case，结果选 T | 后定义有效，FP=1。反转定义次序则 TP=1。 |
| 未知 case，缺 selected_skill | runs+1，无表行，无分类；不报错。 |
| 正例缺 selected_skill；另一行显式 null | 均为 FN（target=T）；前者显示 none，后者 None。 |
| 兄弟 B，selected=other 或 none | TN，未中兄弟(other/none)；混淆分母各加 1，分子不加。 |
| 兄弟 target=T、sibling_target=T，selected=T | 混淆(FP)，不是 OK。 |
| expected=未知值/null，缺 sibling_target，selected=null | 进入兄弟分支，OK、TN；兄弟分母加 1。 |
| expected=edge_case，selected=T | FP，不是人工复核/不确定。 |
| run 缺失、null、0、-1、"abc" | 标签分别 #r1、#rNone、#r0、#r-1、#rabc；不改变计数。 |
| case 缺 expected 但没有对应结果 | 不访问该字段，不报错；一旦匹配到它则退出 1。 |
| suite 缺 target | score 退出 1；不会因空结果跳过 target。 |
| 结果缺 case_id，或结果为 null/数组，或 case_id 为数组/对象 | 退出 1，无本次新报告。 |
| JSONL 一条合法后跟坏 JSON | 全量解析失败，退出 1；没有部分新报告。 |
| 在 JSONL 加空白行 | runs 和报告不变。 |
| 结果 selected 不在技能清单、score 未提供 split/pack | 仍按比较评分，无清单/划分验证。 |
| selected 字符串包含竖线/换行 | 原样插入报告，不自动修复 Markdown。 |

## A5 操作故障与恢复（C1、C5、C6）

- 省略 --skills/--out/--results、非法 --set：退出 2，stderr 说明参数错误，无文件处理。--help 退出 0。
- suite 或 results 不存在、不可读、UTF-8 错误、JSON 语法错：退出 1，stderr 有错误类别/原因，无成功反馈。权限测试使用确实不可访问的运行身份，不以管理员读取成功代替该分支。
- 预先写旧 report，再输入坏 JSONL：旧报告完整保留。修复 JSONL 重跑覆盖为新报告，不从上次部分计数继续。
- 把 out 指向已有普通文件或不可写位置：写入失败，非零退出；已完成的其他文件按 C5 保留，无回滚承诺。恢复位置/权限后重跑。
- 在 prepare 部分写入时中断：允许留下部分包，没有完整事务保证；新目录重跑产生全套包。同目录重跑覆盖同名项但不删除多余项。
- split 输入名 a.v1.json 和 a：分别输出 a.v1.split.json 和 a.split.json；已有文件被覆盖。输出目录按需递归创建。

## A6 实施检查

交付实现时应在选定目标平台运行上述场景；不得仅验证一份正常报告。尤其检查随机序列、舍入、缺失/null、未知/重复/少行、兄弟错误仍 TN、非事务副作用。容许替换启动器、库、语言和错误堆栈文案，不容许替换计数规则、默认值、输出字段、集合顺序或退出类别。本套件是规格交付；不代表任何目标实现已经完成或通过这些测试。
