# 触发评测判分 — {'x': [True, None]}

- runs: 4（TP 0 / FP 1 / FN 0 / TN 3）
- precision 0.000 / recall 0.000 / **F1 0.000**
- 兄弟混淆率: 0.250（1/4）

| case | expected | selected | 判定 |
|---|---|---|---|
| None#rNone | None | {'x': [True, None]} | 混淆(FP) |
| 1#r{'r': [False]} | 42 | ['x', False, None, {'a': "it's", 'b': 'a"b', 'c': 'both\'"', 'd': '\t\n\\\x01\xa0字'}] | 未中兄弟(['x', False, None, {'a': "it's", 'b': 'a"b', 'c': 'both\'"', 'd': '\t\n\\\x01\xa0字'}]) |
| raw|
字#r[1, 2] | sibling | ['x'] | OK |
| quote#rFalse | what | A|
B | 未中兄弟(A|
B) |

> 本报告只给原始配对计数与比率；统计非劣需预注册界值 + McNemar/配对 Bootstrap（§10.3），不在此自动宣布。
