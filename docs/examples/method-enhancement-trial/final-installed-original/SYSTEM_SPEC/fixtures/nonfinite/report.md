# 触发评测判分 — nan

- runs: 2（TP 0 / FP 0 / FN 0 / TN 2）
- precision 0.000 / recall 0.000 / **F1 0.000**
- 兄弟混淆率: 0.000（0/2）

| case | expected | selected | 判定 |
|---|---|---|---|
| a#rinf | sibling | nan | 未中兄弟(nan) |
| a#rinf | sibling | -inf | 未中兄弟(-inf) |

> 本报告只给原始配对计数与比率；统计非劣需预注册界值 + McNemar/配对 Bootstrap（§10.3），不在此自动宣布。
