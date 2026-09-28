# 验收场景

在支持的 POSIX 环境运行目标命令；每项使用独立临时目录，除特别说明，目录树在执行期间稳定、可读。不需要任何来源项目文件。测试应断言退出码、诊断 code/级别/目标、计数及只读性，不断言对齐空格。规范的 runtime 处理是目标要求，不声称已有工具通过这些验收。

公共夹具 G：`good/SKILL.md` 为以下 UTF-8 内容，最后一行 `---` 后有一个 LF，共 40 字节、5 行。

```yaml
---
name: good
description: example
---
```

| ID / 规则 | 输入、动作 | 预期 |
| --- | --- | --- |
| A01 R1–R4,C1–C2 | 只放 G，执行包根 | 0；M=1,S=1,E=0,W=0；概览 good/5/40，stderr 空 |
| A02 R1,C1 | 无参数；不存在目录；用普通文件当目录（分别运行） | 无参数退出2且用法，无扫描；另两种退出1、一个 input，M=S=0 |
| A03 R1,R4 | 空目录；只有 `note.md` 空文本 | 分别0且M/S为0/0、1/0，无概览，无元数据要求 |
| A04 R1,R4 | G 的根参数传两次；或根与其 good 子目录一起传 | 均0，M=2,S=2，两个概览；不去重 |
| A05 R1 | good 中添加 `skill.md`（无元数据）和 `UPPER.MD`（坏链接） | 前者仅做引用；后者不扫描；M=2,S=1，0 |
| A06 R1 | G 根下隐藏目录 `.hidden/n.md` 放 `[x](missing)` | 1，一个 broken-ref，M=2,S=1；隐藏项不忽略 |
| A07 R1 | SKILL.md 仅字节 FF | 1，M=1,S=0，一个 encoding，无概览和其他检查 |
| A08 R2 | G 前加 UTF-8 BOM；或删结束分隔；或 YAML 换成序列（分别运行） | 各1，S=1，一个 frontmatter，仍有概览 |
| A09 R2 | YAML 换为 `name: 1`、`description: false` | 1，两个 frontmatter，先 name 再 description，无命名 WARN |
| A10 R2 | name 为 `" "`、description 为 `""`；另测缺少两个键 | 各两个 frontmatter；原始字符串 trim 后须非空 |
| A11 R2 | G name 改为 `Bad_Name` | 0，name-style 和 name-dir 两个 WARN，E=0 |
| A12 R2 | G name 改为 `good-` | 0，只有 name-dir；尾部连字符不触发风格警告 |
| A13 R2 | G name 改成 YAML 双引号转义值 `"good\n"` | 0，仅 name-dir，因正则末尾 LF 语义没有 name-style |
| A14 R2 | `---name: good` 开始、`---suffix` 结束，description 保持 | 0，无 WARN；不强制分隔符独占整行 |
| A15 R2 | 多余字段、重复 name（先 wrong 后 good）、多行 description | 0，末 name 生效，多余字段忽略；另测未知 YAML tag 得一个 frontmatter |
| A16 R3 | G 追加 `[a](gone.md#x) [b](gone.md#y)` 及两次 `references/no.md` | 1，两个 broken-ref，目标 gone.md 与 references/no.md |
| A17 R3 | G 追加 `[a](references/a.md#missing)`；创建该文件 | 0，M=2,S=1；锚点不存在不影响结果 |
| A18 R3 | G 追加 http/https/mailto/绝对路径/纯 fragment 链接 | 0，不访问网络或绝对路径目标 |
| A19 R3 | G 追加带标题链接、含空格链接和引用式链接，目标均不存在 | 0；按 RULES 表格使用普通目标名，不混入独立裸路径 |
| A20 R3 | G 追加代码块内 `[x](code.md)`、图片 `![x](img.png)`、ftp 链接 | 1，三个 broken-ref，代码不被排除 |
| A21 R3 | G 追加 `assets/a.png references/a.md scripts/a.py foo/references/a.md (references/a.md)` | 1，只有前两个裸路径诊断 |
| A22 R3 | G 追加 `[a](a%20b.md) [b](a.md?q=1) [c](HTTPS://host/a)` | 无对应字面文件时3个 broken-ref，不解码、不访问网络 |
| A23 R3 | G 追加 `[a](../shared.txt) [b](references)`，包根有 shared.txt，good 有 references 目录 | 0，父路径与目录目标允许；删 shared.txt 后1 |
| A24 R3 | G 追加 `[a](a.md) [b](./a.md)`，二者均不存在 | 1，两个 broken-ref；不按解析路径去重 |
| A25 R1,R4 | G 每个 LF 替换为 CRLF，再单独替换为 CR（分别运行） | 均0，概览仍5行40字节；磁盘字节不作为统计值 |
| A26 R1,R3 | 文件别名 link.md 指向根外普通 Markdown，其中含相对引用；引用只在真实目标父目录存在 | 以 link.md 的父目录检查，broken-ref；根内目录链接指向坏包时不遍历 |
| A27 C1,C3 | 一个失效的 `.md` 文件链接；或不可读 `.md`；或不可枚举子目录 | 1，stderr runtime，无正常结果行；权限测试用非特权进程 |
| A28 R1,C4 | 名为 a.md 的目录或 FIFO | 1，不阻塞读取；明确非普通文件错误 |
| A29 C1,C3 | 大目录扫描中 SIGINT；宿主杀进程/超时分别测试 | SIGINT 尽力130及取消反馈；其他由宿主判未完成，均不能接受部分 stdout 为通过 |
| A30 C3–C4 | 运行前后比较输入的路径、内容哈希、模式、修改时间；包中放会写 marker 的脚本但不引用执行 | 无内容/模式/mtime 变化，无 marker、缓存、锁或报告文件；允许 atime 变化 |
| A31 C4 | 稳定目录重复运行及同时启动两进程 | 每次同结果，各自计数独立，无累加、无写入冲突 |
| A32 C1,C3 | 若实现依赖外部 YAML 运行库，移除该依赖；内置解析器的实现不适用本场景 | 1，runtime，未联网/安装，未扫描 |
| A33 C3–C4 | 在读取时删除文件或撤销权限，受控让读取失败 | 1、无正常结果；不声称能发现所有不报错的并发修改 |
| A34 R1,C1 | 第一个根不存在，第二个根为 G | 1，M=1,S=1，一个 input，仍输出 G 概览 |
| A35 C2 | 混合命名 WARN 和 broken-ref ERROR | 概览→总数→全部 WARN→全部 ERROR→结果，1；code、路径及目标足以定位 |

发布集成验收：退出1/2/130或其他异常退出均不能当预检查通过；0不自动发布，空目录和仅 WARN 的0均交给既有发布策略。检查完成之后发布产品修改包时，必须重新检查。不得要求用户持有编译状态、Registry 条目或来源仓库才能运行以上场景。
