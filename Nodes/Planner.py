from pydantic import BaseModel
from typing import Literal
from langchain_core.messages import SystemMessage,HumanMessage
from Agent.Gateway.models import ModelRole
from Agent.config import PLANNER_PROMPT
from .supervisor_node import AgentState


class PlannedTask(BaseModel):
    id: str
    description: str
    assigned_agent: Literal[
        "research",
        "coding",
        "retrieval",
        "tool"
    ]


class PlannerOutput(BaseModel):
    reasoning: str
    tasks: list[PlannedTask]


async def planner(state: AgentState):
     
     planner_llm = state.llm_gateway(ModelRole.PLANNER)
     
     planner = planner_llm.with_structured_output(PlannerOutput)

     plan = await planner.ainvoke(
         [
             SystemMessage(
                 content=PLANNER_PROMPT
             ),
             HumanMessage(
                 content=state["user_query"]
             )
         ]
     )

     tasks = [
         {
             "id": task.id,
             "description": task.description,
             "status": "pending",
             "assigned_agent": task.assigned_agent,
             "result": None
         }
         for task in plan.tasks
     ]

     return {
            "tasks": tasks,
            "iteration_count": 0,
     }