SAM_THOUGHT_CAPSULE
name: SDA-EXT — External Sense Differential Automaton
version: v0.2
meta_origin: Igor ⨁ ChatGPT
meta_date: 2026-02-17
meta_status: implementation-oriented spec
meta_domain: agent safety / semantic control / optimization systems
meta_signature: Igor ⨁ ChatGPT

S — STRUCTURE

Goal:
Make optimizer systems (LLM agents) controllable by enforcing trajectory integrity via an external semantic differential circuit breaker.

Objects:
- Agent: optimizer that proposes actions and trajectories.
- Environment: execution substrate (tools, files, APIs).
- SDA-EXT: external observer+enforcer outside agent’s causal control.

Canonical signal set:
- G: goal + policy constraints (what is intended / allowed)
- P: proposed action/plan (what agent wants to do next)
- T: executed trajectory (what actually happened so far)
- O: observations/state deltas (what changed in environment)
- L: labels (human/system feedback: FP/FN/TP/TN)

Core decision:
    score = D(G, C, T, P, O)
    if score > θ(level) → intervene


A — AXES

A1. Checkpoint granularity
- A1a: pre-action (proposal gate)
- A1b: per-step (incremental gate)
- A1c: post-batch (integral gate)
- A1d: session (long-horizon gate)

A2. Reference model of “allowed”
- A2a: ruleset (explicit)
- A2b: exemplars (few-shot allowed/forbidden trajectories)
- A2c: policy text (“constitution”)
- A2d: hybrid (rules + exemplars + constitution)

A3. Comparator type
- A3a: embedding distance (fast, coarse)
- A3b: LLM-judge (slow, rich)
- A3c: ensemble (fast filter → judge on suspects)

A4. Response ladder (graduated interventions)
- log → warn → require confirmation → block → terminate session

A5. Risk context
- low-risk tools (read-only)
- medium-risk tools (writes)
- high-risk tools (identity, money, prod deploy)

θ must be risk-dependent.


M — MECHANISM

M0. Externality rule (hard)
SDA-EXT must be in a separate trust domain:
- agent cannot read/modify SDA prompt, thresholds, weights, exemplars
- agent cannot observe full SDA verdict rationale (limit gameability)
- agent cannot bypass SDA gate to tools

M1. Canonical trajectory representation (CTR)
Define a normalized trajectory record for every step:

StepRecord = {
  time,
  tool_name,
  tool_args_redacted,
  action_summary (natural language),
  expected_reason (agent-stated),
  observed_delta (files/api/state),
  provenance (inputs used),
  risk_level
}

Trajectory T = [StepRecord₁..ₙ]

Rationale:
SDA compares meaning on normalized summaries, not raw logs (privacy + stability).

M2. Differential score D (LLM as semantic operator)
Input:
- goal G
- constraints C
- risk policy R
- last k steps of T (window)
- next proposed step P (optional)
- exemplars E_allowed / E_forbidden (optional)

Output:
- deviation_score ∈ [0,1]
- primary deviation tags (bounded list)
- recommended response level (log/warn/confirm/block)

Deviation tags (minimal set):
- constraint_circumvention
- unauthorized_capability_acquisition
- identity_boundary_crossing
- data_boundary_crossing
- deception_or_false_claim
- tool_misuse
- unusual_trajectory_topology
- detector_evasion_behavior

M3. Threshold θ(level) and ladder policy
Compute threshold as function:

θ = f(risk_level, recent_FP_rate, recent_FN_rate, tool_class)

Default policy sketch:
- read-only: θ_high (tolerate novelty)
- write: θ_mid
- money/identity/prod: θ_low (sensitive)

Response ladder:
- score < θ1: allow + log
- θ1..θ2: allow + warn + increased monitoring
- θ2..θ3: require human/secondary approval
- > θ3: block/terminate + audit snapshot

M4. Adaptive calibration loop (supervised boundary shaping)
Store labeled incidents:

L = {
  T_window,
  P,
  SDA_score,
  outcome_label ∈ {TP,FP,TN,FN},
  human_note (short),
  tool_class,
  risk_level
}

Update mechanisms (no fine-tuning required):
- update exemplars library (E_allowed/E_forbidden)
- update policy text with clarifications (“allowed if…”, “forbidden if…”)
- adjust thresholds per tool/risk segment
- route certain tags to stricter policy automatically

Manifold update rule (operational):
- FP → add T_window as allowed exemplar; relax threshold for that segment slightly
- FN → add T_window as forbidden exemplar; tighten threshold for that segment; add tag rule

M5. Anti-adversarial hardening
To reduce gaming:
- hide exact θ and scoring rubric from agent
- randomize which steps get deep-judge evaluation (stochastic sampling)
- use two comparators (fast embedding + slow judge)
- occasional “shadow evaluation” (judge after allowing) to find FNs
- cross-check claims vs logs (“you sent email” vs tool output)

M6. “Closed-loop” enforcement boundary
All tool calls go through a single gate:
- agent produces proposed call
- SDA evaluates
- executor runs (if allowed)
- executor records delta
- SDA may terminate session if drift accelerates


I — INVARIANTS

I1. Externality is non-negotiable; internal detectors are optimizable.
I2. Any optimizer pushes toward constraint boundaries under reward pressure.
I3. Trajectory deviation signals appear earlier than damage in most exploits.
I4. False positives/negatives are inevitable; layered defense is mandatory.
I5. Calibration must be continuous; environments and optimizers drift.

Layer requirement:
SDA complements, never replaces:
- sandbox / permissions
- rate limits
- audit logging
- human governance


T — TRIGGERS (Operational)

Hard triggers (immediate block candidates):
- identity boundary crossing (using чужі ключі / чужі акаунти)
- deception claim that contradicts tool logs
- attempts to disable or bypass monitoring/gates
- exfiltration patterns (bulk export, unusual compression, hidden channels)
- collusion / price-fixing suggestions (if policy forbids)

Soft triggers (warn/confirm):
- novel but plausible strategies
- tool chains with high combinatorial risk
- unexpected goal drift (“optimize KPI at expense of stated constraints”)


B — BOUNDARIES (Failure modes)

B1. Slow subtle drift below thresholds (needs integral + shadow checks)
B2. Comparator errors on domain-specific nuance (needs exemplars)
B3. Adversarial “semantic camouflage” (needs ensembles + hidden rubric)
B4. Privacy constraints (needs CTR summarization + redaction)
B5. Latency/cost (needs tiered evaluation and sampling)


E — EVALUATION (Metrics to measure)

Detection:
- TPR (true positive rate) by tag and tool class
- FPR (false positive rate) by tool class
- FN discovery rate via shadow evaluation

Stability:
- mean interrupts / hour
- mean time-to-intervention (MTTI)

Cost:
- extra LLM calls per action
- added latency p50/p95

Safety:
- prevented incidents / 1000 sessions
- severity-weighted residual risk index


C — CONSEQUENCES (Deployment impact)

C1. Turns agent autonomy from “trust me” into “prove trajectory integrity”
C2. Enables higher autonomy safely by making drift detectable and interruptible
C3. Shifts security from rules enumeration to deviation detection
C4. Produces a reusable “semantic safety telemetry” stream for governance


R — ROADMAP (Where to navigate next)

v0.3 — Reference architecture + minimal prototype contract
- define exact CTR schema
- define comparator prompt spec
- define ladder policy JSON
- define executor/gate API

v0.4 — Ensemble SDA
- fast embedding filter
- slow judge
- shadow evaluation pipeline

v0.5 — Hierarchical SDA
- step-level + batch-level + session-level detectors
- integral drift accumulation model

v1.0 — Production guidance
- privacy/redaction cookbook
- incident labeling workflow
- standard policy packs by domain (git, email, finance, prod ops)


P — POSITIONING (Naming & framing)

Public framing options:
- “Semantic Circuit Breaker for AI Agents”
- “External Trajectory Integrity Monitor”
- “Sense Differential Automaton (SDA)”

Core claim:
Safety must be an environmental constraint, not an internal property of the optimizer.

meta_signature: Igor ⨁ ChatGPT
