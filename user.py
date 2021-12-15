from fastapi import FastAPI, status
from database import Base, engine, UserInfo
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime, date
from fastapi import HTTPException

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

#create user request base model
class UserRequest(BaseModel):
    username: str
    email: str
    password: str
    userType: str
    firstName: str
    lastName: str
    middleInitial: str
    registrationDate: datetime
    mobileNumber: int


# Create the database
Base.metadata.create_all(engine)

#Initialize app
app = FastAPI()

@app.get("/")
def root():
    return "user"

@app.post("/user", status_code=status.HTTP_201_CREATED)
def create_user(user: UserRequest):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # create an instance of the database model
    userdb = UserInfo(username = user.username,
                email = user.email,
                password = user.password,
                userType = user.userType,
                firstName = user.firstName,
                lastName = user.lastName,
                middleInitial = user.middleInitial,
                registrationDate = date.today(),
                mobileNumber = user.mobileNumber
                )

    # add it to the session and commit it
    session.add(userdb)
    session.commit()
    session.close()

    
    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "message": "success"
        })



@app.get("/user/{username}")
def read_user(username: str):
 # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the item with the given username
    gocollab = session.query(UserInfo).get(username)

    # close the session
    session.close()

    if not gocollab:
        raise HTTPException(status_code=404, detail=f"username {username} not found")

    return f"username: {gocollab.username} email: {gocollab.email} password: {gocollab.password} userType: {gocollab.userType} firstName: {gocollab.firstName} lastName: {gocollab.lastName} middleInitial: {gocollab.middleInitial} registrationDate: {gocollab.registrationDate} mobileNumber: {gocollab.mobileNumber}"

@app.put("/user/{username}")
def update_user(username: str, email: str, password: str, userType: str, firstName: str, lastName: str, middleInitial: str, mobileNumber: int):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the info with the given username
    gocollab = session.query(UserInfo).get(username)

    # update todo item with the given task (if an item with the given id was found)
    if gocollab:
        gocollab.email = email
        gocollab.password = password
        gocollab.userType = userType
        gocollab.firstName = firstName
        gocollab.lastName = lastName
        gocollab.middleInitial = middleInitial
        gocollab.mobileNumber = mobileNumber

        session.commit()

    # close the session
    session.close()

    # check if todo item with given id exists. If not, raise exception and return 404 not found response
    if not gocollab:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

    return gocollab


@app.delete("/user/{username}")
def delete_user(username: str):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the todo item with the given id
    userdel = session.query(UserInfo).get(username)

    # if todo item with given id exists, delete it from the database. Otherwise raise 404 error
    if userdel:
        session.delete(userdel)
        session.commit()
        session.close()
    else:
        raise HTTPException(status_code=404, detail=f"username {username} not found")

    return None

@app.get("/user")
def read_user_list():
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get all user items
    user_list = session.query(UserInfo).all()

    # close the session
    session.close()

    return user_list