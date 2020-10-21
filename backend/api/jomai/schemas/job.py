from datetime import datetime
from typing import List

from pydantic import BaseModel


class JobBase(BaseModel):
    title: str
    url: str
    location: str
    posted_on: datetime


class JobCreate(JobBase):
    pass


class Job(JobBase):
    id: int

    class Config:
        orm_mode = True


# got this from here
# https://stackoverflow.com/questions/58068001/python-pydantic-using-a-list-with-json-objects
class JobsList(BaseModel):
    __root__: List[Job]
