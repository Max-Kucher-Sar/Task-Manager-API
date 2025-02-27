from typing import Optional

from pydantic import BaseModel


class CreateUser(BaseModel):
    username: str
    firstname: str
    lastname: str
    age: int


class UpdateUser(BaseModel):
    firstname: str
    lastname: str
    age: int


class UserOut(BaseModel):
    id: int
    username: str
    firstname: Optional[str]
    lastname: Optional[str]
    age: Optional[int]

    class Config:
        orm_mode = True


class CreateTask(BaseModel):
    title: str
    content: str
    priority: int


class UpdateTask(BaseModel):
    title: str
    content: str
    priority: int