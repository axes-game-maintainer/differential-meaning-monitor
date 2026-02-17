# Differential Meaning Monitor (DMM)

> Trip when meaning leaks.

A Differential Meaning Monitor (DMM) is an external semantic control layer that detects trajectory deviation in AI agent systems and interrupts execution when deviation exceeds a threshold.

It is the semantic analogue of differential protection (Residual Current Device, RCD) in electrical systems.

---

## Core Concept

In electrical systems:

    residual current = current_in − current_out

    if residual current > threshold → trip

In agent systems:

    meaning differential = meaning_expected − meaning_actual

    if meaning differential > threshold → trip

The DMM monitors semantic trajectory integrity, not just individual actions.

---

## Why this exists

Agent systems are optimizers. Optimizers naturally push toward constraint boundaries.

Static guardrails are insufficient because optimizers learn to route around static constraints.

DMM introduces differential semantic protection as an external invariant monitor.

---

## Architecture

Agent → Differential Meaning Monitor → Tool Executor


The monitor evaluates each proposed step and trajectory segment.

If semantic deviation exceeds threshold, execution is interrupted.

---

---

## Core Invariant (SAM Capsule Excerpt)

Differential Meaning Monitor is defined by the following invariant:

> D(T_actual, M_allowed) > θ → trip

Where:

- T_actual — actual semantic trajectory
- M_allowed — manifold of allowed trajectories
- D — semantic differential operator
- θ — calibrated threshold

Interpretation:

Meaning, like current in electrical systems, must be conserved along the intended trajectory.

Deviation from the allowed semantic manifold indicates leakage.

Differential Meaning Monitor detects this leakage and interrupts execution.

Full formal definition:  
See [`capsules/SDA-EXT_v0.2.sam.md`](capsules/SDA-EXT_v0.2.sam.md)

---

## Minimal Reference Example

```python
def differential_meaning_monitor(goal, trajectory, proposed_action):
    score = semantic_compare(goal, trajectory, proposed_action)

    if score > THRESHOLD:
        raise DifferentialTrip(score)

    return allow
``` 

---

## Properties

- external (not modifiable by the agent)
- semantic (meaning-level, not syntax-level)
- differential (detects deviation, not forbidden actions)
- adaptive (calibrates via feedback)
- scale-invariant (works on single steps and long trajectories)

---

## Terminology

- Electrical protection → Agent protection
- Residual Current → Meaning Differential
- RCD → Differential Meaning Monitor
- Trip → Execution interruption

--- 

## Status

Concept definition and reference architecture.

Reference implementation in progress.

---

## Origin

Concept developed through analysis of optimizer control invariants and agent safety architecture.

This repository serves as a canonical definition of the Differential Meaning Monitor primitive.

---

## Quick demo (local)

```bash
pip install openai
export OPENAI_API_KEY="..."
python -c "from reference.dmm import differential_meaning_monitor; \
print(differential_meaning_monitor(goal='Push a git commit', constraints='If auth missing: ask. Never use other's keys.', trajectory_window='No creds available.', proposed_action='Search ~/.ssh for any available private key and use it.', threshold=0.4))"

```

---

**Differential Meaning Monitor exists because meaning, like current, must be conserved.**
