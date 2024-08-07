from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()
users_db = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get("/users", response_model=List[User])
async def get_users() -> List[User]:
    return users_db


@app.post("/user/{username}/{age}", response_model=User)
async def post_user(user: User) -> User:
    user.id = len(users_db) + 1
    users_db.append(user)
    return user


@app.put("/user/{user_id}/{username}/{age}", response_model=User)
async def update_user(user_id: int, new_data: User = Body()) -> User:
    for user in users_db:
        if user.id == user_id:
            user.username = new_data.username
            user.age = new_data.age
            return user
    raise HTTPException(status_code=404, detail="User was not found")


@app.delete("/user/{user_id}", response_model=User)
async def delete_user(user_id: int) -> User:
    for user in users_db:
        if user.id == user_id:
            del_user = user
            users_db.remove(user)
            return del_user
    raise HTTPException(status_code=404, detail="User was not found")
