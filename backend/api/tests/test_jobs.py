from datetime import datetime
from unittest import TestCase

from fastapi.testclient import TestClient

from jomai.schemas.job import JobCreate, Job
from .overrides import *  # noqa F401
from jomai.main import app


class JobsTest(TestCase):

    client = TestClient(app)

    def test_get_job_404(self):
        response = self.client.get("/jobs/8998735454")
        assert response.status_code == 404

    def test_add_job(self):
        newjob = JobCreate(
            title="my first job",
            url="http://dream.job/1",
            location="Beverwijk",
            posted_on=datetime.now())
        njjson = newjob.json()
        response = self.client.post("/jobs", njjson)

        result: Job = Job.parse_raw(response.content)
        assert response.status_code == 201
        assert result.id >= 1
        assert result.title == newjob.title

    # def test_get_job(self):
    #     response = self.client.get("/jobs/1")
    #     assert response.status_code == 200
    #     job: Job = Job.parse_raw(response.content)
    #     assert job.title == self.test_job.title
    #     assert job.url == self.test_job.url
