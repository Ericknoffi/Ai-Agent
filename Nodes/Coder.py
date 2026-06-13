import re
import json
from langchain_core.messages import SystemMessage, HumanMessage
from Gateway.models import ModelRole
from config import CODER_PROMPT
from .supervisor_node import AgentState
from ._utils import get_current_task, build_updated_tasks, get_prior_results


def _parse_coder_json(text: str) -> dict | None:
    """
    Parse the JSON object the coder prompt instructs the model to return.
    Strips markdown fences if the model added them despite being told not to.
    Returns a dict with keys {summary, run, files} or None on parse failure.
    """
    cleaned = re.sub(r"```(?:json)?\n?|```", "", text).strip()
    try:
        parsed = json.loads(cleaned)
        
        if isinstance(parsed, dict) and any(k in parsed for k in ("summary", "run", "files")):
            return parsed
    except (json.JSONDecodeError, ValueError):
        pass
    return None


async def coder(state: AgentState):
    task = get_current_task(state)

    
    prior = get_prior_results(state)
    human_content = (
        f"Original request: {state['user_query']}\n\n"
        + (f"{prior}\n\n" if prior else "")
        + f"Your task: {task['description']}"
    )

    try:
        agent = state["llm_gateway"].get_agent(ModelRole.CODING)

        response = await agent.ainvoke({
            "messages": [
                SystemMessage(content=CODER_PROMPT),
                HumanMessage(content=human_content),
            ]
        })

        messages = response.get("messages", [])
        last_message = messages[-1] if messages else None
        raw_text = ""

        if last_message:
            content = last_message.content
            if isinstance(content, list):
                raw_text = " ".join(
                    block.get("text", "") for block in content
                    if isinstance(block, dict)
                ).strip()
            else:
                raw_text = (content or "").strip()

            finish_reason = (
                last_message.response_metadata.get("finish_reason", "")
                if hasattr(last_message, "response_metadata") else ""
            )
            if finish_reason == "length":
                raw_text += "\n[Note: response was truncated due to token limit]"

        if not raw_text:
            raw_text = "Coder returned an empty response."


        parsed = _parse_coder_json(raw_text)
        final_result = parsed if parsed is not None else raw_text

        return {
            "tasks": build_updated_tasks(state, task["id"], "completed", final_result)
        }

    except Exception as e:
        return {
            "tasks": build_updated_tasks(state, task["id"], "failed", None),
            "errors": state.get("errors", []) + [f"Coder failed on task {task['id']!r}: {e}"],
        }
