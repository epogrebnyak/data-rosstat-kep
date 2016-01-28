from kep.reader.rs import CurrentMonthRowSystem
from kep.extract.publish import Publisher
from kep.extract.dataframes import KEP
   
if __name__ == "__main__":
    CurrentMonthRowSystem().update()
    Publisher().publish()
    dfa, dfq, dfm = KEP().dfs()
