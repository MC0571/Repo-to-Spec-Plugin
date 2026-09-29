# 触发评测判分 — T

- runs: 16（TP 1 / FP 15 / FN 0 / TN 0）
- precision 0.062 / recall 1.000 / **F1 0.118**
- 兄弟混淆率: 0.000（0/0）

| case | expected | selected | 判定 |
|---|---|---|---|
| a#r1 | should_trigger | T | TP |
| b#r1 | edge_case | T | FP |
| b#r1 | edge_case | T | FP |
| b#r1 | edge_case | T | FP |
| b#r1 | edge_case | T | FP |
| b#r1 | edge_case | T | FP |
| b#r1 | edge_case | T | FP |
| b#r1 | edge_case | T | FP |
| b#r1 | edge_case | T | FP |
| b#r1 | edge_case | T | FP |
| b#r1 | edge_case | T | FP |
| b#r1 | edge_case | T | FP |
| b#r1 | edge_case | T | FP |
| b#r1 | edge_case | T | FP |
| b#r1 | edge_case | T | FP |
| b#r1 | edge_case | T | FP |

> 本报告只给原始配对计数与比率；统计非劣需预注册界值 + McNemar/配对 Bootstrap（§10.3），不在此自动宣布。
