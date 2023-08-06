from datetime import datetime
from testing.postgresql import Postgresql
from sqlalchemy import create_engine
from triage.cohort import CohortTableGenerator
from . import utils
import pytest

def test_cohort_table_generator():
    input_data = [
        # entity_id, outcome_date, outcome
        (1, datetime(2016, 1, 1), True),
        (1, datetime(2016, 4, 1), False),
        (1, datetime(2016, 3, 1), True),
        (2, datetime(2016, 1, 1), False),
        (2, datetime(2016, 1, 1), True),
        (3, datetime(2016, 1, 1), True),
        (5, datetime(2016, 3, 1), True),
        (5, datetime(2016, 4, 1), True),
    ]
    with Postgresql() as postgresql:
        engine = create_engine(postgresql.url())
        utils.create_binary_outcome_events(engine, "events", input_data)
        table_generator = CohortTableGenerator(
            query="select entity_id from events where outcome_date < '{as_of_date}'::date",
            db_engine=engine,
            cohort_table_name="exp_hash_cohort",
        )
        as_of_dates = [datetime(2016, 1, 1), datetime(2016, 2, 1), datetime(2016, 3, 1)]

        table_generator.generate_cohort_table(as_of_dates)
        expected_output = [
            (1, datetime(2016, 2, 1)),
            (1, datetime(2016, 3, 1)),
            (2, datetime(2016, 2, 1)),
            (2, datetime(2016, 3, 1)),
            (3, datetime(2016, 2, 1)),
            (3, datetime(2016, 3, 1)),
        ]
        results = list(
            engine.execute(
                f"""
                select entity_id, as_of_date from {table_generator.cohort_table_name}
                order by entity_id, as_of_date
            """
            )
        )
        assert results == expected_output


    with Postgresql() as postgresql:
        engine = create_engine(postgresql.url())
        utils.create_binary_outcome_events(engine, "events", [])
        table_generator = CohortTableGenerator(
            query="select entity_id from events where outcome_date < '{as_of_date}'::date",
            db_engine=engine,
            cohort_table_name="exp_hash_cohort",
        )
        with pytest.raises(ValueError):
            # Request time outside of available intervals
            table_generator.generate_cohort_table([datetime(2015, 12, 31)])
