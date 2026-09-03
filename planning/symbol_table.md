# Global Symbol Table

| Symbol | Plain name | Type | Domain / unit | Scope | Source / note |
|---|---|---|---|---|---|
| \(p_0\) | Nominal component defect rate | input parameter | \([0,1]\), proportion | Q1, Q4 | Q1; numerical instance \(p_0=0.10\). |
| \(p\) | True defect rate of the sampled supplier batch | parameter | \([0,1]\), proportion | Q1 | Q1. |
| \(X_t\) | Defective-count observation among the first \(t\) inspected components | random variable | \(\{0,\ldots,t\}\), items | Q1 | Defined for a possible sequential rule; no distributional assumption is yet human-confirmed. |
| \(\tau\) | Inspection stopping time | decision / random variable | positive integer, inspections | Q1 | Q1's explicit minimization target under the human's chosen sequential interpretation. |
| \(d\) | Batch decision | output decision | \(\{\mathrm{accept},\mathrm{reject},\mathrm{inconclusive}\}\) | Q1 | `inconclusive` is only a candidate terminal action pending the next framing decision. |
| \(p_i\) | Defect rate of component or product node \(i\) | input / estimated parameter | \([0,1]\), proportion | Q2--Q4 | Given in Q2/Q3; sampling-derived in Q4. |
| \(c_i^{buy},c_i^{ins},c_i^{asm},c_i^{dis}\) | Purchase, inspection, assembly, and disassembly cost | input parameter | yuan/item | Q2--Q4 | Use only where the table supplies the corresponding cost. |
| \(s\) | Market selling price | input parameter | yuan/item | Q2, Q3 | Table 1/2. |
| \(\ell\) | Exchange loss excluding replacement item | input parameter | yuan/item | Q2, Q3 | Appendix definition. |
| \(a_i\) | Inspection action at node \(i\) | decision | \(\{0,1\}\) | Q2--Q4 | 1 means inspect. |
| \(b_i\) | Disassembly action for a detected/returned defective node \(i\) | decision | \(\{0,1\}\) | Q2--Q4 | 1 means disassemble; the reuse transition convention is unresolved. |
| \(G=(V,E)\) | Assembly directed acyclic graph | input structure | graph | Q3, Q4 | Figure 1 gives the provided instance. |
