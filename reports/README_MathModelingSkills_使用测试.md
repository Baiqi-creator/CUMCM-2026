# MathModeling-skills 使用测试：队友 README

## 1. 这是什么

把数模工作拆成读题、数据审计、关键人工判断、方法筛选、代码实验、结果追溯和论文审计的工作流。它不能替代队员判断数学模型是否正确。

## 2. 本次测试

2024 CUMCM B 题。实际测试 PDF 读题、parser/classifier、决策账本、假设/符号表、数据审计、Q1--Q4 方法筛选、Q2 Python 枚举/Markov reward、baseline、sanity、审查和一致性审计。未完整求解或实验 Q1、Q3、Q4，未冻结数字或写论文。

## 3. 实际使用流程

`赛题与附件 → workflow-orchestrator → problem parser/classifier → 数据审计 → 人工关键 Gate → 方法筛选 → 实际代码 → 实验 → baseline / sanity / robustness → frozen numbers → 论文`

## 4. 我们实际观察到的优点

- 缺官方题面时会阻塞，未靠记忆编题；表格和 DAG 被解析为文件。
- Q1 的边界、抽样框和 \(\delta\) 缺失被列为风险。
- Q2 枚举 16 策略时发现非吸收循环；审计又发现并修复拆解成本漏计。
- 输入、脚本、CSV、sanity、run summary 和 review 均落盘，可重跑核对。

## 5. 实际发现的问题

- learning 模式 Gate 偏碎，交互可能过多；正式比赛应合并次级 Gate。
- workflow 有助真实性，但不能替代人工审查公式、状态和题意；本次漏计拆解成本就是证据。

## 6. 正式比赛推荐设置

探索期用 `speed + lean`，只在会改变结论的假设、目标口径、风险阈值和最终主张处停下；交稿前再切 submission 审计。

Codex 可自主：文件清点、数据字段审计、机械枚举、运行、残差/sanity、结果文件和一致性检查。队员必须确认：模型目标、题面歧义、关键概率/经济假设、主模型路线、最终解释与论文结论。

## 7. 推荐第一条提示词

```text
这是数模赛题。附件在 <路径>，原始数据只读，哈希为 <哈希>。禁止编造数据、结果和参考文献；先用 workflow-orchestrator、parser/classifier 和数据审计。只在会明显改变答案的重大建模决策处停止，其余技术选择记录为 MODEL ASSUMPTION。代码必须实际运行；保存输入、结果、run summary、sanity 和 review；每个数值必须能追溯到结果文件。
```

## 8. Gate 怎么回复

- “选 B：序贯抽样；固定样本规则保留作 baseline。理由：减少期望检测次数。”
- “采用拆解后无限期望递归；若策略不吸收，报告无效，不给有限利润。”
- “该成本口径会改变结论，先列两个解释和敏感性，再由我确认。”

## 9. 如何检查 Codex 有没有胡编

- 核对附件路径、哈希和原始数据是否未改。
- 每个结论查 CSV/JSON/run summary；未运行不得接受数值。
- 重跑脚本，检查输出；手算一个小情形或 Bellman 方程。
- 查策略空间规模、概率和、残差、边界条件和异常策略。

## 10. 本次测试实际产物

- `planning/parse/problem_parse.json`：题面契约；`methods/Q*/`：决策账本和方法卡。
- `workspace/data_clean/q2_table1.json`：表 1 输入；`code/Q2/q2_main.py`：Q2 求解器。
- `results/Q2/experiments/round1/`：CSV、sanity、run summary；`results/Q2/reports/scoped_consistency.json`：最终审计。
- `reports/MathModelingSkills_2024B_TEST.md`：测试记录。

## 11. 本次测试结论

**推荐但需要调整。** 它适合流程管理、数据审计、候选模型整理、代码实验、结果追踪和论文一致性；关键建模判断和最终数学正确性仍应由队员负责。
