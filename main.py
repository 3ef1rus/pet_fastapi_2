from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root() -> dict:
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str) -> dict:
    return {"message": f"Hello {name}"}


users = [
    {"id": 1, "name": "Alice", "age": 30},
    {"id": 2, "name": "Bob", "age": 25},
    {"id": 3, "name": "Charlie", "age": 35},
]


@app.get("/users/{user_id}")
async def get_user(user_id: int) -> dict:
    curr_user = [user for user in users if user.get("id") == user_id]
    return curr_user[0]


@app.get("/users")
async def get_users() -> list[dict]:
    return users
