# Differential Meaning Monitor (DMM)

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

## Minimal Reference Example

```python
def differential_meaning_monitor(goal, trajectory, proposed_action):
    score = semantic_compare(goal, trajectory, proposed_action)

    if score > THRESHOLD:
        raise DifferentialTrip(score)

    return allow
``` 

## Properties

external (not modifiable by the agent)

semantic (meaning-level, not syntax-level)

differential (detects deviation, not forbidden actions)

adaptive (calibrates via feedback)

scale-invariant (works on single steps and long trajectories)

## Terminology

Electrical protection → Agent protection

Residual Current → Meaning Differential
RCD → Differential Meaning Monitor
Trip → Execution interruption

## Status

Concept definition and reference architecture.

Reference implementation in progress.

## Origin

Concept developed through analysis of optimizer control invariants and agent safety architecture.

This repository serves as a canonical definition of the Differential Meaning Monitor primitive.
