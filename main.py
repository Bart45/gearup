import sqlite3

from fastapi import FastAPI, status, Response, Cookie, HTTPException, Request

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


@app.get("/tracks")
async def method_get_tracks(request: Request):
    page = 0
    per_page = 10
    if request.query_params.__contains__("page"):
        page = int(request.query_params.get("page"))
    if request.query_params.__contains__("per_page"):
        per_page = int(request.query_params.get("per_page"))

    app.db_connection.row_factory = sqlite3.Row
    cursor = app.db_connection.cursor()
    offset = page * per_page
    tracks = cursor.execute(
        "SELECT * FROM tracks ORDER BY TrackId LIMIT ? OFFSET ?",
        (per_page, offset - 1)).fetchall()
    return tracks


@app.get("/tracks/composers")
async def method_get_composers_tracks(request: Request):
    if request.query_params.__contains__("composer_name"):
        composer = request.query_params.get("composer_name")
    else:
        return JSONResponse(status_code=status.HTTP_412_PRECONDITION_FAILED)

    app.db_connection.row_factory = lambda cursor, x: x[0]
    cursor = app.db_connection.cursor()
    if composer in cursor.execute("SELECT DISTINCT Composer FROM tracks").fetchall():

        composer_tracks = cursor.execute(
            "SELECT Name FROM tracks WHERE Composer = ? ORDER BY Name ",
            (composer, )).fetchall()
    else:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND)

    return composer_tracks
