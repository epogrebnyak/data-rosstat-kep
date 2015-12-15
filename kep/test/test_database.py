from kep.test.test_stream import get_test_flat_rows
from kep.query.save import get_reshaped_dfs
from kep.database.db import stream_to_database

def test_database():
    gen = get_test_flat_rows()
    stream_to_database(gen)
    dfa, dfq, dfm = get_reshaped_dfs()
    assert dfa.loc[2014,'I_yoy'] == 97.3 