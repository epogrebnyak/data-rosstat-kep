from kep.reader.rs import CurrentMonthRowSystem
from kep.extract.dataframes import KEP
   
if __name__ == "__main__":
    m = CurrentMonthRowSystem()
    dfa, dfq, dfm = KEP().dfs()
