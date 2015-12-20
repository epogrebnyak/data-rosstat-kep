from kep.importer.parser.stream import stream_flat_data
from kep.query.save import get_reshaped_dfs
from kep.database.db import stream_to_database

def test_database(labelled_rows):
    gen = list(stream_flat_data(labelled_rows))
    stream_to_database(gen)
    dfa, dfq, dfm = get_reshaped_dfs()
    assert dfa.loc[2014, 'I_yoy'] == 97.3
