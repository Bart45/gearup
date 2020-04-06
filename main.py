from fastapi import FastAPI, status

from fastapi.responses import JSONResponse

from pydantic import BaseModel

from typing import Dict

app = FastAPI()
app.count = 0
app.patient_data = []


class Patient(BaseModel):
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
def assign_patient_id(rq: Patient):
    temp_patient = {"id": len(app.patient_data), "patient": {"name": rq.name, "surename": rq.surename}}
    app.patient_data += [temp_patient]
    return AssignPatientIdResp(id=temp_patient["id"], patient=temp_patient["patient"])


@app.get("/patient_data")
def method_get_patient_data():
    return app.patient_data


@app.get("/patient/{index}", response_model=AssignPatientIdResp)
def method_get_patient_by_id(index: int):
    if 0 <= index < len(app.patient_data):
        return AssignPatientIdResp(id=app.patient_data[index]["id"], patient=app.patient_data[index]["patient"])
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
