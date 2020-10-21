import uvicorn
from fastapi import FastAPI, HTTPException, Path, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from jomai.crud.repository import Repository
from jomai.db.session import get_session
from jomai.models import Job
from jomai.schemas import job as job_schemas

app = FastAPI()

origins = ["http://0.0.0.0:4200"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/jobs/{job_id}", response_model=job_schemas.Job)
async def read_job(job_id: int,
                   session: Session = Depends(get_session)):
    job = Repository.get_job(job_id, session)
    if not job:
        raise HTTPException(status_code=404, detail="Job does not exist")
    return job


@app.post("/jobs", response_model=job_schemas.Job, status_code=201)
def add_job(
        job: job_schemas.JobCreate,
        session: Session = Depends(get_session)):
    """Add a new jobs and returns id"""

    new_job = Job(**job.dict())
    # I far from like passing down dependencies manually and creating unnecessary coupling.
    # I can make repo functions static
    return Repository.add_job(new_job, session)


@app.put("/jobs/{job_id")
def update_job(
        job: job_schemas.Job,
        job_id: int = Path(
            ...,
            title="The id of the job",
            description="Some more information",
            ge=1)):
    """Updates the jobs with given job_id"""
    return {"job_name": job.title, "job_id": job_id}


if __name__ == "__main__":
    print("STARTING UVICORN THROUGH main.py")
    uvicorn.run("jomai.main:app", host="0.0.0.0", port=8000, reload=True)
