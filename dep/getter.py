import pandas as pd
from datetime import datetime
from calendar import monthrange

import config
import reader

FILENAMES = {f:config.get_csv_filename(f) for f in ('m', 'q', 'a')}

def get_end_of_monthdate(y, m):
    dm = datetime(year=y, month=m, day=monthrange(y, m)[1])
    return pd.Timestamp(dm) 
    
def get_end_of_quarterdate(y, q):
    dq =  datetime(year=y, month=q*3, day=monthrange(y, q*3)[1])   
    return pd.Timestamp(dq)     
    
class Dataframes():
    """Converts incoming stream of dictionaries to pandas dataframes."""
    
    def __init__(self, gen):
       self.dicts = list(gen)           
    
    def data_stream(self, freq, keys):
        return iter({k: d[k] for k in keys} for d in self.dicts if d['freq'] == freq)  
   
    def annual_df(self):
        """Returns pandas dataframe with ANNUAL data."""        
           
        def __check_for_dups__(df): 
               """This is a leftover from debugging. Sometimes 
                  reading values went wrong, needed capturing 
                  this info."""
               r = df[df.duplicated(['varname','year']) == True]
               dups = r['varname'].unique()               
               if dups > 0:
                   raise Exception("Duplicate labels: " + " ".join(dups))

        annual_data_stream = self.data_stream('a', ['varname', 'year', 'value'])
        dfa = pd.DataFrame(annual_data_stream)
        __check_for_dups__(dfa)
        dfa = dfa.pivot(columns='varname', values='value', index='year')
        return dfa
        
    def quarter_df(self):
        """Returns pandas dataframe with QUARTERLY data."""
        # get datastream 
        qtr_data_stream = self.data_stream('q', ['varname', 'year', 'qtr', 'value'])
        # make dataframe
        dfq = pd.DataFrame(qtr_data_stream)
        # add time index
        dfq["time_index"] = dfq.apply(lambda x: get_end_of_quarterdate(x['year'], x['qtr']), axis=1)
        # reshape
        dfq = dfq.pivot(columns='varname', values='value', index='time_index')
        # add extra columns
        dfq.insert(0, "year", dfq.index.year)    
        dfq.insert(1, "qtr", dfq.index.quarter)
        return dfq
        
    def monthly_df(self):
        """Returns pandas dataframe with MONTHLY data."""
        # get datastream     
        monthly_data_stream = self.data_stream('m', ['varname', 'year', 'month', 'value'])    
        # make dataframe
        dfm = pd.DataFrame(monthly_data_stream)                        
        # add time index
        dfm["time_index"] = dfm.apply(lambda x: get_end_of_monthdate(x['year'], x['month']), axis=1)
        # reshape
        dfm = dfm.pivot(columns='varname', values='value', index='time_index')
        # add extra columns
        dfm.insert(0, "year", dfm.index.year)
        dfm.insert(1, "month", dfm.index.month)
        return dfm 
        
    def save(self):        
        self.annual_df().to_csv(FILENAMES['a'])
        self.quarter_df().to_csv(FILENAMES['q'])
        self.monthly_df().to_csv(FILENAMES['m'])

    def dfs(self):
        """Shorthand for obtaining three resulting dataframes."""
        self.dfa = self.annual_df()
        self.dfq = self.quarter_df()
        self.dfm = self.monthly_df()
        return self.dfa, self.dfq, self.dfm  
    
    
class KEP():
    """Read stored CSVs as dataframes."""

    def __init__(self):
        try:
           self.read_dfs()        
        except FileNotFoundError:
           print ("Unable to read files.")
    
    def read_dfs(self):

        def from_csv(filename):
            return pd.read_csv(filename, index_col=0)
        
        # read dataframe CSV dumps
        self.dfa = from_csv(FILENAMES['a'])
        self.dfq = from_csv(FILENAMES['q'])
        self.dfm = from_csv(FILENAMES['m'])
        self.dfq.index = pd.to_datetime(self.dfq.index)    
        self.dfm.index = pd.to_datetime(self.dfm.index)    
    
    def update(self):        
        Dataframes(gen=reader.Rows().dicts()).save()
        return self        
    
    def get_df(self, freq):        
        return {'a': self.dfa, 'q': self.dfq, 'm': self.dfm}[freq]
        
    def get_varnames(self, freq):
        return self.get_df(freq).columns.tolist()
    
    def dfs(self):
    	"""Shorthand for obtaining three resulting dataframes."""
    	return self.dfa, self.dfq, self.dfm  
    
if __name__ == "__main__": 
    dfa, dfq, dfm = Dataframes(gen=reader.Rows().dicts()).dfs()
    for df in (dfa, dfq, dfm):
       assert isinstance(dfa, pd.DataFrame)
       assert len(df)>0
                 
    a, q, m = KEP().update().dfs()
    assert dfa.equals(a)
    # will not compare due to Nan comparisons
    #assert dfq.equals(q)
    #assert dfm.equals(m)