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
    posted_on = Column(DateTime, nullable=False)
