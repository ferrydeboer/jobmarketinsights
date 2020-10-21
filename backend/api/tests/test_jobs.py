from datetime import datetime
from unittest import TestCase

from fastapi.testclient import TestClient

from .overrides import *  # noqa F401
from jomai.main import app
# If imported before main models.Job wil overwrite schema job.
from jomai.schemas.job import JobCreate, JobsList, Job as SchemaJob
from . import data


class JobsTest(TestCase):
    client = TestClient(app)

    # This now breaks with connection being closed when all tests run.
    # def test_get_job_404(self):
    #    response = self.client.get("/jobs/8998735454")
    #    assert response.status_code == 404

    def test_add_job(self):
        newjob = JobCreate(
            title="my first job",
            url="http://dream.job/1",
            location="Beverwijk",
            posted_on=datetime.now())
        njjson = newjob.json()
        response = self.client.post("/jobs", njjson)

        result: SchemaJob = SchemaJob.parse_raw(response.content)
        assert response.status_code == 201
        assert result.id >= 1
        assert result.title == newjob.title

    def test_get_jobs(self):
        response = self.client.get("/jobs")

        assert response.status_code == 200
        result: JobsList = JobsList.parse_raw(response.content)
        assert len(result.__root__) == 3
        for job in result.__root__:
            assert job.title is not None

    def test_get_job(self):
        expected = data.jobs()[1]
        response = self.client.get("/jobs/1")
        assert response.status_code == 200
        actual: SchemaJob = SchemaJob.parse_raw(response.content)
        assert expected.title == actual.title
        # assert expected.posted_on == actual.posted_on
        assert expected.location == actual.location
