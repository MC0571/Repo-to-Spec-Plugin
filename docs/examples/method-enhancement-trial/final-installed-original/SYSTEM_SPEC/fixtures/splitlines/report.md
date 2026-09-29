# 触发评测判分 — T

- runs: 2（TP 1 / FP 0 / FN 1 / TN 0）
- precision 1.000 / recall 0.500 / **F1 0.667**
- 兄弟混淆率: 0.000（0/0）

| case | expected | selected | 判定 |
|---|---|---|---|
| a#r1 | should_trigger | none | FN |
| a#r1 | should_trigger | T | TP |

> 本报告只给原始配对计数与比率；统计非劣需预注册界值 + McNemar/配对 Bootstrap（§10.3），不在此自动宣布。
