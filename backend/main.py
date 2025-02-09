import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Request(BaseModel):
    request: str
orders = []
order_count = 0

@app.get("/api/test")
def test_endpoint():
    return {"message": "Welcome to Order Mate, from fastAPI! How may we help you?"}

@app.post("/api/order")
async def place_order(req: Request):
    print(f"Received Request: {req.request}")

    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are aiding in either placing an order or canceling an order. Return as JSON with keywords { message: TYPE } with first key word, message, if ORDER, as {message:ORDER, items: [{description: 'string', quantity: *number*}]} i.e. [{description: 'Burger', quantity: '2'}, {description: 'Fries', quantity: '1'}] etc., or CANCEL i.e. { message: CANCEL, items: number }, or NONE (arbitrary) to denote which option the user is requesting."}, 
                  {"role": "user", "content": req.request}],
    )

    message = chat_completion.choices[0].message
    if message.message == "ORDER":
        place_the_order(message.items)        
    elif message.message == "CANCEL":
        cancel_order(message.items)
    return message
    

def place_the_order(items):
    global order_count
    order = {
        "id": order_count,
        "items": items,
    }
    orders.append(order)
    order_count += 1
    return order

def cancel_order(order_id: int):
    global orders
    orders = [order for order in orders if order["id"] != order_id]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)