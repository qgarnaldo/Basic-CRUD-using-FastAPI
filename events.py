from fastapi import FastAPI, status
from database import Base, engine, Events
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

#create request base model
class EventRequest(BaseModel):
    userID: str
    eventNumber: int
    eventName: str
    eventDetails: str
    eventStart: datetime
    eventEnd: datetime


# Create the database
Base.metadata.create_all(engine)

#Initialize app
app = FastAPI()

@app.get("/")
def root():
    return "event"

@app.post("/event", status_code=status.HTTP_201_CREATED)
def create_event(event: EventRequest):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # create an instance of the database model
    eventdb = Events(eventDetails = event.eventDetails,
                     userID = event.userID,
                     eventNumber = event.eventNumber,
                     eventName = event.eventName,
                     eventStart = event.eventStart,
                     eventEnd = event.eventEnd)

    # add it to the session and commit it
    session.add(eventdb)
    session.commit()

    # close the session
    session.close()

    # return response
    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "message": "success"
        })


@app.get("/event/{eventNumber}")
def read_event(eventNumber: int):
 # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the item with the given username
    eventGet = session.query(Events).get(eventNumber)

    # close the session
    session.close()

    if not eventGet:
        raise HTTPException(status_code=404, detail=f"event {eventNumber} not found")

    return f"Event Number: {eventGet.eventNumber} Admin: {eventGet.userID} Event Name: {eventGet.eventName} Event Details: {eventGet.eventDetails} Event Start: {eventGet.eventStart} Event End: {eventGet.eventEnd}"

@app.put("/event/{eventNumber}")
def update_event(eventNumber: int, userID: str, eventName: str, eventDetails: str, eventStart: datetime, eventEnd: datetime):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the info with the given username
    eventUpdate = session.query(Events).get(eventNumber)

    # update todo item with the given task (if an item with the given id was found)
    if eventUpdate:
        eventUpdate.eventName = eventName
        eventUpdate.eventDetails = eventDetails
        eventUpdate.eventStart = eventStart
        eventUpdate.eventEnd = eventEnd

        session.commit()

    # close the session
    session.close()

    # check if todo item with given id exists. If not, raise exception and return 404 not found response
    if not eventUpdate:
        raise HTTPException(status_code=404, detail=f"event {eventNumber} not found")

    return eventUpdate


@app.delete("/event/{eventNumber}")
def delete_event(eventNumber: int):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the item with the given post number
    eventDelete = session.query(Events).get(eventNumber)

    # if todo item with given id exists, delete it from the database. Otherwise raise 404 error
    if eventDelete:
        session.delete(eventDelete)
        session.commit()
        session.close()
    else:
        raise HTTPException(status_code=404, detail=f"event {eventNumber} not found")

    return None

@app.get("/event")
def read_event_list():
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get all user items
    event_list = session.query(Events).all()

    # close the session
    session.close()

    return event_list

