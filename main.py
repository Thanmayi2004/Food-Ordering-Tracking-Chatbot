from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
import db_helper
import generic_helper

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="Frontend/Templates/css"), name="static")
app.mount("/images", StaticFiles(directory="Frontend/Templates/images"), name="images")

inprogress_orders = {}

# Serve the index.html
@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("Frontend/Templates/index.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

@app.post("/")
async def handle_request(request: Request):
    payload = await request.json()
    
    # Extract intent and parameters from the request payload
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']
    
    session_id = generic_helper.extract_session_id(output_contexts[0]['name'])
    
    intent_handler_dict = {
        'add.order- context: ongoing-order': add_to_order,
        'remove.order - context: ongoing-order': remove_from_order,
        'order.complete - context:ongoing-order': complete_order,
        'track.order - context: ongoing-tracking': track_order   
    }
    
    return intent_handler_dict[intent](parameters, session_id)

def remove_from_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        return JSONResponse(content={
            "fulfillmentText": "I'm having trouble finding your order. Sorry! Can you please place your order again"
        })
        
    current_order = inprogress_orders[session_id] 
    food_items = parameters["food-items"]
    
    removed_items = []
    no_such_items = []
    
    for item in food_items:
        if item not in current_order:
            no_such_items.append(item)
        else:
            removed_items.append(item)
            del current_order[item]
            
    if len(removed_items) > 0:
        fulfillment_text = f'Removed {",".join(removed_items)} from your order!'
                
    if len(no_such_items) > 0:
        fulfillment_text += f' Your current order does not have {",".join(no_such_items)}.'
    
    if len(current_order.keys()) == 0:
        fulfillment_text += " Your order is empty!"
    else:
        order_str = generic_helper.get_str_from_food_dict(current_order) 
        fulfillment_text += f" Here is what is left in your order: {order_str}"
    
    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })
    
def add_to_order(parameters: dict, session_id: str):
    food_items = parameters["food-items"]
    quantities = parameters["number"]
    
    if len(food_items) != len(quantities):
        fulfillment_text = "Sorry I didn't understand. Can you please specify food items and quantities clearly?" 
    else:
        new_food_dict = dict(zip(food_items, quantities))
        
        if session_id in inprogress_orders:
            current_food_dict = inprogress_orders[session_id]
            current_food_dict.update(new_food_dict)
            inprogress_orders[session_id] = current_food_dict
        else:
            inprogress_orders[session_id] = new_food_dict
            
        order_str = generic_helper.get_str_from_food_dict(inprogress_orders[session_id])
        fulfillment_text = f"So far you have: {order_str}. Would you like to alter any quantity for any food item or add anything else?"
    
    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })
    
def complete_order(parameters: dict, session_id: str):
    if session_id not in inprogress_orders:
        fulfillment_text = "I'm having trouble finding your order. Sorry! Can you place a new order again?" 
    else:
        order = inprogress_orders[session_id]
        order_id = save_to_db(order)
        
        if order_id == -1:
            fulfillment_text = "Sorry, I could not process your order due to a backend error. Please place a new order again."
        else:
            order_total = db_helper.get_total_order_price(order_id)
            fulfillment_text = f"Awesome. We have placed your order. " \
                               f"Here is your order ID #{order_id}. " \
                               f"Your order total is {order_total}, which you can pay at the time of your delivery!"
        
        del inprogress_orders[session_id]
                               
    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })                           

def save_to_db(order: dict):
    next_order_id = db_helper.get_next_order_id()
    
    for food_item, quantity in order.items():
        rcode = db_helper.insert_order_item(
            food_item,
            quantity,
            next_order_id
        )
        
        if rcode == -1:
            return -1
        
    db_helper.insert_order_tracking(next_order_id, "In progress")    
        
    return next_order_id   

def track_order(parameters: dict, session_id: str):
    order_id = int(parameters['order_id'])
    status = db_helper.get_order_status(order_id)  
    
    if status:
        fulfillment_text = f"The order status for order ID: {order_id} is: {status}."
    else:
        fulfillment_text = f"No order found with order ID: {order_id}."
        
    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })
