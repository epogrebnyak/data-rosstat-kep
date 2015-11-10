# -*- coding: utf-8 -*-

import matplotlib
# Without the following import, setting matplotlib.style crashes with AttributeError.
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

matplotlib.style.use('ggplot')

# The default figsize is the of an A4 sheet in inches
A4_SIZE_PORTRAIT = (8.27, 11.7)
TITLE_FONT_SIZE = 12

def many_plots_per_page(df, nrows, ncols, figsize=A4_SIZE_PORTRAIT, title_font_size=TITLE_FONT_SIZE):
    
    page_vars = df.columns
    
    # The following command uses the built-in Pandas mechanism for placing subplots on a page.
    # It automatically increases spacing between subplots and rotates axis ticks if they
    # take up too much space. However, this mechanism is broken in Pandas < 0.17.
    # See: https://github.com/pydata/pandas/issues/11536
    # It also cannot handle multiple variables per subplot, so if we want that, we'll have to
    # replicate parts of the Pandas implementation or write our own.
    axes = df.plot(subplots=True, layout=(nrows, ncols), legend="123", figsize=figsize)
    
    # Now removing axis labels and adding plot titles.
    for i, axes_row in enumerate(axes):
        for j, ax in enumerate(axes_row):
            var_idx = i * ncols + j
            if var_idx >= len(page_vars):
                # We're at the end of the last page, which is not filled completely.
                break
            ax.set_title(page_vars[var_idx], fontsize=title_font_size)
            ax.set_xlabel('')
            
            # The following is an example of how to draw vertical labels.
            # API references:
            # - http://matplotlib.org/api/axes_api.html#matplotlib.axes.Axes.get_xticklabels
            # - http://matplotlib.org/api/text_api.html#matplotlib.text.Text.set_rotation
            labels = ax.get_xticklabels()
            for l in labels:
                l.set_rotation('vertical')
                
            # TODO @DN:
            # убрать тики на верхней горизонтальной оси  
            
            return axes
    
def save_plots_as_pdf2(df, filename, nrows, ncols, figsize=A4_SIZE_PORTRAIT, title_font_size=TITLE_FONT_SIZE):    
    vars_ = df.columns
    nvars = len(vars_)
    vars_per_page = nrows * ncols
    with PdfPages(filename) as pdf:
        for start_index in range(0, nvars, vars_per_page):
            page_vars = vars_[start_index:start_index+vars_per_page]

            # The following command uses the built-in Pandas mechanism for placing subplots on a page.
            # It automatically increases spacing between subplots and rotates axis ticks if they
            # take up too much space. However, this mechanism is broken in Pandas < 0.17.
            # See: https://github.com/pydata/pandas/issues/11536
            # It also cannot handle multiple variables per subplot, so if we want that, we'll have to
            # replicate parts of the Pandas implementation or write our own.
            axes = df[page_vars].plot(subplots=True, layout=(nrows, ncols), legend=None, figsize=figsize)

            # Now removing axis labels and adding plot titles.
            for i, axes_row in enumerate(axes):
                for j, ax in enumerate(axes_row):
                    var_idx = i * ncols + j
                    if var_idx >= len(page_vars):
                        # We're at the end of the last page, which is not filled completely.
                        break
                    ax.set_title(page_vars[var_idx], fontsize=title_font_size)
                    ax.set_xlabel('')
                    
                    # The following is an example of how to draw vertical labels.
                    # API references:
                    # - http://matplotlib.org/api/axes_api.html#matplotlib.axes.Axes.get_xticklabels
                    # - http://matplotlib.org/api/text_api.html#matplotlib.text.Text.set_rotation
                    labels = ax.get_xticklabels()
                    for l in labels:
                        l.set_rotation('vertical')
                        
                    # TODO @DN:
                    # убрать тики на верхней горизонтальной оси 
                    
            pdf.savefig()


def save_plots_as_pdf(df, filename, nrows, ncols, figsize=A4_SIZE_PORTRAIT, title_font_size=TITLE_FONT_SIZE):    
    vars_ = df.columns
    nvars = len(vars_)
    vars_per_page = nrows * ncols
    with PdfPages(filename) as pdf:
        for start_index in range(0, nvars, vars_per_page):
            page_vars = vars_[start_index:start_index+vars_per_page]

            # The following command uses the built-in Pandas mechanism for placing subplots on a page.
            # It automatically increases spacing between subplots and rotates axis ticks if they
            # take up too much space. However, this mechanism is broken in Pandas < 0.17.
            # See: https://github.com/pydata/pandas/issues/11536
            # It also cannot handle multiple variables per subplot, so if we want that, we'll have to
            # replicate parts of the Pandas implementation or write our own.
            axes = df[page_vars].plot(subplots=True, layout=(nrows, ncols), legend=None, figsize=figsize)

            # Now removing axis labels and adding plot titles.
            for i, axes_row in enumerate(axes):
                for j, ax in enumerate(axes_row):
                    var_idx = i * ncols + j
                    if var_idx >= len(page_vars):
                        # We're at the end of the last page, which is not filled completely.
                        break
                    ax.set_title(page_vars[var_idx], fontsize=title_font_size)
                    ax.set_xlabel('')
                    
                    # The following is an example of how to draw vertical labels.
                    # API references:
                    # - http://matplotlib.org/api/axes_api.html#matplotlib.axes.Axes.get_xticklabels
                    # - http://matplotlib.org/api/text_api.html#matplotlib.text.Text.set_rotation
                    labels = ax.get_xticklabels()
                    for l in labels:
                        l.set_rotation('vertical')
                        
                    # TODO @DN:
                    # убрать тики на верхней горизонтальной оси 
                    
            pdf.savefig()
            
def one_plot_as_pdf(filename, row_col, df, figsize=(8.27, 11.7), title_font_size=12):   
    pass

if __name__ == "__main__":
    from query import get_var_list
    from api2 import get_dataframe
    df = get_dataframe(get_var_list(), "m", "1999-01")
    #save_plots_as_pdf(df, 'output/monthly.pdf', 3, 2)
    df = df[0:5]
    z = many_plots_per_page(df, 3, 2)
    