from kep import KEP

k = KEP().update()
dfa, dfq, dfm = k.get_all()
k = k.write_xl()
k.write_monthly_pdf()
k.write_monthly_png()
