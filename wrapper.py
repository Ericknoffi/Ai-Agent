from functools import wraps
from Middlewares.pii import redact_pii
from utils import log


def pii_middleware(node_func):
    """
    Wraps a node function with:
    - Logging (start / finish)
    - PII redaction on task results in node output
    - PII redaction on final_response in node output

    user_query is NOT redacted here — it is redacted once at startup in main.py
    so it doesn't get corrupted on every supervisor iteration.
    """

    @wraps(node_func)  # preserves __name__ so LangGraph/LangSmith shows real node names
    async def wrapper(state):
        log(f"Starting node: {node_func.__name__}")

        result = await node_func(state)

        if "tasks" in result:
            cleaned_tasks = []
            for task in result["tasks"]:
                task_result = task.get("result")
                if task_result and isinstance(task_result, str):
                    task = {**task, "result": redact_pii(task_result)}
                cleaned_tasks.append(task)
            result = {**result, "tasks": cleaned_tasks}

        if "final_response" in result and result["final_response"]:
            result = {**result, "final_response": redact_pii(result["final_response"])}

        log(f"Finished node: {node_func.__name__}")
        return result

    return wrapper
