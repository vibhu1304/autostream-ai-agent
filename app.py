from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.messages import HumanMessage

from agent.graph import agent_app
from agent.state import AgentState

app = FastAPI()

# simple in-memory session store
sessions = {}

class ChatRequest(BaseModel):
    session_id: str
    message: str


@app.post("/chat")
def chat(req: ChatRequest):

    # initialize state if new session
    if req.session_id not in sessions:
        sessions[req.session_id] = {
            "messages": [],
            "intent": None,
            "name": None,
            "email": None,
            "platform": None
        }

    state: AgentState = sessions[req.session_id]

    state["messages"].append(HumanMessage(content=req.message))

# Slot filling based on last question
    last_bot_msg = state["messages"][-2].content if len(state["messages"]) > 1 else ""

    if "name" in last_bot_msg.lower():
        state["name"] = req.message

    elif "email" in last_bot_msg.lower():
        state["email"] = req.message

    elif "platform" in last_bot_msg.lower():
        state["platform"] = req.message

    new_state = agent_app.invoke(state)


    # store updated state
    sessions[req.session_id] = new_state

    reply = new_state["messages"][-1].content
    return {"reply": reply}
