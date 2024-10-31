from typing import Optional, Annotated

from pydantic import BaseModel, Field


class WorkBase(BaseModel):
    name: Annotated[str, Field(..., min_length=2, title="Название работы")]
    salary: Annotated[int, Field(..., ge=0, title="Размер зарплаты")]
    user_id:int

class WorkResponse(WorkBase):
    id: int

    class Config:
        from_attributes = True


class WorkCreate(BaseModel):
    pass


class UserBase(BaseModel):
    name: str
    age: int
    works: Optional[int] = "unemployed"


class User(UserBase):
    id:int

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    pass


