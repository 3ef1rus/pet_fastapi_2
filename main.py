from typing import List, Optional, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pyexpat.errors import messages

app = FastAPI()


class Work(BaseModel):
    id: int
    name: str
    salary: int


class User(BaseModel):
    id: int
    name: str
    age: int
    works: Optional[Work] = "unemployed"


class UserCreate(BaseModel):
    name: str
    age: int
    works_id: Optional[int] = None


works = [
    {"id": 1, "name": "Programmer", "salary": 3000},
    {"id": 2, "name": "Cleaner", "salary": 750},
    {"id": 3, "name": "Doctor", "salary": 2500},
]

users = [
    {"id": 1, "name": "Alice", "age": 30, "works": works[0]},
    {"id": 2, "name": "Bob", "age": 25, "works": works[1]},
    {"id": 3, "name": "Charlie", "age": 35, "works": works[2]},
]



@app.get("/users")
async def get_users() -> List[User]:
    # buff_objs = []
    # for user in users:
    #     buff_objs.append(User(id=user["id"], name=user["name"], age=user["age"]))
    # return buff_objs
    return [User(**user) for user in users]


@app.get("/users/search")
async def search_users(user_id: Optional[int] = None) -> Dict[str, Optional[User]]:
    if user_id:
        for user in users:
            if user["id"] == user_id:
                return {"data": User(**user)}
        raise HTTPException(status_code=404, detail="User Not Found")
    else:
        return {"data": None}


@app.post("/users/add", status_code=201)
async def add_user(user: UserCreate) -> User:
    new_id_user=len(users)+1
    work = next((w for w in works if w["id"] == user.works_id), None)
    if not work:
        raise HTTPException(status_code=404, detail="Work with ID not found")
    new_user = User(id=new_id_user, name=user.name, age=user.age, works=work)
    users.append(new_user.model_dump())
    return new_user


@app.put("/users/update/{user_id}")
async def update_user(user_id:int,user: UserCreate) -> User:
    for i, curr_user in enumerate(users):
        if curr_user.get("id") == user_id:
            # Update user fields (excluding unchanged values)
            curr_user.update(user.model_dump(exclude_unset=True))

            # Handle optional work update
            if user.works_id is not None:
                work = next((w for w in works if w.get("id") == user.works_id), None)
                if not work:
                    raise HTTPException(status_code=404, detail="Work with ID not found")
                curr_user["works"] = work

            # Persist the updated user (replace with your database/storage logic)
            users[i] = curr_user  # Update in-memory list (placeholder)

            return User(**curr_user)  # Return updated user object

    raise HTTPException(status_code=404, detail="User Not Found")


@app.get("/users/{user_id}")
async def get_user(user_id: int) -> User:
    # curr_user = [user for user in users if user.get("id") == user_id]
    for user in users:
        if user["id"] == user_id:
            return User(**user)
    raise HTTPException(status_code=404, detail="User Not Found")


@app.delete("/users/{user_id}")
async def delete_user(user_id: int) -> None:
    for user in users:
        if user["id"] == user_id:
            users.pop(users.index(user))



