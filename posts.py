from fastapi import FastAPI, status
from database import Base, engine, Posts
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

#create request base model
class PostsRequest(BaseModel):
    userID: str
    postNumber: int
    postContent: str


# Create the database
Base.metadata.create_all(engine)

#Initialize app
app = FastAPI()

@app.get("/")
def root():
    return "post"

@app.post("/post", status_code=status.HTTP_201_CREATED)
def create_post(post: PostsRequest):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # create an instance of the database model
    postdb = Posts(postContent = post.postContent,
                    userID = post.userID,
                    postNumber = post.postNumber)

    # add it to the session and commit it
    session.add(postdb)
    session.commit()

    # close the session
    session.close()

    # return response
    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "message": "success"
        })


@app.get("/post/{postNumber}")
def read_post(postNumber: int):
 # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the item with the given username
    postGet = session.query(Posts).get(postNumber)

    # close the session
    session.close()

    if not postGet:
        raise HTTPException(status_code=404, detail=f"post {postNumber} not found")

    return f"Post Number: {postGet.postNumber} Admin: {postGet.userID} Post Content: {postGet.postContent}"

@app.put("/post/{postNumber}")
def update_post(postNumber: int, userID: str, postContent: str):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the info with the given username
    postUpdate = session.query(Posts).get(postNumber)

    # update todo item with the given task (if an item with the given id was found)
    if postUpdate:
        postUpdate.postContent = postContent

        session.commit()

    # close the session
    session.close()

    # check if todo item with given id exists. If not, raise exception and return 404 not found response
    if not postUpdate:
        raise HTTPException(status_code=404, detail=f"post {postNumber} not found")

    return postUpdate


@app.delete("/post/{postNumber}")
def delete_post(postNumber: int):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the item with the given post number
    postDelete = session.query(Posts).get(postNumber)

    # if todo item with given id exists, delete it from the database. Otherwise raise 404 error
    if postDelete:
        session.delete(postDelete)
        session.commit()
        session.close()
    else:
        raise HTTPException(status_code=404, detail=f"post {postNumber} not found")

    return None

@app.get("/post")
def read_post_list():
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get all user items
    post_list = session.query(Posts).all()

    # close the session
    session.close()

    return post_list

