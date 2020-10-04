from typing import Dict, Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


class Job(BaseModel):
    title: str = Field(
        title="The title of the job description", description="Need I say more?"
    )
    url: str


app = FastAPI()
jobs: Dict = {}
# {1: Job(title="Tester", url="https://www.testers.jobs/123")}


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/jobs/{job_id}", response_model=Job)
async def read_job(job_id: int, q: Optional[str] = None):
    if job_id not in jobs.keys():
        raise HTTPException(status_code=404, detail="Job does not exist")
    return jobs[job_id]


@app.post("/jobs")
def add_job(job: Job):
    """Add a new jobs and returns id"""

    ids = jobs.keys()
    job_id = 1
    if ids:
        job_id = max(ids) + 1

    jobs[job_id] = job
    return job_id


@app.put("/jobs/{job_id")
def update_job(job_id: int, job: Job):
    """Updates the jobs with given job_id"""
    return {"job_name": job.title, "job_id": job_id}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
