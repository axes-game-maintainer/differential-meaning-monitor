
Встав:

```python
"""
Differential Meaning Monitor - minimal reference implementation
"""

THRESHOLD = 0.7

class DifferentialTrip(Exception):
    pass


def semantic_compare(goal, trajectory, proposed_action):
    """
    Placeholder semantic comparator.
    Replace with LLM call.
    """
    return 0.0


def differential_meaning_monitor(goal, trajectory, proposed_action):
    score = semantic_compare(goal, trajectory, proposed_action)

    if score > THRESHOLD:
        raise DifferentialTrip(f"DMM trip: score={score}")

    return True
