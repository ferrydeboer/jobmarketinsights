import threading

from sqlalchemy import event, create_engine
from sqlalchemy.orm import sessionmaker

from jomai.db import Base
# .core_mocks needs to be imported before get_session!
from .core_mocks import *  # noqa F401
from jomai.db.session import get_session
from jomai.main import app
from jomai.models import Job

from .data import default

engine = create_engine("sqlite://",
                       pool_pre_ping=True,
                       echo=True,
                       pool_size=1,  # Sort of fixes tests when running together
                       # could still make subsequent tests fail if the run on same
                       # thread
                       connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        # Probably only has to be done once.
        db = TestingSessionLocal()
        yield db
    finally:
        tid = threading.currentThread().ident
        print(f"Closing session on {tid}")
        db.close()


app.dependency_overrides[get_session] = override_get_db


@event.listens_for(engine, "engine_connect")
# i was expecting connect to work. But then the tables is not existing on
# the actual commits. This gets called very often which I still wouldn't expect.
# but for now it seems to work atleast.
def on_engine_connect(dbapi_connection, connection_record):
    print("Engine Connect")


@event.listens_for(engine, 'checkout')
def my_on_checkout(dbapi_conn, connection_rec, connection_proxy):
    print("Engine checkout")
    SchemaBuilder.create_tables(dbapi_conn, connection_rec)


class SchemaBuilder:
    creating_tables = False

    @staticmethod
    def create_tables(dbapi_connection, connection_record):
        query = """SELECT name \
        FROM sqlite_master\
        WHERE type ='table' AND\
        name NOT LIKE 'sqlite_%';"""

        rs = dbapi_connection.execute(query)
        if rs.rowcount <= 0 and not SchemaBuilder.creating_tables:
            SchemaBuilder.creating_tables = True
            tid = threading.currentThread().ident
            print(f"Creating schema from {tid}")
            Base.metadata.create_all(bind=engine)
            SchemaBuilder.insert_testdata()
            SchemaBuilder.creating_tables = False

    @staticmethod
    def insert_testdata():
        session = next(override_get_db())
        cnt = session.query(Job.title).count()
        print(f"Found {cnt} jobs")
        if cnt <= 0:
            print(f"Inserting {len(default.jobs())} test jobs")
            jobs = default.jobs()
            session.add_all(jobs)
            session.commit()

            # for job in data.jobs.values():
            #     session.refresh(job)
