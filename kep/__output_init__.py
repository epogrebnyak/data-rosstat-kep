# init for output directory
# TODO: make same interface as in kep.__init__()
#       see import line for that

def from_csv(f):
    return pd.read_csv(f, index_col=0)

_dfa = from_csv("df_annual.txt")
_dfq = from_csv("df_quarter.txt")
_dfm = from_csv("df_monthly.txt")
_dfq.index = pd.to_datetime(_dfq.index)    
_dfm.index = pd.to_datetime(_dfm.index)

DFA = _dfa
DFQ = _dfq
DFM = _dfm

# ---------------------------------------------------------------------------------
#   
#  Time series and dataframe by label       
#
# ---------------------------------------------------------------------------------
    
def get_ts(self, freq, varname):
    df = get_df(freq, [varname])
    return df[varname]

def get_df(self, freq, labels):        
    df_dict = {'a': dfa, 'q': dfq, 'm': dfm}
    df = df_dict[freq]
    slicing_labels = [lab for lab in labels if lab in df.columns]       
    return df[slicing_labels]
    
def get_varnames(self, freq = None):
    varnames = dict((ltr, df.columns.tolist()) for df, ltr in zip([_dfa,_dfq, _dfm], 'aqm')) 
    if freq:
        return varnames[freq]
    else:
        return varnames 
