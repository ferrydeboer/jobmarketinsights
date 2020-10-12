from datetime import datetime

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
