from fastapi import FastAPI, status
from database import Base, engine, Comments
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime, date
from fastapi import HTTPException

from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

#create request base model
class CommentRequest(BaseModel):
    userID: str
    commentNumber: int
    postID: int
    commentContents: str
    commentTime: datetime

# Create the database
Base.metadata.create_all(engine)

#Initialize app
app = FastAPI()

@app.get("/")
def root():
    return "comment"

@app.post("/comment", status_code=status.HTTP_201_CREATED)
def create_comment(comment: CommentRequest):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # create an instance of the database model
    commentdb = Comments(commentContents = comment.commentContents,
                         userID = comment.userID,
                         commentNumber = comment.commentNumber,
                         postID = comment.postID,
                         commentTime = date.today()
                         )

    # add it to the session and commit it
    session.add(commentdb)
    session.commit()

    # grab the username given to the object from the database
    userID = commentdb.userID

    # close the session
    session.close()

    # return response
    return JSONResponse(status_code=200, content={
        "status_code": 200,
        "message": "success"
        })



@app.get("/comment/{commentNumber}")
def read_comment(commentNumber: int):
 # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the item with the given username
    commentGet = session.query(Comments).get(commentNumber)

    # close the session
    session.close()

    if not commentGet:
        raise HTTPException(status_code=404, detail=f"comment {commentNumber} not found")

    return f"Comment Number: {commentGet.commentNumber} User: {commentGet.userID} Post ID: {commentGet.postID} Comment Content: {commentGet.commentContent} comment Time: {commentGet.commentTime} "

@app.put("/comment/{commentNumber}")
def update_comment(commentNumber: int, userID: str, postId: int, commentContent: str, commentTime: datetime):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the info with the given username
    commentUpdate = session.query(Comments).get(commentNumber)

    # update todo item with the given task (if an item with the given id was found)
    if commentUpdate:
        commentUpdate.commentContent = commentContent
        commentUpdate.commentTime = commentTime

        session.commit()

    # close the session
    session.close()

    # check if todo item with given id exists. If not, raise exception and return 404 not found response
    if not commentUpdate:
        raise HTTPException(status_code=404, detail=f"comment {commentNumber} not found")

    return commentUpdate


@app.delete("/comment/{commentNumber}")
def delete_comment(commentNumber: int):
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get the item with the given post number
    commentDelete = session.query(Comments).get(commentNumber)

    # if todo item with given id exists, delete it from the database. Otherwise raise 404 error
    if commentDelete:
        session.delete(commentDelete)
        session.commit()
        session.close()
    else:
        raise HTTPException(status_code=404, detail=f"comment {commentNumber} not found")

    return None

@app.get("/comment")
def read_comment_list():
    # create a new database session
    session = Session(bind=engine, expire_on_commit=False)

    # get all user items
    comment_list = session.query(Comments).all()

    # close the session
    session.close()

    return comment_list

