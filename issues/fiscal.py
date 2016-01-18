from rowsystem.rowsystem import KEP
#a = KEP()
#a.__update__()
#dfm = a.monthly_df()
#print(dfm['GOV_CONSOLIDATED_REVENUE_bln_rub'])

from rowsystem.classes import CurrentMonthRowSystem as C
c = C()
z = [x for x in c.data.dicts if x['varname'] == 'GOV_CONSOLIDATED_REVENUE_bln_rub' and x['year'] == 2001]
for t in z:
    print(t)
