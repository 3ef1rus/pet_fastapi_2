from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    id: int
    name: str
    age: int


users = [
    {"id": 1, "name": "Alice", "age": 30},
    {"id": 2, "name": "Bob", "age": 25},
    {"id": 3, "name": "Charlie", "age": 35},
]


@app.get("/users")
async def get_users() -> List[User]:
    # buff_objs = []
    # for user in users:
    #     buff_objs.append(User(id=user["id"], name=user["name"], age=user["age"]))
    # return buff_objs
    return [User(**user) for user in users]


@app.get("/users/{user_id}")
async def get_user(user_id: int) -> dict:
    # curr_user = [user for user in users if user.get("id") == user_id]
    for user in users:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User Not Found")


# @app.post("/users", status_code=201)
# async def create_user(user: [User]):
#     users.extend(user)


@app.delete("/users/{user_id}")
async def delete_user(user_id: int) -> None:
    for user in users:
        if user["id"] == user_id:
            users.pop(users.index(user))
