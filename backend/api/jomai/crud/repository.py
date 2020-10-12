from fastapi import Depends
from sqlalchemy.orm import Session

from jomai.db.session import get_session
from jomai.models import Job


class Repository:
    session: Session

    def __init__(self, session: Session = Depends(get_session)):
        # maybe the issue is that this Repository is shared over requests.
        self.session = session

    def get_job(self, job_id: int):
        return self.session.query(Job).filter(Job.id == job_id).first()

    def add_job(self, job: Job):
        self.session.add(job)
        # I wouldn't commit on every db operation.
        self.session.commit()
        # If you want to refresh the data for returning it
        # some middleware for the commit and possibly refreshing
        # the return value is a better way to go. Provided the
        # return value from the path operation is available for
        # inspection.
        self.session.refresh(job)
        return job
