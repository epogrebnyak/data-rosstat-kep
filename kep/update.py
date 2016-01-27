from publish import Publisher
from rs import CurrentMonthRowSystem
   
if __name__ == "__main__":
    CurrentMonthRowSystem().update()
    Publisher().publish()
