from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


#created an engine instance of the mysql database
#and connecting database to fastAPI
engine = create_engine("mysql://root:root@localhost:3306/celebal")
Base = declarative_base()
Base.metadata.create_all(engine)

#created all the model (class) attributes
class StudM(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256))
    age = Column(Integer)
    email = Column(String(128))

#created a Pydantic Model
class Stud(BaseModel):
    name: str
    age: int
    email: str

#initializing FastAPI
app = FastAPI()

#API for creating new student record
@app.post("/newstud")
def newStud(student:Stud):
    #create a new database session
    session = Session(bind=engine)
    #create an instance of the database in the model
    student = StudM(name = student.name, age = student.age, email = student.email)
    # add and commit student into the session
    session.add(student)
    session.commit()
    session.refresh(student)
    session.close()
    return student

#API for showing student record for given id
@app.get("/stud/{id}")
def readStud(id: int):
    # create a new database session
    session = Session(bind=engine)
    # Read the student record with the given id
    student = session.query(StudM).get(id)
    session.close()
    return student

#API for Updating student record with a given id
@app.put("/studUpdate/{id}")
def updateStud(id: int, name: str, age: int, email: str):
    #create a new database session
    session = Session(bind=engine, expire_on_commit=False)
    #get student records for given id
    student = session.query(StudM).get(id)
    #update student with the given id
    if student:
        student.name = name
        student.age = age
        student.email = email
        session.commit()
        session.close()
    #if record is not found throw error
    else:
        raise HTTPException(status_code=404)    
    return student

#API for deleting student record with a given id
@app.delete("/studDel/{id}")
def deleteStud(id: int):
    #create a new database session
    session = Session(bind=engine)
    #get the student records given id
    student = session.query(StudM).get(id)
    #delete the records for given id
    if student:
        session.delete(student)
        session.commit()
        session.close()
    else:
        #if id is not found throw error
        raise HTTPException(status_code=404)
    return "Student record deleted"

#API for displaying all student records
@app.get("/studAll")
def allStud():
    # create a new database session
    session = Session(bind=engine)
    #get records of all the students
    students = session.query(StudM).all()
    # close the session
    session.close()
    return students
