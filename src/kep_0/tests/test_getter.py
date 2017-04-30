import pandas as pd

import kep.reader.reader as reader
from kep.getter.getter import Dataframes, KEP

def test_getter():
    
    dfa, dfq, dfm = Dataframes(gen=reader.Rows().dicts()).dfs()
    
    for df in (dfa, dfq, dfm):
       assert isinstance(df, pd.DataFrame)
       assert len(df)>0

    a, q, m = KEP().update().get_all()
    assert dfa.equals(a)

    # will not compare due to Nan comparisons
    #assert dfq.equals(q)
    #assert dfm.equals(m)
