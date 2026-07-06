# Core Model

ArbiterSTG operates after execution. Its object is residue, not authorization.

## Operating Sequence

```text
execution -> residue production -> accessibility review -> trace classification -> routing or disposition
```

ArbiterSTG begins after execution has occurred. It does not decide whether execution should occur. It does not decide whether execution was valid. It classifies the post-execution condition of residue.

## Core Questions

1. What residue is asserted or observed?
2. Was residue produced?
3. Is it accessible?
4. Is access direct, partial, proxy-mediated, or bridge-dependent?
5. What mode should govern its post-execution handling?
6. What claims exceed the trace?
7. What warnings or flags must remain attached?

## Residue Transitions

| Transition | Description |
| --- | --- |
| `R_p -> R_a` | Produced residue becomes accessible. |
| `R_p -> R_s` | Produced residue is assigned to an interpretive, institutional, or proxy route. |
| `R_p -> R_u` | Produced residue persists but becomes unreachable. |
| `R_u -> R_a via R_b` | Unreachable residue becomes accessible through bridge residue. |
| `R_a -> R_s` | Accessible residue becomes assigned. |

## Trace Eligibility Threshold

The Trace Eligibility Threshold is the minimum condition required for residue to enter structured trace review.

Residue below the threshold may remain Null, Shadowed, or outside formal admission. Threshold failure should not be converted into proof of non-execution.

Suggested threshold checks:

- A residue assertion is named.
- Its relation to a prior execution is stated.
- Its accessibility condition is stated.
- Its route, if any, is stated.
- Any support limitation is stated.
- Any claim made from the residue is stated.

