def test_database():
    from stream import get_test_flat_db_rows
    gen = get_test_flat_db_rows()
    #_create_table()
    # wipe_db_tables()
    stream_to_database(gen)
    dfa, dfq, dfm = read_dfs(db_file = DB_FILE)
    assert get_period_value(dfa, 'I_yoy', 2014) == 97.3    