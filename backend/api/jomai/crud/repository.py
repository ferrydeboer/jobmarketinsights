from sqlalchemy.orm import Session

from jomai.models import Job


class Repository:
    # session: Session

    # def __init__(self, session: Session = Depends(get_session)):
    #     # maybe the issue is that this Repository is shared over requests.
    #     self.session = session

    @staticmethod
    def get_job(job_id: int, session: Session):
        return session.query(Job).filter(Job.id == job_id).first()

    @staticmethod
    def add_job(job: Job, session: Session):
        session.add(job)
        # I wouldn't commit on every db operation.
        session.commit()
        # If you want to refresh the data for returning it
        # some middleware for the commit and possibly refreshing
        # the return value is a better way to go. Provided the
        # return value from the path operation is available for
        # inspection.
        session.refresh(job)
        return job
