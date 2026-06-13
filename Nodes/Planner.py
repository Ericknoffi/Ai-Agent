from pydantic import BaseModel, field_validator
from typing import Literal
from langchain_core.messages import SystemMessage, HumanMessage
from Gateway.models import ModelRole
from config import PLANNER_PROMPT
from .supervisor_node import AgentState


class PlannedTask(BaseModel):
    id: str
    description: str
    assigned_agent: Literal["research", "coding"]


class PlannerOutput(BaseModel):
    request_domain: Literal["software", "general"]
    reasoning: str = ""          
    tasks: list[PlannedTask]

    @field_validator("tasks")
    @classmethod
    def max_three_tasks(cls, v: list) -> list:
        return v[:3]


def normalize_tasks_for_general_request(tasks: list[PlannedTask]) -> list[PlannedTask]:
    """Force all tasks to research agent for non-software requests."""
    return [
        PlannedTask(id=t.id, description=t.description, assigned_agent="research")
        for t in tasks
    ]


def _dedup_task_ids(tasks: list[dict]) -> list[dict]:
    """Ensure task IDs are unique — LLM can occasionally produce duplicates."""
    seen: set[str] = set()
    deduped = []
    for task in tasks:
        tid = task["id"]
        if tid in seen:
            task = {**task, "id": f"{tid}_{len(seen)}"}
        seen.add(task["id"])
        deduped.append(task)
    return deduped


async def planner(state: AgentState):
    if not state.get("llm_gateway"):
        raise ValueError("llm_gateway missing from state — was it set in main.py?")

    planner_llm = state["llm_gateway"].get_model(ModelRole.PLANNER)
    planner_chain = planner_llm.with_structured_output(PlannerOutput)  

    try:
        plan = await planner_chain.ainvoke(
            [
                SystemMessage(content=PLANNER_PROMPT),
                HumanMessage(content=state["user_query"]),
            ]
        )
    except Exception as e:
        return {
            "tasks": [{
                "id": "t1",
                "description": state["user_query"],
                "status": "pending",
                "assigned_agent": "research",
                "result": None,
                "retry_count": 0,
            }],
            "iteration_count": 0,
            "planner_reasoning": f"Planner LLM failed ({e}), falling back to single research task.",
            "errors": state.get("errors", []) + [f"Planner error: {e}"],
        }

    if not plan.tasks:
        return {
            "tasks": [{
                "id": "t1",
                "description": state["user_query"],
                "status": "pending",
                "assigned_agent": "research",
                "result": None,
                "retry_count": 0,
            }],
            "iteration_count": 0,
            "planner_reasoning": "Planner returned no tasks — using single research task fallback.",
            "errors": state.get("errors", []) + ["Planner returned empty task list"],
        }

    planned_tasks = (
        normalize_tasks_for_general_request(plan.tasks)
        if plan.request_domain == "general"
        else plan.tasks
    )

    tasks = [
        {
            "id": task.id,
            "description": task.description,
            "status": "pending",
            "assigned_agent": task.assigned_agent,
            "result": None,
            "retry_count": 0,   
        }
        for task in planned_tasks
    ]

    tasks = _dedup_task_ids(tasks)

    return {
        "tasks": tasks,
        "iteration_count": 0,
        "planner_reasoning": plan.reasoning,
    }
