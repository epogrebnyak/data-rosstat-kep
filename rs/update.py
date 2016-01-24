from kep import AdminKEP
   
if '__main__' == __name__:   
   kep = AdminKEP()
   kep.__update_from_current_month__()
   kep.publish()