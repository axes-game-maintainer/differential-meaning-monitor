# DMM Specification (Draft)

## Terms
- Agent
- Trajectory (T)
- Allowed manifold (M)
- Deviation score (D)
- Trip thresholds (θ1..θ3)

## Canonical Trajectory Representation (CTR)
Describe StepRecord fields and redaction rules.

## Decision API
Input: G, C, T_window, P
Output: score, tags, recommended_action

## Response Ladder
log / warn / confirm / block / terminate

## Calibration
How FP/FN labels update exemplars and thresholds.
