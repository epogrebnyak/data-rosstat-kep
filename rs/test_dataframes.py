from dataframes import KEP
import pandas as pd
   
def test_df_KEP():
    k = KEP()
    
    assert k.dfm.equals(k.get_df('m', k.get_varnames()['m']))
    assert k.dfa.equals(k.get_df('a', k.get_varnames()['a']))
    assert k.dfq.equals(k.get_df('q', k.get_varnames()['q']))
    
    m1_name = k.get_varnames()['m'][0]
    assert isinstance(k.get_ts("m", m1_name), pd.Series)