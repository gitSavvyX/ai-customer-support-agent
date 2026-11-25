# 🤖 Autonomous Customer Support Agent
An Agentic AI system that uses OpenAI Function Calling (Tool Calling) to autonomously resolve customer support tickets. It can read the customer's issue, query a mock database for their order status, and draft a personalized response.

## 🧠 Agentic Logic
Unlike a standard chatbot, this agent uses **Tool Calling**. When a user asks "Where is my order?", the agent:
1. Recognizes it needs external data.
2. Calls the `get_order_status` tool (Python function).
3. Receives the data (e.g., "Shipped").
4. Uses the LLM to generate a polite response based on the live data.

## 🛠️ Tech Stack
• Python, FastAPI
• OpenAI API (Tool Calling / Agents)
• Pydantic, JSON
• Mock SQLite Database
