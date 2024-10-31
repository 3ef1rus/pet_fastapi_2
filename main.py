from typing import List, Optional, Dict, Annotated
from fastapi import FastAPI, HTTPException, Path, Query, Body, Depends
from sqlalchemy.orm import Session
from models import Base,User,Work
from database import engine,session_local
from schemas import UserCreate,WorkCreate,WorkResponse,User as DbUser
app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db=session_local()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/create",status_code=201,response_model=DbUser)
async def create_user(user: UserCreate, db: Session = Depends(get_db))->User:
    db_user=User(name=user.name,age=user.age)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

