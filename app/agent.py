import json
import sqlite3
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI(api_key="your_api_key_here")

# 1. Setup a mock database
def setup_db():
    conn = sqlite3.connect("crm.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS orders (order_id TEXT, status TEXT, eta TEXT)")
    cursor.execute("INSERT OR IGNORE INTO orders VALUES ('ORD-101', 'Shipped', '2 Days')")
    conn.commit()
    conn.close()

# 2. Define the Tool the AI can use
def get_order_status(order_id: str) -> str:
    conn = sqlite3.connect("crm.db")
    cursor = conn.cursor()
    cursor.execute("SELECT status, eta FROM orders WHERE order_id = ?", (order_id,))
    result = cursor.fetchone()
    conn.close()
    return json.dumps({"status": result[0], "eta": result[1]}) if result else "Order not found"

# 3. Agent Logic
class TicketRequest(BaseModel):
    customer_message: str

def handle_ticket(message: str):
    setup_db()
    
    tools = [{
        "type": "function",
        "function": {
            "name": "get_order_status",
            "description": "Get the status of a customer order",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "The order ID, e.g., ORD-101"}
                },
                "required": ["order_id"]
            }
        }
    }]

    messages = [{"role": "user", "content": message}]
    
    # Step 1: AI decides if it needs to use a tool
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    
    # Step 2: Execute the tool if requested
    if response.choices[0].message.tool_calls:
        tool_call = response.choices[0].message.tool_calls[0]
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        
        if function_name == "get_order_status":
            order_data = get_order_status(arguments["order_id"])
            
            # Step 3: Feed the data back to the AI to write the final response
            messages.append(response.choices[0].message)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": order_data
            })
            
            final_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            return final_response.choices[0].message.content

    return response.choices[0].message.content
