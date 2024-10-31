from typing import List, Optional, Dict, Annotated
from fastapi import FastAPI, HTTPException, Path, Query, Body, Depends
from sqlalchemy.orm import Session
from models import Base,User,Work
from database import engine,session_local
from schemas import UserCreate,WorkCreate,User as DbUser,Work as DbWork
app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db=session_local()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/create",status_code=201,response_model=DbUser)
async def create_user(user: UserCreate, db: Session = Depends(get_db))->DbUser:
    db_user=User(name=user.name,age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@app.post("/works/create",status_code=201,response_model=DbWork)
async def create_work(work: WorkCreate, db: Session = Depends(get_db))->Work:
    db_user = db.query(User).filter(User.id == work.user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_work=Work(name=work.name,salary=work.salary,user_id=work.user_id)
    db.add(db_work)
    db.commit()
    db.refresh(db_work)

    return db_work

