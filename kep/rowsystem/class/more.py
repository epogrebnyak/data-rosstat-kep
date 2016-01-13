# plots.py: KEP().save_pdf(), KEP().save_png()
# save.py: KEP().save_xl(), KEP.save_csv()
# varnames user tables
# temp_query_labels.py + query labels will allow test of import 
# update current dicectory
# replicate test_mwe
# get feedback on stable version (naming, algorightms, program structure, whatever catches eye)


# may do:
# test_label.py (?)

# wont fix:
# rs.rows and rs.rowsystem[i].['string'] are duplicates

def is_labelled(rs):
    labs = [row['label'].head for row in get_raw_data_rows(rs) if row['label'].head is not None]
    return len(labs) > 0

