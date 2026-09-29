# 触发评测判分 — T

- runs: 11（TP 1 / FP 3 / FN 1 / TN 5）
- precision 0.250 / recall 0.500 / **F1 0.333**
- 兄弟混淆率: 0.250（1/4）

| case | expected | selected | 判定 |
|---|---|---|---|
| p#r1 | should_trigger | T | TP |
| p#r1 | should_trigger | none | FN |
| n#r1 | should_not_trigger | T | FP |
| n#r1 | should_not_trigger | X | TN |
| e#r1 | edge_case | T | FP |
| e#r1 | edge_case | none | TN |
| s#r1 | sibling | T | 混淆(FP) |
| s#r1 | sibling | S | OK |
| s#r1 | sibling | X | 未中兄弟(X) |
| u#r1 | other | None | OK |

> 本报告只给原始配对计数与比率；统计非劣需预注册界值 + McNemar/配对 Bootstrap（§10.3），不在此自动宣布。
