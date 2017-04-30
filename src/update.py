from kep import KEP, parse_doc_files

# convert most recent doc files to csv
parse_doc_files()
# parse csv
k = KEP().update()
# obtain dataframes
dfa, dfq, dfm = k.get_all()
# dump outputs
k = k.write_xl()
k.write_monthly_pdf()
k.write_monthly_png()
