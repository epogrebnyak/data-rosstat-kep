from daframes import KEP

kep = KEP()

def get_ts(*arg):
    return kep.get_ts(*arg)

def get_df(*arg):
    return kep.get_df(*arg)

def get_varnames():
    return kep.varnames()
    
def dfa():
    return kep.dfa()

def dfq():
    return kep.dfa()
    
def dfm():
    return kep.dfm()