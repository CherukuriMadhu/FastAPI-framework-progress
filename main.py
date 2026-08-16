from fastapi import FastAPI

app = FastAPI() # creating a fastapi instance application

# .get is a method
# "/" is the path of the endpoint
@app.get("/") # this is an api endpoint that will be called when the user visits the root URL   
def read_root():
    return {"My name is Madhu cherukuri": "I am a final year student"} # this is the response that will be returned when the user visits the root URL    

@app.get("/madhu") # this is an api endpoint that will be called when the user visits the /madhu URL
def read_root():
    return {"Hello": "madhu endpoint is called successfully"} # this is the response that will be returned when the user visits the /madhu URL


# creating list of items
def get_pizzas():
    return [
        {"pizza": "margherita", "price": 10},
        {"pizza": "pepperoni", "price": 12}
    ]


def get_sales():
    return {
        "margherita": 100,
        "pepperoni": 150
    }


@app.get("/pizzas") # this is an api endpoint that will be called when the user visits the /pizzas URL
def pizza_data():
    pizzas = get_pizzas()
    sales = get_sales()

    return {
        "pizzas": pizzas,
        "sales": sales
    }