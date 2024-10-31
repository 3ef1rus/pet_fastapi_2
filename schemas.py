from typing import Optional, Annotated, Union

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    name: str
    age: int


class User(UserBase):
    id:int

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    pass


class WorkBase(BaseModel):
    name: Annotated[str, Field(..., min_length=2, title="Название работы")]
    salary: Annotated[int, Field(..., ge=0, title="Размер зарплаты")]
    user_id:int


class Work(WorkBase):
    id: int
    user:User

    class Config:
        from_attributes = True


class WorkCreate(WorkBase):
    pass




