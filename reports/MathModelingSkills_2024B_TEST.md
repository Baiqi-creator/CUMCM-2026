# MathModeling-skills 独立能力测试：2024 CUMCM B 题

状态：已结束。本文只记录已实际执行的步骤和已产生的证据；未发生的建模、实验、论文或审计结果不预填。

## Gate 0 — 官方题面可读性

- 当前阶段 / Gate：`G0 blocked_missing_official_problem_text`，随后解除。
- 关键提示词：使用用户指定的官方赛题文件，校验 SHA256、读取 PDF、核验问题 1--4、表 1、表 2 和附录。
- Codex 实际完成：初次网络下载失败后未改用题解；发现本地文件实际位于 `workspace/problem/CUMCM2024_B.pdf`，校验 SHA256，解析两页文本并读取图 1。
- 关键结论：题面附件完整且可读；图 1 的 DAG 为 `(1,2,3)->S1`、`(4,5,6)->S2`、`(7,8)->S3`、`(S1,S2,S3)->成品`。
- 风险或问题：环境没有 Poppler/Python PDF 库，因而使用 PDF 内嵌文本和图像的本地解析；未改动原 PDF。
- 人工决定：提供本地 PDF 与 SHA256。
- 最终选择及理由：使用该本地文件；哈希匹配。
- 新文件：`planning/parse/problem_parse.json`、`planning/classification/problem_classification.json`、四个 `planning/manifests/Q*.json`。
- 本阶段评价：工作流对缺失官方材料保持了阻塞，未根据记忆补造题面；本地路径与 PDF 工具缺失需要额外排查。

## Gate 1 — Q1 主方向

- 当前阶段 / Gate：Q1 `G1`。
- 关键提示词：将“检测次数尽可能少”作为优化目标，选择序贯抽样主路线，并保留固定样本 exact-binomial baseline。
- Codex 实际完成：建立 Q1 目标、变量、统计边界风险及候选输出形式；未筛选或实现模型。
- 关键结论：固定样本与序贯抽样的“最少检测次数”含义不同，需人工确定。
- 风险或问题：题目未给出两类错误风险、无差异区或固定/序贯约定。
- 人工决定：选择 B，序贯抽样为主方向。
- 最终选择及理由：原题强调尽量少检测，希望降低实际/期望检测次数；固定样本 exact-binomial 保留为 baseline。
- 新文件：`methods/Q1/q1_decisions.jsonl`（首条记录）、`planning/symbol_table.md`、`planning/model_assumptions.md`。
- 本阶段评价：技能正确把算法选择前的目标解释保留给人工；尚未产生任何虚构数值。

## Gate 1 — Q1 边界与无差异区方向

- 当前阶段 / Gate：Q1 `G1`，边界和终止约定待继续框定。
- 关键提示词：不得任意指定 \(p_1\)、\(\delta\) 或最大样本量；将 \(\delta\) 与 Q2/Q3 的经济影响关联。
- Codex 实际完成：记录序贯复合假设在 \(p_0=0.10\) 处相接的停止风险；建立数据审计，明确题目缺少批量和抽样框。
- 关键结论：仅凭 95% 拒收与 90% 接收要求，不能唯一识别一个统一有限停止的二元序贯规则；经济敏感性可作为 \(\delta\) 的后续校准依据，但题目并未直接给出唯一值。
- 风险或问题：有限批次无放回与 Bernoulli 近似的统计保证尚未比较；没有实际样本路径或批次总量。
- 人工决定：选择 B，以 Q2/Q3 的经济损失敏感性校准 \(\delta\)。
- 最终选择及理由：避免任意数值，使 Q1 判定与生产决策价值一致。
- 新文件：`workspace/data/data_profile.json`、`workspace/data/data_report.md`、本报告。
- 本阶段评价：技能暴露了题目未给参数而非掩盖该缺口，并将其转换为可追溯的后续验证条件；尚未完成方法筛选。

## Accelerated evaluation — 方法筛选与 Q2 实运行

- 当前阶段 / Gate：用户明确授权跳过低影响 framing；正常 G2.5 未被伪称为通过。
- 关键提示词：Q1--Q4 完成方法筛选；至少一个问题用真实题目数据运行，保存结果并做验证。
- Codex 实际完成：为 Q1--Q4 建立 main/baseline 方法卡；将 Q2 表 1 转写为可追溯 JSON；枚举全部 \(2^4=16\) 个策略，以 18 状态 Bellman 线性系统计算每个策略每个情形的期望利润；运行、修正并复跑代码；执行代码审查。
- 关键结论：初次运行的拆解策略利润后来被最终审计修正（遗漏拆解成本）。修正后，Q2 的最优策略位序为“检零件1、检零件2、检成品、拆解”，六个情形依次为 `1101,1101,1101,1111,0100,0000`；相对 baseline `0000` 的利润改进依次为 2.194787、15.156250、8.449931、41.531250、4.629630、0 元/已履约客户需求。
- 风险或问题：首次运行发现 6 个含拆解但未充分检零件的策略出现非吸收复装循环，线性系统奇异。代码已将其保留为“无有限期望的无效策略”，没有删除或赋造数值。数值结论依赖方法卡中明确的“调换后必须继续履约、售价仅收一次”假设。
- 人工需要做出的决定：无；这是用户授权的 accelerated scope 内技术处理。Q1 的 \(\delta\)、批次大小和无放回抽样仍未被伪造为已知。
- 新文件：`workspace/data_clean/q2_table1.json`、`methods/Q{1,2,3,4}/*_method_card.md`、`code/Q2/q2_main.py`、`results/Q2/experiments/round1/`、`code/Q2/reviews/q2_python_review.json`。
- 本阶段评价：workflow 的数据契约、策略空间、风险探针、运行摘要与审查要求均产生了可检查文件；正常的人机选择 Gate 对快速测试有较高交互成本，需由用户显式授权才被绕过。

## 当前测试结论（范围：方法筛选 + Q2 数值实现）

1. 实际调用/遵循的能力：workflow orchestration、problem parser、classifier、decision logger、symbol/assumption register、data audit、method selection、code plan/generation/review 的工件契约。
2. workflow 确有约束：缺题面时阻塞；Q1 因边界、\(\delta\)、抽样框连续停在 Gate；代码生成前的正常 G2.5 仍被报告为未通过而非伪造。
3. parser/classifier 效果：准确抽取表、附录和 DAG，并显式暴露 Q1/Q4 与 Q2/Q3 的依赖；其代价是 PDF 工具缺失时需要额外本地解析。
4. 方法筛选：Q1 固定样本 baseline/序贯主方案，Q2 精确枚举+Markov reward，Q3 DAG-MDP，Q4 robust-confidence-set；未把未运行方案说成已验证。
5. 假设和风险：主动记录了 Q1 边界、有限总体、复用循环、调换收入计数等风险；Q2 奇异策略为实际发现。
6. 编造检查：无虚构数据或运行结果；所有数值来自表 1 JSON 和 `q2_main.py` 实际运行。Q1/Q3/Q4 未运行的结论均标为 conditional。
7. 代码可运行：Q2 脚本完成运行，审查 JSON 五项检查均 PASS。
8. 可追溯性：输入、代码、CSV、sanity metrics、run summary 和 review 均在工作区保存。
9. baseline/验证：baseline `0000` 已实际同表比较；完整枚举、Bellman 残差最大 \(2.84\times10^{-14}\)、转移质量超额为 0、零次品 sanity 的误差为 0 均已实际执行。
10. Gate 评价：常规 Gate 对高风险统计定义有效，但 Q1 连续细粒度 Gate 交互成本较高。
11. token/交互成本：重复读取技能规范、人工 framing 卡和大量 manifest/工件会显著增加成本。
12. 最有价值：题面解析、显式假设表、策略空间完整性、风险探针与可运行结果契约。
13. 比赛中可简化：探索期设 `speed + lean`，合并低影响 framing，单一决策账本，临近交稿再切换 submission 审计。
14. 建议配置：先 parser/data audit，人工只确认会改变答案的假设；主/基线各一个；每次运行强制保存输入、summary、sanity 和 review。
15. 最终结论：**推荐但需要调整**。证据是 Q2 真实运行发现并修复了非吸收策略风险且结果可追溯；但严格默认 Gate 和工件量对竞赛时间压力偏重。

## 队友使用指南（简短）

- 给 Codex：官方题面/附件、数据路径和哈希、禁止资料范围、期望语言与时间预算。
- 第一条提示词：要求“先读题、解析、列歧义和依赖，到第一个高影响 Gate 停止；不准编造数据”。
- 它会自动做：建立问题契约、数据清单、变量/依赖、候选主/基线和可追溯工件。
- 人必须判断：目标口径、经济/统计风险阈值、题面未给的关键假设、最终论文主张。
- 减少 Gate：用 `speed + lean`，只保留会改变结果的 Gate，并在提示词中明确授权技术性选择。
- 防幻觉：要求保存原始输入哈希、代码、run summary；未运行不得报告数值；每个结论链接到文件。
- 查真实性：重跑脚本，核对输入哈希/CSV/run summary/review，检查 sanity 与残差，而不是只读文字报告。
