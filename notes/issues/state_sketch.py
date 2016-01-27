# ---------------------------------------------------------------------------------
#   
#  Dicts copied from database
#  
#  States: rs -> db -> csv -> dfs
#         |---------| 
#            (1) CurrentMonthRowsystem.save_db()
#
#         |----------------|
#            (2) CurrentMonthDataframe.save_csv() #          
#
#
# ---------------------------------------------------------------------------------         

# admin.CurrentMonth.save_db()
# admin.CurrentMonth.save_csv()
# CurrentMonthRowsystem.save_db()     # saves to sqlite
# CurrentMonthDataframe.save_csv()    # saves to CSV
# KEP().init_from_csv()
# KEP().init_from_db()
