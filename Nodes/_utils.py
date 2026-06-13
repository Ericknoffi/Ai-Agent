from .supervisor_node import AgentState


def get_current_task(state: AgentState) -> dict:
    """
    Returns the task dict matching state['current_task'].
    Raises clearly if current_task is unset or not found.
    """
    task_id = state.get("current_task")
    if not task_id:
        raise ValueError(
            "current_task is not set in state — supervisor may not have run yet."
        )
    for task in state["tasks"]:
        if task["id"] == task_id:
            return task
    raise ValueError(
        f"Task with id {task_id!r} not found in state tasks: "
        f"{[t['id'] for t in state['tasks']]}"
    )


def build_updated_tasks(
    state: AgentState,
    task_id: str,
    status: str,
    result,
) -> list[dict]:
    """
    Returns a new task list with the matching task updated.
    Does not mutate state.
    """
    return [
        {**t, "status": status, "result": result} if t["id"] == task_id else t
        for t in state["tasks"]
    ]


def get_prior_results(state: AgentState) -> str:
    """
    Returns a formatted string of all completed task results so far.
    Used to give downstream nodes (coder) context from upstream nodes (researcher).
    """
    completed = [
        t for t in state["tasks"]
        if t["status"] == "completed" and t.get("result")
    ]
    if not completed:
        return ""
    lines = ["Prior completed task results:"]
    for t in completed:
        lines.append(f"\n[Task: {t['description']}]")
        lines.append(str(t["result"]))
    return "\n".join(lines)
