def table_has_data(table_name, db_engine):
    return any(db_engine.execute(
        "select 1 from {} limit 1".format(table_name)
    ))
