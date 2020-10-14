from sqlalchemy import event

from jomai.db import Base
from .core_mocks import *  # noqa F401
from jomai.db.session import get_session, engine, SessionLocal
from jomai.main import app


@event.listens_for(engine, "engine_connect")
# i was expecting connect to work. But then the tables is not existing on
# the actual commits. This gets called very often which I still wouldn't expect.
# but for now it seems to work atleast.
def on_engine_connect(dbapi_connection, connection_record):
    SchemaBuilder.create_tables(dbapi_connection, connection_record)


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
            Base.metadata.create_all(bind=engine)
            SchemaBuilder.creating_tables = False


def override_get_db():
    try:
        # Probably only has to be done once.
        db = SessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_session] = override_get_db
