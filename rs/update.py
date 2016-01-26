from admin import Admin
from publish import Publisher
from rs import CurrentMonthRowSystem
   
if __name__ == "__main__":
    Admin().update() 
    
    m = CurrentMonthRowSystem()
    m.save()
    m.toc(to_file = True)
    
    #Publisher().write_varnames_markdown()    
    
    
    #Publisher().publish()