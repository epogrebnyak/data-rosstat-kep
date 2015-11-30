#
#  2015-05-18 02:50 PM
#  Example from http://matplotlib.org/api/backend_pdf_api.html
#
#  More:
#      http://stackoverflow.com/questions/11328958/matplotlib-pyplot-save-the-plots-into-a-pdf
#      

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Initialize:
with PdfPages('foo.pdf') as pdf:
     # As many times as you like, create a figure fig and save it:
     fig = plt.figure()
     pdf.savefig(fig)
     # When no figure is specified the current figure is saved
     pdf.savefig()