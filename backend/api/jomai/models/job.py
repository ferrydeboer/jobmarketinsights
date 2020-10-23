from jomai.db.base_class import Base
from sqlalchemy import Column, DateTime, Integer, String


class Job(Base):
    """
    A Job post on a particular platform.
    """

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    url = Column(String, nullable=False)
    location = Column(String)
    applications = Column(Integer, nullable=True)
    posted_on = Column(DateTime, nullable=False)

    def has_changed(self, other):
        """
        :param other: the other/original instance
        :return: True of one of applicable fields has changed
        given it's the same object!
        :raises ValueError if job with different url is given.
        """
        if self.url != other.url:
            raise ValueError("Expecting both to be have the same url!")

        title = self.title != other.title
        location = self.location != other.location
        applications = self.applications != other.applications
        result = title or \
            location or \
            applications
        return result
