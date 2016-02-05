from kep.reader.rs import CurrentMonthRowSystem
from kep.getter.publish import Publisher
from kep.getter.dataframes import KEP
   
if __name__ == "__main__":
    CurrentMonthRowSystem().update()
    Publisher().publish()
    dfa, dfq, dfm = KEP().dfs()
