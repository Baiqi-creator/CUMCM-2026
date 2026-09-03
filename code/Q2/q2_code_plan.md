# Q2 Python code plan — round1

Accelerated-evaluation implementation authorized by `planning/accelerated_evaluation_override.md`; normal G2.5 is intentionally not claimed.

- Main M2: enumerate all sixteen binary policies `(inspect1, inspect2, inspect_product, disassemble)` and solve an 18-state absorbing Markov reward system exactly using Gaussian elimination.
- Baseline B2: policy `(0,0,0,0)` from the same solver.
- Input: `workspace/data_clean/q2_table1.json`, yuan/item and proportions.
- Outputs: all-policy table, best-vs-baseline table, sanity metrics, and run summary.
- Checks: transition-mass equals one, Bellman residual below `1e-9`, finite solution, and a zero-defect analytical sanity case.
