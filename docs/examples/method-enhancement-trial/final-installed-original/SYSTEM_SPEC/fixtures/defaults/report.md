# 触发评测判分 — none

- runs: 4（TP 1 / FP 1 / FN 0 / TN 2）
- precision 0.500 / recall 1.000 / **F1 0.667**
- 兄弟混淆率: 0.333（1/3）

| case | expected | selected | 判定 |
|---|---|---|---|
| a#r1 | should_trigger | none | TP |
| b#r1 | sibling | none | 混淆(FP) |
| b#r1 | sibling | None | OK |
| b#r1 | sibling | null | 未中兄弟(null) |

> 本报告只给原始配对计数与比率；统计非劣需预注册界值 + McNemar/配对 Bootstrap（§10.3），不在此自动宣布。
