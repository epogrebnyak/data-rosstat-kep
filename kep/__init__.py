from kep.extract.dataframes import KEP

kep = KEP()

def get_ts(*arg):
    return kep.get_ts(*arg)

def get_df(*arg):
    return kep.get_df(*arg)

def get_varnames():
    return kep.varnames()
    
def get_dfa():
    return kep.dfa()

def get_dfq():
    return kep.dfa()
    
def get_dfm():
    return kep.dfm()
