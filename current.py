from kep.reader.rs import CurrentMonthRowSystem
from kep.getter.dataframes import KEP
from kep import get_varnames   
   
if __name__ == "__main__":
    m = CurrentMonthRowSystem()
    dfa, dfq, dfm = KEP().dfs()
    varnames = get_varnames()
