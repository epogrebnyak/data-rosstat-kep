import pandas as pd
from datetime import datetime
from calendar import monthrange

import kep.config as config 
import kep.reader.reader as reader
import kep.getter.plots as plots

FILENAMES = {f: config.get_csv_filename(f) for f in ('m', 'q', 'a')}


def get_end_of_monthdate(y, m):
    dm = datetime(year=y, month=m, day=monthrange(y, m)[1])
    return pd.Timestamp(dm) 


def get_end_of_quarterdate(y, q):
    dq = datetime(year=y, month=q*3, day=monthrange(y, q*3)[1])
    return pd.Timestamp(dq)     


class Dataframes():
    """Converts incoming stream of dictionaries *gen* to pandas 
       dataframes at annual, quarterly and monthly frequencies."""
    
    def __init__(self, gen):
       self.dicts = list(gen)           
    
    def data_stream(self, freq, keys):
        return iter({k: d[k] for k in keys} for d in self.dicts if d['freq'] == freq)  

    def get_dataframe(self, freq):
        if freq == 'a':
            gen = self.data_stream('a', ['varname', 'year', 'value'])
        elif freq == 'q':
            gen = self.data_stream('q', ['varname', 'year', 'qtr', 'value'])
        elif freq == 'm':
            gen = self.data_stream('m', ['varname', 'year', 'month', 'value'])
        else:
            raise ValueError(freq)
        return pd.DataFrame(gen)

    def annual_df(self):
        """Returns pandas dataframe with ANNUAL data."""        
           
        def __check_for_dups__(df): 
               """This is an ugly leftover from debugging. 
                  Sometimes reading values went wrong, needed capturing 
                  this situation."""
               r = df[df.duplicated(['varname','year']) == True]
               dups = r['varname'].unique()               
               if dups > 0:
                   raise Exception("Duplicate labels: " + " ".join(dups))

        dfa = self.get_dataframe("a")
        __check_for_dups__(dfa)
        return dfa.pivot(columns='varname', values='value', index='year')        

    def quarter_df(self):
        """Returns pandas dataframe with QUARTERLY data."""
        # get dataframe
        dfq = self.get_dataframe("q")
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
        # get dataframe
        dfm = self.get_dataframe("m")
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
        return self.annual_df(), self.quarter_df(), self.monthly_df() 

    
class KEP():
    """Read stored CSVs as dataframes."""

    def __init__(self):
        try:
           self.read_dfs()        
        except FileNotFoundError:
           print ("CSV files not found. Updating...")
           self.update()
           self.read_dfs()           
    
    def read_dfs(self):

        def from_csv(filename):
             df = pd.read_csv(filename, index_col=0)
             df.index = pd.to_datetime(df.index)  
             return df

        # annual index in int numbers
        self.dfa = pd.read_csv(open(FILENAMES['a']), index_col=0)

        # read dataframe from CSV dumps
        self.dfq = from_csv(open(FILENAMES['q']))
        self.dfm = from_csv(open(FILENAMES['m']))
        
    def update(self):        
        Dataframes(gen=reader.Rows().dicts()).save()
        return self        
        
    def get_varnames(self, freq):
        return self.get_df(freq).columns.tolist()
        
    def get_df(self, freq):        
        return {'a': self.dfa, 'q': self.dfq, 'm': self.dfm}[freq]
    
    def get_all(self):
        """Shorthand for obtaining three resulting dataframes."""
        self.read_dfs()
        return self.dfa, self.dfq, self.dfm  
    
    def write_xl(self):
       """Save dataset as xls and xlsx files."""

       def _write_to_xl(file):
            with pd.ExcelWriter(file) as writer:
                self.dfa.to_excel(writer, sheet_name='year')
                self.dfq.to_excel(writer, sheet_name='quarter')
                self.dfm.to_excel(writer, sheet_name='month')
                #self.df_vars().to_excel(writer, sheet_name='variables')   
                   
       for file in [config.XLSX_FILE, config.XLS_FILE]:
            _write_to_xl(file)
       return self

    def write_monthly_pdf(self):
        df = self.dfm.drop(['year', 'month'], 1)
        plots.save_plots_as_pdf(df, config.PDF_FILE)
        return self

    def write_monthly_png(self):
        df = self.dfm.drop(['year', 'month'], 1)
        plots.write_png_pictures(df, config.PNG_FOLDER)
        plots.generate_md(df, config.MD_FILE)
        return self

KEP().read_dfs()