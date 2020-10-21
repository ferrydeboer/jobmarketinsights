from datetime import datetime, timedelta
from typing import Dict

from jomai.models import Job


# Due to single threading the data for tests needs to be inserted in the thread running the API.
# Sticking with some default test data for now will suffice.
def jobs() -> Dict:
    return {
        1: Job(
            title="Developer",
            url="https://www.dream.jobs/1",
            location="Amsterdam",
            posted_on=datetime.now()),
        2: Job(
            title="Tester",
            url="https://www.dream.jobs/2",
            location="Rotterdam",
            posted_on=datetime.now() - timedelta(days=2)),
        3: Job(
            title="DevOps Engineer",
            url="https://www.dream.jobs/3",
            location="Utrecht",
            posted_on=datetime.now() - timedelta(days=1)),
    }
