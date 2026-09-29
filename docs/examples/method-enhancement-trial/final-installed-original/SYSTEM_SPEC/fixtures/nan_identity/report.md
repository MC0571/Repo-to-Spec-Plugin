# 触发评测判分 — [nan]

- runs: 2（TP 1 / FP 0 / FN 0 / TN 1）
- precision 1.000 / recall 1.000 / **F1 1.000**
- 兄弟混淆率: 0.000（0/1）

| case | expected | selected | 判定 |
|---|---|---|---|
| nan#r1 | should_trigger | [nan] | TP |
| scalar#r1 | sibling | nan | 未中兄弟(nan) |

> 本报告只给原始配对计数与比率；统计非劣需预注册界值 + McNemar/配对 Bootstrap（§10.3），不在此自动宣布。
