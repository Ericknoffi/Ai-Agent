from langgraph.graph import StateGraph, START, END
from Nodes.Coder import coder
from Nodes.Planner import planner
from Nodes.Researcher import researcher
from Nodes.Finalizer import finalizer_node
from Nodes.supervisor_node import AgentState, supervisor_node, supervisor_router
import registry


graph = StateGraph(AgentState)
graph.add_node("planner", planner)
graph.add_node("supervisor", supervisor_node)
graph.add_node("research", researcher)
graph.add_node("coding", coder)
graph.add_node("finalizer", finalizer_node)

graph.add_edge(START, "planner")
graph.add_edge("planner", "supervisor")
graph.add_edge("research", "supervisor")
graph.add_edge("coding", "supervisor")
graph.add_edge("finalizer", END)

graph.add_conditional_edges(
    "supervisor",
    supervisor_router,
    {
        "research": "research",
        "coding": "coding",
        "finalizer": "finalizer",
    },
)


async def main():
    # Initialize MCP tools before constructing/using models
    await registry.initialize_tools()
    app = graph.compile()
    print("Graph compiled, tools initialized. Ready to run the app.")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())