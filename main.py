from typing import List, Optional, Dict, Annotated, Type
from fastapi import FastAPI, HTTPException, Path, Query, Body, Depends
from sqlalchemy.orm import Session
from models import Base, UserDB, WorkDB
from database import engine, get_db
from schemas import UserCreate, WorkCreate, User, Work, UserUpdate, WorkUpdate

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.post("/works/create", response_model=Work)
async def create_work(work: WorkCreate, db: Session = Depends(get_db)) -> WorkDB:
    db_work = WorkDB(name=work.name, salary=work.salary)
    db.add(db_work)
    db.commit()
    db.refresh(db_work)
    return db_work


@app.post("/users/create", response_model=User)
async def create_user(user: UserCreate, db: Session = Depends(get_db)) -> UserDB:
    db_user = UserDB(name=user.name, age=user.age, work_id=user.work_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/works/", response_model=List[Work])
async def get_works(db: Session = Depends(get_db)) -> List[Type[WorkDB]]:
    return db.query(WorkDB).all()


@app.get("/users/", response_model=List[User])
async def get_users(db: Session = Depends(get_db)) -> list[Type[UserDB]]:
    return db.query(UserDB).all()


@app.put("/users/update/{user_id}", response_model=User)
async def update_user(
    user_id: int, user: UserUpdate, db: Session = Depends(get_db)
) -> Type[UserDB]:
    curr_user = db.query(UserDB).filter(UserDB.id == user_id).first()

    if curr_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(curr_user, key, value)
    db.add(curr_user)
    db.commit()
    db.refresh(curr_user)
    return curr_user


@app.put("/works/update/{work_id}", response_model=Work)
async def update_work(
    work_id: int, work: WorkUpdate, db: Session = Depends(get_db)
) -> Type[WorkDB]:
    curr_work = db.query(WorkDB).filter(WorkDB.id == work_id).first()
    if curr_work is None:
        raise HTTPException(status_code=404, detail="Work not found")

    for key, value in work.model_dump(exclude_unset=True).items():
        setattr(curr_work, key, value)

    db.add(curr_work)
    db.commit()
    db.refresh(curr_work)
    return curr_work


@app.delete("/works/delete/{work_id}")
async def delete_work(work_id: int, db: Session = Depends(get_db)) -> dict:
    curr_work = db.query(WorkDB).filter(WorkDB.id == work_id).first()
    if curr_work is None:
        raise HTTPException(status_code=404, detail="Work not found")
    db.delete(curr_work)
    db.commit()
    return {"message": "Work deleted"}
