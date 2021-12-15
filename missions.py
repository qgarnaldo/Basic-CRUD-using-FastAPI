from fastapi import FastAPI, status
from database import Base, engine, Missions
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

#create request base model
class MissionRequest(BaseModel):
    userID: str
    missionNumber: int
    missionName: str
    missionDetails: str
    missionStart: datetime
    missionEnd: datetime

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

# Create the database
Base.metadata.create_all(engine)

#Initialize app
app = FastAPI()

@app.get("/")
def root():
    return "mission"

@app.post("/mission", status_code=status.HTTP_201_CREATED)
def create_mission(mission: MissionRequest):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # create an instance of the database model
    missiondb = Missions(missionDetails = mission.missionDetails,
                        userID = mission.userID,
                        missionNumber = mission.missionNumber,
                        missionName = mission.missionName,
                        missionStart = mission.missionStart,
                        missionEnd = mission.missionEnd)

    # add it to the session and commit it
    session.add(missiondb)
    session.commit()

    # close the session
    session.close()

    # return response
    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "message": "success"
        })


@app.get("/mission/{missionNumber}")
def read_mission(missionNumber: int):
 # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the item with the given username
    missionGet = session.query(Missions).get(missionNumber)

    # close the session
    session.close()

    if not missionGet:
        raise HTTPException(status_code=404, detail=f"mission {missionNumber} not found")

    return f"Mission Number: {missionGet.missionNumber} Admin: {missionGet.userID} Mission Name: {missionGet.missionName} Mission Details: {missionGet.missionDetails} Mission Start: {missionGet.missionStart} Mission End: {missionGet.missionEnd}"

@app.put("/mission/{missionNumber}")
def update_mission(missionNumber: int, userID: str, missionName: str, missionDetails: str, missionStart: datetime, missionEnd: datetime):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the info with the given username
    missionUpdate = session.query(Missions).get(missionNumber)

    # update todo item with the given task (if an item with the given id was found)
    if missionUpdate:
        missionUpdate.missionName = missionName
        missionUpdate.missionDetails = missionDetails
        missionUpdate.missionStart = missionStart
        missionUpdate.missionEnd = missionEnd

        session.commit()

    # close the session
    session.close()

    # check if todo item with given id exists. If not, raise exception and return 404 not found response
    if not missionUpdate:
        raise HTTPException(status_code=404, detail=f"mission {missionNumber} not found")

    return missionUpdate


@app.delete("/mission/{missionNumber}")
def delete_mission(missionNumber: int):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the item with the given post number
    missionDelete = session.query(Missions).get(missionNumber)

    # if todo item with given id exists, delete it from the database. Otherwise raise 404 error
    if missionDelete:
        session.delete(missionDelete)
        session.commit()
        session.close()
    else:
        raise HTTPException(status_code=404, detail=f"mission {missionNumber} not found")

    return None

@app.get("/mission")
def read_mission_list():
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get all user items
    mission_list = session.query(Missions).all()

    # close the session
    session.close()

    return mission_list

