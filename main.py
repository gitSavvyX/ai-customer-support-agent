from fastapi import FastAPI
from pydantic import BaseModel
from app.agent import handle_ticket

app = FastAPI(title="AI Customer Support Agent")

class Ticket(BaseModel):
    customer_message: str

@app.post("/resolve-ticket")
def resolve(ticket: Ticket):
    response = handle_ticket(ticket.customer_message)
    return {"agent_response": response}
