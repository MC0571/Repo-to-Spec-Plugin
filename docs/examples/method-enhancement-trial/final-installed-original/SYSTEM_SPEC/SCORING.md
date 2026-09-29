# 判分与报告

## S1 配对与分类

初始 TP、FP、FN、TN、兄弟总数 B、兄弟混淆数 C 均为 0。按 results 原始行顺序逐条处理，以 result.case_id 查询最后覆盖生效的 suite case。找不到则直接跳过，不生成行、不计入任何分类；results 总行数 N 仍包含它。匹配成功后，令 s 为 selected_skill（缺失为字符串 `none`），t 为 target，e 为 expected。相等采用 VALUE_SEMANTICS。

| 条件，按此先后判定 | 分类文案 | 计数变化 |
|---|---|---|
| e 等于字符串 `should_trigger` 且 s=t | `TP` | TP+1 |
| e 等于字符串 `should_trigger` 且 s≠t | `FN` | FN+1 |
| e 等于字符串 `should_not_trigger` 或 `edge_case`，且 s=t | `FP` | FP+1 |
| e 等于字符串 `should_not_trigger` 或 `edge_case`，且 s≠t | `TN` | TN+1 |
| 其余 e，且 s=t | `混淆(FP)` | B+1，C+1，FP+1 |
| 其余 e，且 s≠t 且 s=sibling_target（缺失为 null） | `OK` | B+1，TN+1 |
| 其余 e，且 s≠t 且 s≠sibling_target | `未中兄弟({D(s)})` | B+1，TN+1 |

“其余”包括字符串 `sibling`、未知字符串、null、数字、布尔、数组、对象。兄弟目标等于本次 target 时，选中它仍优先判混淆(FP)。错误选择其他非目标技能不会增加 FN 或 FP；不能把 `OK` 与 `TN` 混同为兄弟选择全部正确。

每条结果独立贡献一次；重复 `(case_id,run)` 不合并。suite 中同键 case 只采用最后一份；实际行仍显示 result 自身 case_id，而非套件中最后一份 case_id 的表示。缺失 case 的结果既不产生错误诊断也不补行。

## S2 数值

- P = TP / (TP+FP)，分母为 0 时为 0.0。
- R = TP / (TP+FN)，分母为 0 时为 0.0。
- F = 2×P×R / (P+R)，P+R 为 0 时为 0.0。
- Q = C/B，B 为 0 时为 0.0。

使用 binary64 逐步运算：先计算 P、R，再按左结合 `(2*P)*R` 除以 `P+R`，不先对 P、R 截断或四舍五入，也不改用整数化简公式。P/R/F/Q 显示为定点小数 3 位，按该二进制浮点数的准确值取最近十进制值，恰好中点取末位偶数；始终保留三位及前导 `0`。不依赖 locale，不使用百分号、千位分隔符或小数逗号。计数为普通十进制整数。

匹配行数 = TP+FP+FN+TN ≤ N；兄弟两种非目标分支都计入 TN，但 TN 不出现在 P/R/F 分母中。没有总准确率、置信区间、分组汇总、逐 case 多数投票或通过结论。

## S3 唯一文本模板

以下 `{...}` 是插值占位符，不是输出中的花括号。所有固定字符、空格、全角括号、破折号、大小写、行顺序及空行必须保留。`D` 在 VALUE_SEMANTICS 中定义。

```text
# 触发评测判分 — {D(target)}

- runs: {N}（TP {TP} / FP {FP} / FN {FN} / TN {TN}）
- precision {P:.3f} / recall {R:.3f} / **F1 {F:.3f}**
- 兄弟混淆率: {Q:.3f}（{C}/{B}）

| case | expected | selected | 判定 |
|---|---|---|---|
{零行或多行配对行}

> 本报告只给原始配对计数与比率；统计非劣需预注册界值 + McNemar/配对 Bootstrap（§10.3），不在此自动宣布。
```

配对行严格为：

```text
| {D(result.case_id)}#r{D(result.run，缺失为整数1)} | {D(expected)} | {D(selected_skill，缺失为字符串none)} | {分类文案} |
```

构造方式消除空行歧义：先写标题加两个 LF；写三个统计行，各以 LF 结束；再写一个 LF；将表头、分隔行、全部配对行用单个 LF 连接；追加两个 LF，再追加固定引用段，最后追加一个 LF。零配对行时分隔行后直接两个 LF 接引用段，不放占位行。磁盘文件仅含此 report；stdout 为 report 加一个 LF，不输出路径、进度、警告或成功摘要。

标题或单元格中的字符串直接插入，包含 `|`、换行、回车、反引号、HTML 或 Unicode 空白时也不转义、不裁剪、不规范化；因此合法输入可能产生不美观或列错位的 Markdown，仍须保留原始文本。文件扩展名无需为 `.md`，不会决定输出格式。结尾 `§10.3` 是固定文字，不是实施所需外部文档。
