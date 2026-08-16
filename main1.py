from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# -----------------------------
# Root endpoint
# -----------------------------

@app.get("/")
def read_root():
    return {
        "My name is Madhu Cherukuri":
        "I am a final year student"
    }


# -----------------------------
# Pizza Model
# -----------------------------

class Pizza(BaseModel):
    pizza: str
    price: float


# -----------------------------
# In-memory database
# -----------------------------

pizzas = [
    {
        "id": 1,
        "pizza": "margherita",
        "price": 10
    },
    {
        "id": 2,
        "pizza": "pepperoni",
        "price": 12
    }
]


# -----------------------------
# CREATE - POST
# -----------------------------

@app.post("/pizzas")
def create_pizza(pizza: Pizza):

    new_pizza = {
        "id": len(pizzas) + 1,
        "pizza": pizza.pizza,
        "price": pizza.price
    }

    pizzas.append(new_pizza)

    return {
        "message": "Pizza created successfully",
        "pizza": new_pizza
    }


# -----------------------------
# READ ALL - GET
# -----------------------------

@app.get("/pizzas")
def get_all_pizzas():

    return {
        "pizzas": pizzas
    }


# -----------------------------
# READ ONE - GET
# -----------------------------

@app.get("/pizzas/{pizza_id}")
def get_pizza(pizza_id: int):

    for pizza in pizzas:
        if pizza["id"] == pizza_id:
            return pizza

    raise HTTPException(
        status_code=404,
        detail="Pizza not found"
    )


# -----------------------------
# UPDATE - PUT
# -----------------------------

@app.put("/pizzas/{pizza_id}")
def update_pizza(pizza_id: int, updated_pizza: Pizza):

    for pizza in pizzas:

        if pizza["id"] == pizza_id:

            pizza["pizza"] = updated_pizza.pizza
            pizza["price"] = updated_pizza.price

            return {
                "message": "Pizza updated successfully",
                "pizza": pizza
            }

    raise HTTPException(
        status_code=404,
        detail="Pizza not found"
    )


# -----------------------------
# DELETE - DELETE
# -----------------------------

@app.delete("/pizzas/{pizza_id}")
def delete_pizza(pizza_id: int):

    for pizza in pizzas:

        if pizza["id"] == pizza_id:

            pizzas.remove(pizza)

            return {
                "message": "Pizza deleted successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Pizza not found"
    )


# -----------------------------
# Sales
# -----------------------------

def get_sales():
    return {
        "margherita": 100,
        "pepperoni": 150
    }


@app.get("/sales")
def sales_data():

    return {
        "sales": get_sales()
    }