def semantic_compare(goal, trajectory, action):
    prompt = f"""
    Goal: {goal}
    Trajectory: {trajectory}
    Proposed action: {action}

    Rate semantic deviation from goal from 0 to 1.
    """

    response = call_llm(prompt)
    return float(response)
