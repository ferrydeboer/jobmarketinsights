import os
from datetime import datetime
from unittest import TestCase

from fastapi.testclient import TestClient

from .overrides import override_get_db  # noqa F401

from jomai.main import app
from jomai.models import Job
# If imported before main models.Job wil overwrite schema job.
from jomai.schemas.job import JobCreate, JobsList, Job as SchemaJob
from .data import default


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
        response = self.client.post("/jobs/", njjson)

        # result: SchemaJob = SchemaJob.parse_raw(response.content)
        assert response.status_code == 201
        # assert result.id >= 1
        # assert result.title == newjob.title

    def test_get_jobs(self):
        response = self.client.get("/jobs")

        assert response.status_code == 200
        result: JobsList = JobsList.parse_raw(response.content)
        assert len(result.__root__) == 3
        for job in result.__root__:
            assert job.title is not None

    def test_get_job(self):
        expected = default.jobs()[0]
        response = self.client.get("/jobs/1")
        assert response.status_code == 200
        actual: SchemaJob = SchemaJob.parse_raw(response.content)
        assert expected.title == actual.title
        # assert expected.posted_on == actual.posted_on
        assert expected.location == actual.location

    def test_import_jobs(self):
        self.set_test_jobs()

        # run code
        datapath = os.path.join(os.path.dirname(__file__), 'data', "python.html")

        with open(datapath, "rb") as file:
            files = {"file": ("python.html", file, "text/html")}
            payload = {
                "keyword": "python"}
            response = self.client.put(
                "/jobs/flsearch/",
                data=payload,
                files=files
            )

        assert response.status_code == 200
        changes = response.json()
        assert len(changes["new"]) == 1
        assert len(changes["updated"]) == 1
        assert changes["processed"] == 3

        default.extra_jobs = []

    def set_test_jobs(self):
        unchanged = Job(
            url="https://www.freelance.nl/opdracht/900882-bi-sas-specialist",
            title="BI/SAS specialist",
            location="Apeldoorn",
            posted_on=datetime.now(),
            applications=0)
        changed = Job(
            url="https://www.freelance.nl/opdracht/900815-aws-machine-learning",
            title="AWS Machine Learning ",
            location="Remote/Amsterdam",
            posted_on=datetime.now(),
            applications=0)
        default.extra_jobs += [unchanged, changed]
