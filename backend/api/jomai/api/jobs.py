from fastapi import APIRouter, Depends, HTTPException, Path, File, Form
from sqlalchemy.orm import Session

from jomai.crud.repository import Repository
from jomai.db.session import get_session
from jomai.models import Job
from jomai.parsers.freelancenl import FreelanceNl
from jomai.schemas import job as job_schemas

router = APIRouter()


@router.get("/", response_model=job_schemas.JobsList)
async def get_jobs(session: Session = Depends(get_session)):
    jobs = Repository.get_jobs(session)
    return jobs


@router.get("/{job_id}", response_model=job_schemas.Job)
async def read_job(job_id: int,
                   session: Session = Depends(get_session)):
    job = Repository.get_job(job_id, session)
    if not job:
        raise HTTPException(status_code=404, detail="Job does not exist")
    return job


@router.post("/", response_model=job_schemas.Job, status_code=201)
def add_job(
        job: job_schemas.JobCreate,
        session: Session = Depends(get_session)):
    """Add a new jobs and returns id"""

    new_job = Job(**job.dict())
    # I far from like passing down dependencies manually and creating
    # unnecessary coupling.
    return Repository.add_job(new_job, session)


@router.put("/{job_id}")
def update_job(
        job: job_schemas.Job,
        job_id: int = Path(
            ...,
            title="The id of the job",
            description="Some more information",
            ge=1)):
    """Updates the jobs with given job_id"""
    return {"job_name": job.title, "job_id": job_id}


@router.put("/flsearch/")
def upload_jobs(file: bytes = File(..., title="Used keyword search results"),
                keyword: str = Form(..., title="Used keyword"),
                session: Session = Depends(get_session),
                parser: FreelanceNl = Depends(FreelanceNl)
                ):
    """Updates or adds jobs from a search result"""
    contents: str = file.decode("utf-8")
    jobs = []
    new = []
    updated = []
    processed = 0
    for job in parser.parse_content(contents):
        # find job (if found, update)
        existing = Repository.get_job_url(job.url, session)
        processed += 1
        if existing:
            if existing.has_changed(job):
                # should validate if really changed?
                # update with (new) values
                existing.title = job.title
                existing.applications = job.applications
                existing.location = job.location
                jobs.append(existing)
                updated.append(job.url)
        else:
            # insert
            # I don't want to commit on every result.
            # so preferably I add a bulk update function.
            jobs.append(job)
            new.append(job.url)

    response = {
        "new": new,
        "updated": updated,
        "processed": processed,
        "keyword": keyword
    }
    return response
