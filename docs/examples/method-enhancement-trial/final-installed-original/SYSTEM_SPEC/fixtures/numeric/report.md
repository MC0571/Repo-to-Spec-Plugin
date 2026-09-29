# 触发评测判分 — True

- runs: 4（TP 0 / FP 1 / FN 0 / TN 3）
- precision 0.000 / recall 0.000 / **F1 0.000**
- 兄弟混淆率: 0.000（0/3）

| case | expected | selected | 判定 |
|---|---|---|---|
| True#r-0.0 | edge_case | 1.0 | FP |
| float#r1e-05 | sibling | 1e+20 | 未中兄弟(1e+20) |
| float#r1e+16 | sibling | 0.0001 | 未中兄弟(0.0001) |
| float#r1.2345678901234567 | sibling | 1000000000000000.0 | 未中兄弟(1000000000000000.0) |

> 本报告只给原始配对计数与比率；统计非劣需预注册界值 + McNemar/配对 Bootstrap（§10.3），不在此自动宣布。
