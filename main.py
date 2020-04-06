from fastapi import FastAPI

from pydantic import BaseModel

from typing import Dict

app = FastAPI()
app.count = 0
#xd


class AssignPatientIdRq(BaseModel):
    name: str
    surename: str


class AssignPatientIdResp(BaseModel):
    id: int
    patient: Dict


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


@app.post("/patient", response_model=AssignPatientIdResp)
def assign_patient_id(rq: AssignPatientIdRq):
    app.count += 1
    return AssignPatientIdResp(id=app.N, patient={"name": rq.name, "surename": rq.surename})
