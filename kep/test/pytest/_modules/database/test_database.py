from kep.importer.parser.stream import stream_flat_data
from kep.query.save import get_reshaped_dfs
from kep.database.db import stream_to_database, wipe_db_tables

# using fixtures: yes (labelled_rows)
# comment: very weak test, possibly to be revised

def test_database(labelled_rows):
    wipe_db_tables()
    gen = list(stream_flat_data(labelled_rows))
    stream_to_database(gen)
    dfa, dfq, dfm = get_reshaped_dfs()
    assert dfa.loc[2014, 'I_yoy'] == 97.3
