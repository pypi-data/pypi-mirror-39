from testing.postgresql import Postgresql
from sqlalchemy import create_engine
from triage.db import table_has_data


def test_table_has_data_if_true():
    with Postgresql() as postgresql:
        engine = create_engine(postgresql.url())
        engine.execute("create table compliments (col1 varchar)")
        engine.execute("insert into compliments values ('good job')")
        assert table_has_data("compliments", engine)


def test_table_has_data_if_missing():
    with Postgresql() as postgresql:
        engine = create_engine(postgresql.url())
        engine.execute("create table compliments (col1 varchar)")
        assert not table_has_data("compliments", engine)
