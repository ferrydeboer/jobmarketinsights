import unittest
from datetime import datetime

from parameterized import parameterized

from jomai.models import Job


class JobTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.original: Job = Job(
            url="https://my.dream.job/123",
            title="My dream job",
            location="Amsterdam",
            applications=10,
            posted_on=datetime.now())

    @parameterized.expand([
        ("title", "new title"),
        ("applications", 23),
        ("location", "New Amsterdam")
    ])
    def test_has_changed(self, field, new_value):
        fields = vars(self.original)

        job_fields = {k: v for (k, v) in fields.items() if not k.startswith('_')}
        job_fields[field] = new_value
        changed: Job = Job(**job_fields)

        assert changed.has_changed(self.original)

    def test_should_raise_different_urls(self):
        with self.assertRaises(ValueError):
            other = Job(url="https://notmy.dream.job/0")
            self.original.has_changed(other)
