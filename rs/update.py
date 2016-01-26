from admin import Admin
from publish import Publisher
   
if __name__ == "__main__":
    Admin().update() 
    #Publisher().write_varnames_markdown()    
    Publisher().publish()