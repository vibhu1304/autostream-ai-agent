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

**LangGraph is used to implement a state machine-style agent workflow instead of a single prompt chain.**


---

##  Setup Instructions

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd autostream-agent

2. Create Virtual Environment 
python -m venv venv
venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

4.. Run Server
uvicorn app:app --host 127.0.0.1 --port 8000

#Addition point
This project currently runs without any external API keys.
Intent detection is rule-based
RAG retrieves information from a local knowledge base
Lead capture is simulated using mock functions
This makes the system fully runnable in local environments without paid APIs.





