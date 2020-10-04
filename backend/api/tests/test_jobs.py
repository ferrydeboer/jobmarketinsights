from unittest import TestCase

from fastapi.testclient import TestClient

from jomai.main import Job, app, jobs


class JobsTest(TestCase):

    client = TestClient(app)

    def setUp(self) -> None:
        self.test_job = Job(title="Tester", url="https://www.testers.jobs/123")
        jobs[1] = self.test_job

    def test_get_job_404(self):
        response = self.client.get("/jobs/2")
        assert response.status_code == 404

    def test_get_job(self):
        response = self.client.get("/jobs/1")
        assert response.status_code == 200
        job: Job = Job.parse_raw(response.content)
        assert job.title == self.test_job.title
        assert job.url == self.test_job.url
