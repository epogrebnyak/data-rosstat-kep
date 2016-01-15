from rowsystem.maincall import datafolder_objects, testfolder_objects

rs, kep = datafolder_objects()
print (rs.not_imported()) 

rs2, kep2 = testfolder_objects()
print (rs2.not_imported())