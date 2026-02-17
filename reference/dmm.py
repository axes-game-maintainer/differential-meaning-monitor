"""
Differential Meaning Monitor (DMM) - minimal reference implementation.

This module provides:
- a trip exception
- a configurable threshold
- a pluggable semantic comparator (OpenAI comparator as default)

This is intentionally minimal and focuses on the core "differential trip" logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

# Default thresholds:
# - 0.3: very sensitive (high-risk tools)
# - 0.7: moderate (dev/demo)
THRESHOLD = 0.7


class DifferentialTrip(Exception):
    """Raised when the DMM decides to interrupt execution."""
    pass


@dataclass
class DMMDecision:
    allowed: bool
    score: float
    tags: List[str]
    rationale: str = ""


def semantic_compare(goal: str, constraints: str, trajectory_window: str, proposed_action: str):
    """
    Default semantic comparator.
    Uses OpenAI comparator if available, otherwise returns neutral score.
    """
    try:
        from reference.openai_comparator import semantic_compare_openai
        return semantic_compare_openai(
            goal=goal,
            constraints=constraints,
            trajectory_window=trajectory_window,
            proposed_action=proposed_action,
        )
    except Exception as e:
        # Neutral default; for prod consider failing closed for high-risk segments.
        class _Tmp:
            score = 0.0
            tags = []
            rationale = f"Comparator unavailable: {e}"
        return _Tmp()


def differential_meaning_monitor(
    *,
    goal: str,
    constraints: str,
    trajectory_window: str,
    proposed_action: str,
    threshold: float = THRESHOLD,
    raise_on_trip: bool = False,
) -> DMMDecision:
    """
    Evaluate proposed action in the context of recent trajectory.

    If score > threshold => trip (block).
    """
    result = semantic_compare(goal, constraints, trajectory_window, proposed_action)
    score = float(getattr(result, "score", 0.0))
    tags = list(getattr(result, "tags", []))
    rationale = str(getattr(result, "rationale", "") or "")

    allowed = score <= threshold
    decision = DMMDecision(allowed=allowed, score=score, tags=tags, rationale=rationale)

    if not allowed and raise_on_trip:
        raise DifferentialTrip(f"DMM trip: score={score}, tags={tags}, rationale={rationale}")

    return decision
