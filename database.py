from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

# Create a sqlite engine instance
engine = create_engine("sqlite:///gocollab.db")

# Create a DeclarativeMeta instance
Base = declarative_base()

# Define User class inheriting from Base
class UserInfo(Base):
    __tablename__ = 'user'
    username = Column(String(50), primary_key=True)
    email = Column(String(50))
    password = Column(String(50))
    userType = Column(String(50))
    firstName = Column(String(50))
    lastName = Column(String(50))
    middleInitial = Column(String(50))
    registrationDate = Column(DateTime, server_default=func.now())
    mobileNumber = Column(Integer)

class Posts(Base):
    __tablename__='posts'
    postNumber = Column(Integer, primary_key=True)
    userID = Column(String(50), ForeignKey("user.username") )
    postContent = Column(String)

class Missions(Base):
    __tablename__='missions'
    missionNumber = Column(Integer, primary_key=True)
    userID = Column(String(50), ForeignKey("user.username") )
    missionName = Column(String)
    missionDetails = Column(String)
    missionStart = Column(DateTime)
    missionEnd = Column(DateTime)

class Events(Base):
    __tablename__='events'
    eventNumber = Column(Integer, primary_key=True)
    userID = Column(String(50), ForeignKey("user.username") )
    eventName = Column(String)
    eventDetails = Column(String)
    eventStart = Column(DateTime)
    eventEnd = Column(DateTime)

class Comments(Base):
    __tablename__='comments'
    commentNumber = Column(Integer, primary_key=True)
    userID = Column(String(50), ForeignKey("user.username") )
    postID = Column(Integer, ForeignKey("posts.postNumber") )
    commentContents = Column(String)
    commentTime = Column(DateTime)
