# Model Assumptions

This is an assumption register, not a final approval. Entries marked **human judgment pending** must be resolved before the affected method is screened as executable.

| ID | Statement | Scope / source | Modeling need | Human-confirmed type | Validation / impact / mitigation |
|---|---|---|---|---|---|
| A-Q1-1 | Inspected items can be represented by a stated sampling model (e.g., independent Bernoulli draws, or a finite-batch alternative). | Q1; sampling plan is required but the sampling protocol is not specified. | Needed to calculate valid sequential error guarantees. | human judgment pending | The sampling frame determines whether binomial-type sequential evidence is valid; record the alternative if a finite batch is sampled without replacement. |
| A-Q1-2 | A practical distinction around \(p_0=0.10\), a finite operational cap, or an inconclusive terminal decision is permitted. | Q1; the composite hypotheses meet at \(p_0\). | Needed because a forced, uniformly finite sequential accept/reject decision at the boundary is not identified by the two confidence statements alone. | human judgment pending | The next choice card selects the governing convention; sensitivity analysis must cover it. |
| A-Q2-3 | Reused items follow an explicitly selected finite-cycle or infinite-horizon expected-value convention. | Q2/Q3; the statement says to repeat steps after disassembly. | Needed to avoid ambiguous cost recursion. | human judgment pending | Defer until Q2/Q3 framing; compare conventions if economically material. |
