from langgraph.graph import StateGraph, END
from langchain_core.messages import AIMessage

from agent.state import AgentState
from agent.intent import detect_intent
from agent.rag import retrieve_context
from agent.tools import mock_lead_capture


# -------- Nodes -------- #

def intent_node(state: AgentState):
    user_msg = state["messages"][-1].content
    state["intent"] = detect_intent(user_msg)
    return state


def greeting_node(state: AgentState):
    state["messages"].append(
        AIMessage(content="Hi! 👋 I can help you with pricing, features, or getting started with AutoStream.")
    )
    return state


def rag_node(state: AgentState):
    query = state["messages"][-1].content
    context = retrieve_context(query)
    reply = f"Here’s what I found:\n{context}"
    state["messages"].append(AIMessage(content=reply))
    return state


def lead_node(state: AgentState):

    if state.get("name") is None:
        state["messages"].append(AIMessage(content="Great! May I know your name?"))
        return state

    if state.get("email") is None:
        state["messages"].append(AIMessage(content="Thanks! Could you share your email address?"))
        return state

    if state.get("platform") is None:
        state["messages"].append(
            AIMessage(content="Which platform do you create content on? (YouTube, Instagram, etc.)")
        )
        return state

    mock_lead_capture(state["name"], state["email"], state["platform"])
    state["messages"].append(AIMessage(content="You're all set! Our team will contact you shortly. 🚀"))
    return state


# -------- Router -------- #

def router(state: AgentState):
    
    if state.get("lead_stage") is not None and state["lead_stage"] != "done":
        return "lead"

    if state["intent"] == "high_intent":
        return "lead"

    if state["intent"] == "greeting":
        return "greeting"

    return "rag"


# -------- Graph -------- #

graph = StateGraph(AgentState)

graph.add_node("intent", intent_node)
graph.add_node("greeting", greeting_node)
graph.add_node("rag", rag_node)
graph.add_node("lead", lead_node)

graph.set_entry_point("intent")

graph.add_conditional_edges(
    "intent",
    router,
    {
        "greeting": "greeting",
        "rag": "rag",
        "lead": "lead"
    }
)

graph.add_edge("greeting", END)
graph.add_edge("rag", END)
graph.add_edge("lead", END)

agent_app = graph.compile()
