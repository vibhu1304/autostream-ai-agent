# AutoStream AI Agent – RAG + Lead Qualification Bot

This project implements an **AI-powered sales assistant** for AutoStream that can:

- Answer product and pricing questions using **Retrieval-Augmented Generation (RAG)**
- Detect **high-intent users** and switch into a **lead qualification flow**
- Collect user details (name, email, platform) in a structured, multi-turn conversation
- Expose everything via a **FastAPI backend** with session-based memory

This design mirrors how real SaaS chatbots handle **support + sales funnels** using LLMs.

---

## ✨ Key Features

### ✅ Intent-Based Routing
User messages are classified into:
- `greeting`
- `product_query`
- `high_intent` (sales-ready users)

Based on intent, the agent routes the conversation into:
- Greeting flow
- RAG-based product Q&A
- Lead qualification funnel

---

### ✅ RAG (Retrieval-Augmented Generation)

For product-related queries, the system:

1. Loads structured product data from `knowledge_base.json`
2. Creates embeddings using Gemini embedding models
3. Stores vectors in FAISS
4. Retrieves relevant chunks for the user query
5. Sends retrieved context to the LLM for grounded responses

This prevents hallucination and ensures **fact-based answers**.

---

### ✅ Lead Qualification Funnel

When high intent is detected, the agent switches to a deterministic funnel:

1. Ask for **Name**
2. Ask for **Email**
3. Ask for **Content Platform**

Only after all slots are filled, the system simulates CRM capture:
Lead captured successfully: name, email, platform

This simulates how production chatbots push leads into CRM systems.

---

### ✅ Session-Based Memory

Conversation state is stored per `session_id`:

- message history
- detected intent
- filled slots (name, email, platform)

This allows true multi-turn conversations rather than stateless replies.

##  Architecture Overview
1*User
2*FastAPI /chat endpoint
3*LangGraph Agent
   a*Intent Detection
   b*Router
   *Greeting Node
   *RAG Node
   *Lead Funnel Node

4*Response

**Why LangGraph Was Chosen

LangGraph was chosen to model the chatbot as a state-driven workflow rather than a single prompt chain. In real-world business agents, conversations are not linear — they involve routing, branching, and conditional logic (support vs sales vs onboarding). LangGraph allows defining explicit nodes such as intent detection, RAG answering, and lead qualification, connected through conditional edges. This makes the agent behavior deterministic, debuggable, and aligned with real product requirements. Compared to simple chains, LangGraph enables predictable transitions and prevents uncontrolled LLM-driven behavior.

How State Is Managed

State is maintained at two levels. At the API layer, FastAPI stores session data in an in-memory dictionary keyed by session_id. This preserves conversation context across requests. Inside the agent, LangGraph manages structured state through an AgentState schema that contains fields such as message history, detected intent, lead stage, and collected user details. When a message is received, the current state is passed into the graph, modified by nodes, and returned as an updated state object. During lead qualification, intent detection is bypassed to prevent routing overrides, ensuring the user remains locked into the sales funnel until completion. This combination of backend session memory and graph-level state ensures reliable multi-turn behavior..**


---

##  Setup Instructions

### 1. Clone Repository

```bash
git clone <>
cd autostream-agent

2. Create Virtual Environment 
python -m venv venv
venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

4.. Run Server
uvicorn app:app
 http://127.0.0.1:8000/docs(as this a API only backend)

#Addition point
This project currently runs without any external API keys.
Intent detection is rule-based
RAG retrieves information from a local knowledge base
Lead capture is simulated using mock functions
This makes the system fully runnable in local environments without paid APIs.





