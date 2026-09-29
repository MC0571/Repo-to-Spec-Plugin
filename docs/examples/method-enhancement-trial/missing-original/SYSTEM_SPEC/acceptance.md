# 验收

本章为实现者的验收契约，不表示目标实现已经执行通过。A-1 至 A-8 可不依赖真实宿主验证；A-9 至 A-14 的目标集成验证受未决项约束。

| ID | 输入/动作 | 应观察到的结果 | 规则 |
| --- | --- | --- | --- |
| A-1 数据有效域 | 缺必填字段、重复 case_id、runs=0、ratio 越界、sibling 缺目标、候选重复或含保留 none | 真实运行 input_invalid，无选择调用；来源兼容模式的宽松性不得渗透正式模式 | S-1、R-1 |
| A-2 切分 | 顺序 p,n,e,s,q，seed=42，ratio=0.6，重复执行 | train=[s,n,e]，validation=[q,p]；all=[s,n,e,q,p]；n=5、ratio=0.5 时 k=2 而非 3 | S-2 |
| A-3 准备 | suite 含 expected、notes、sibling_target；prepare 默认与 validation/all 各执行 | 默认仅 train；每例一个包，runs 缺省 3；包内无答案。仅完成 prepare 不能声称选择已执行。目标模型输入还应去除可能泄漏答案的 case ID | S-3、R-3 |
| A-4 评分所有分支 | 使用下方向量 | 精确复现 TP/FP/FN/TN、兄弟分子分母和三位显示；C 误选兄弟为原始 TN 且 expected_match=false | S-4、R-2 |
| A-5 缺失/未知/重复 | 计划 p 跑 3 次，只提交 p#1=A；追加未知 case；重复 p#1 | 来源可给 F1=1 且退出 0，未知行只增头部 runs；正式模式缺失/未知/重复均不能 completed，分母计划不缩水 | S-5、R-2 |
| A-6 空、缺字段与异常 | 空结果、缺 selected_skill、坏 JSONL、不可读输入、不可写报告 | 来源空结果写零值且退出 0；缺 selected 当 none；坏 JSON/IO 非正常完成。正式模式空结果为缺失，缺字段为 invalid，不能把错误当 none | S-5/S-6、R-2/R-4 |
| A-7 恢复与并发 | 完成部分运行后中断；迟到旧结果；同 attempt 重送；两个不同结果占同槽 | incomplete；新轮 ID，旧结果不入新轮；同内容传输幂等，冲突不可选优。取消先 cancelling 后确认 cancelled，无最终完整报告 | R-2/R-4 |
| A-8 文件边界 | case_id 含 ../；复用含旧包目录；写报告中断 | 目标只用安全内部文件名；旧文件不增计划；临时/旧报告不作为本轮完成；来源 prepare 不清理的行为仅作兼容诊断 | S-6、R-1/R-5 |
| A-9 环境有效性 | 完整报告后，分别改包、候选顺序/描述/内容、suite、切分、模型、权限、预算、评分规则 | 每次变化均不能凭原报告直接作本次决定；U-4 的复用政策未定前不签发允许。修改策略使旧决定失效但不改观测历史 | R-5、U-2/U-4 |
| A-10 真实选择边界 | 通过目标实际入口完成选择 target、兄弟、none；制造错误/超时/多选；监测任务副作用 | 单选结果精确归集；错误不是 none；各次上下文独立；无实际 Skill 任务执行。若无法实现，U-1 保持未闭合 | R-3、U-1 |
| A-11 完成提交 | 结果齐全且有效，评分时模拟写入中断；再正常提交 | 中断无完成标记；正常提交后报告计数一致且不可变；completed 仍不代表准入允许 | R-4/R-5 |
| A-12 保留集与权限 | 调优者尝试读保留任务、预期、日志和逐例报告；管理员披露失败用于修复 | 前者无权；披露后 exposure=exposed，转回归，不能再用作未见验收；真实执行者看不到答案/阈值 | R-3/R-6、U-5 |
| A-13 策略边界 | 待 U-3 确定后，造每指标阈值上/等于/下、兄弟错但 F1 高、类别缺失、重复意见分歧、重要负例失败 | 按同一预注册政策给出唯一结果，不能仅凭三位显示或均分；目前只输出指标/mismatch/decision=not_evaluated，不预填应通过值 | U-3 |
| A-14 包级端到端 | 待 U-4 确定后，多个目标完整、一个未测、一个不合格、报告失效、发布请求重复/超时、无策略 | 必须依具体目标政策观察最终发布动作、无结论处置和回执；单目标成功不可冒充整包准入；当前不得宣称本项通过 | U-4 |

## A-4 完整计数向量

target=A，候选 A/B/C。用例 p 为 should_trigger、n 为 should_not_trigger、e 为 edge_case、s 为 sibling 且 sibling_target=B、q 为 should_trigger。以下 7 行是计数单元测试输入，不是默认每例 3 次的完整真实运行：

| case/run | selected | 原始判定 | expected_match |
| --- | --- | --- | --- |
| p/1 | A | TP | true |
| n/1 | A | FP | false |
| e/1 | none | TN | true |
| s/1 | A | 混淆(FP) | false |
| s/2 | B | OK，TN | true |
| s/3 | C | 未中兄弟(C)，TN | false |
| q/1 | none | FN | false |

预期 TP=1、FP=2、FN=1、TN=3；precision=1/3 → 0.333，recall=1/2 → 0.500，F1=0.4 → 0.400，兄弟混淆=1/3 → 0.333。再加一行 unknown/1=A，来源头 runs=8，逐行表仍 7 行，矩阵不变；真实归集记 unexpected，不能 completed。

单独用 s/1=none：原始 TN=1、兄弟混淆率 0.000，但 expected_match=false。单独正例选 none：FN=1，precision/recall/F1 均 0.000。单独负例选 B：TN=1，所有指标 0.000；零分母不是缺省通过。来源 missing_selected 的负例当 none/TN；正式输入必须判 invalid。

## 人类反馈检查

正常流程能看到准备范围、计划运行数、进行中的有效数量、完成后的计数和诊断。不完整或依赖缺失必须先呈现状态/原因/可恢复动作，不让高 F1 掩盖未完成。用户能辨认 synthetic、fallback 与 real_selector。对训练集展示逐例修复线索，对保留集遵守角色可见性；UI 实现可自由，但不能扩大信息权限。
