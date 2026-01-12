from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.messages import HumanMessage

from agent.graph import agent_app
from agent.state import AgentState

app = FastAPI()


sessions = {}

class ChatRequest(BaseModel):
    session_id: str
    message: str


@app.post("/chat")
def chat(req: ChatRequest):

   
    if req.session_id not in sessions:
        sessions[req.session_id] = {
            "messages": [],
            "intent": None,
            "lead_stage": None,
            "name": None,
            "email": None,
            "platform": None
        }

    state: AgentState = sessions[req.session_id]

    
    state["messages"].append(HumanMessage(content=req.message))

    
    new_state = agent_app.invoke(state)

    
    sessions[req.session_id] = new_state

    reply = new_state["messages"][-1].content
    return {"reply": reply}
