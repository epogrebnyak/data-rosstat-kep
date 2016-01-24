from kep import AdminKEP

kep = AdminKEP()

def get_ts(*arg):
    return kep.get_ts(*arg)

def get_df(*arg):
    return kep.get_df(*arg)

def get_varnames():
    return kep.varnames()
    
def dfa():
    return kep.annual_df()

def dfq():
    return kep.quarter_df()
    
def dfm():
    return kep.monthly_df()
    
    