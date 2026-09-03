# Q2 Method Card

## Goal and success criteria

Maximize expected profit per fulfilled customer demand for each Table-1 case, with each policy branch charged once. A fulfilled demand ends only at a good product; an uninspected defective product causes exchange loss and a replacement requirement.

## Human constraints

- Output form: complete policy and comparable expected profit.
- Priority: exact branch accounting and reproducibility.
- Accelerated-evaluation note: the user authorized technical choices without additional low-impact Gates; this is not a normal G2.5 record.

## Shortlist

| ID | Role | Mathematical idea | Why eligible | Main risk |
|---|---|---|---|---|
| M2 | main_candidate | Enumerate all \(2^4=16\) stationary policies; evaluate each by an absorbing Markov reward system over retained component-quality states. | Complete finite policy space; exact reuse recursion. | Interpretation of customer replacement and repeated reuse. |
| B2 | usable_baseline | The all-no-inspection, no-disassembly policy evaluated by the same state-reward accounting. | It completes the same customer-demand task and has directly comparable expected profit. | Economically weak but valid. |

## MODEL ASSUMPTIONS

1. Component and conditional assembly defect events are independent across new purchases/assemblies and match Table 1 rates.
2. A returned defective product must be replaced; its recovered components are reused only if the policy chooses disassembly. The market price is collected once per initial customer demand.
3. A tested component recovered after disassembly is tested again when the stationary policy says to inspect. This follows the statement's instruction to repeat the stages.

## Risk-probe summary

The exact linear-system implementation must check transition probability sums, Bellman residuals, and finite expected values. The fallback trigger is any singular/ill-conditioned system or interpretation conflict; then report the affected policy as unsupported rather than inventing a value.
