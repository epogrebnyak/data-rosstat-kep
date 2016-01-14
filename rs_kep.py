from kep import get_dfa as dfa_kep
from rowsystem import get_dfa as dfa_rs

df1 = dfa_rs()
df2 = dfa_kep()
try:
    assert df1 == df2
except:
    print(df2.columns.sym_diff(df1.columns))

# NOTE: program execution seems very slow
# NOTE: several print calls: