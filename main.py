from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World during the coronavirus pandemic!"}

@app.get("/method")
def method_get():
    return {"method": "GET"}

@app.post("/method")
def method_post():
    return {"method": "POST"}

@app.delete("/method")
def method_delete():
    return {"method": "DELETE"}

@app.put("/method")
def method_put():
    return {"method": "PUT"}
