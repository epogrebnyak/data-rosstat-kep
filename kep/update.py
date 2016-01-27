from kep.extract.publish import Publisher
from kep.reader.rs import CurrentMonthRowSystem
   
if __name__ == "__main__":
    CurrentMonthRowSystem().update()
    Publisher().publish()
