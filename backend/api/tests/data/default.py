from datetime import datetime, timedelta
from typing import List

from jomai.models import Job


# Due to single threading the data for tests needs to be inserted in the thread running the API.
# Sticking with some default test data for now will suffice.
def jobs() -> List[Job]:
    return [
        Job(
            title="Developer",
            url="https://www.dream.jobs/1",
            location="Amsterdam",
            posted_on=datetime.now()),
        Job(
            title="Tester",
            url="https://www.dream.jobs/2",
            location="Rotterdam",
            posted_on=datetime.now() - timedelta(days=2)),
        Job(
            title="DevOps Engineer",
            url="https://www.dream.jobs/3",
            location="Utrecht",
            posted_on=datetime.now() - timedelta(days=1)),
    ] + extra_jobs


extra_jobs: List[Job] = []
