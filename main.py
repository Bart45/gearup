import sqlite3

from fastapi import FastAPI, status, Response, Cookie, HTTPException

from fastapi.responses import JSONResponse

from pydantic import BaseModel

from typing import Dict

from hashlib import sha256

app = FastAPI()
app.count = 0
app.patient_data = []


class Patient(BaseModel):
    name: str
    surename: str


class AssignPatientIdResp(BaseModel):
    id: int
    patient: Dict

@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect('chinook.db')


@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()


@app.get("/welcome")
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


@app.get("/tracks/{page = 0}/{per_page = 10}")
async def method_get_tracks(page: int, per_page: int):
    app.db_connection.row_factory = sqlite3.Row
    cursor = app.db_connection.cursor()
    offset = page * per_page
    tracks = cursor.execute(
        "SELECT * FROM tracks ORDER BY TrackId LIMIT ? OFFSET ?",
        (per_page, offset - 1)).fetchall()
    return tracks
