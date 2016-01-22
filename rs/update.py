from kep import KEP
   
if '__main__' == __name__:   
   kep = KEP()
   kep.__update_from_current_month__()
   kep.publish()