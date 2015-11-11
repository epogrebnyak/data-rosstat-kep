# -*- coding: utf-8 -*-

import matplotlib
# Without the following import, setting matplotlib.style crashes with AttributeError.
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

matplotlib.style.use('ggplot')

# The default figsize is the of an A4 sheet in inches
A4_SIZE_PORTRAIT = [8.27, 11.7]
TITLE_FONT_SIZE = 12


def many_plots_per_page(df, nrows, ncols, figsize=A4_SIZE_PORTRAIT, title_font_size=TITLE_FONT_SIZE):
    
    page_vars = df.columns
    
    # The following command uses the built-in Pandas mechanism for placing subplots on a page.
    # It automatically increases spacing between subplots and rotates axis ticks if they
    # take up too much space. However, this mechanism is broken in Pandas < 0.17.
    # See: https://github.com/pydata/pandas/issues/11536
    # It also cannot handle multiple variables per subplot, so if we want that, we'll have to
    # replicate parts of the Pandas implementation or write our own.
    axes = df.plot(subplots=True, layout=(nrows, ncols), legend=None, figsize=figsize)
    
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

            ax.xaxis.tick_bottom()

    return axes

def save_plots_as_pdf(df, filename, nrows, ncols, figsize=A4_SIZE_PORTRAIT, title_font_size=TITLE_FONT_SIZE):
    vars_ = df.columns
    nvars = len(vars_)
    vars_per_page = nrows * ncols
    with PdfPages(filename) as pdf:
        for start_index in range(0, nvars, vars_per_page):
            page_vars = vars_[start_index:start_index+vars_per_page]
            axes = many_plots_per_page(df[page_vars], nrows, ncols, figsize, title_font_size)
            pdf.savefig()

# -----------------------------------------------------------------------------

def one_plot(df, nrows = 3, ncols = 2,  figsize=A4_SIZE_PORTRAIT, title_font_size=TITLE_FONT_SIZE):   
    # set single plot size propotional to paper and number of plot rows/columns per page
    figsize[0] = figsize[0] / ncols
    figsize[1] = figsize[1] / nrows
    ax = df.plot(legend=None, figsize=figsize)

    # additional formatting for plot
    # NOTE: this should be separate function like format_axis()
    ax.set_title(df.name, fontsize=title_font_size)
    ax.set_xlabel('')
    labels = ax.get_xticklabels()
    for l in labels:
        l.set_rotation('vertical')
    return ax
  
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    from query import get_var_list
    from api2 import get_dataframe

    var_names = get_var_list()
    
    df = get_dataframe(var_names, "m", "1999-01")
    # save_plots_as_pdf(df, 'output/monthly.pdf', 3, 2)

    # TODO-2 @DN:
    # - для понимания, нужен комменатрий - почему линии графиков оказываются в 
    #   консоли разноцветные, а в PDF - черно-белые? это особенности PdfPages?
        
    df = get_dataframe(get_var_list(), "m", "1999-01")
    df = df.iloc[:,0:6]
    # TODO-3 @DN:
    # - для понимания, предположим я закрыл окно в котором были отрисованы графики вызовом ниже
    #   у меня есть z, массив объетов subplot - как я могу снова нарисовать z в отдельной figure?

    z = many_plots_per_page(df, 3, 2)

    # DN: Закрытие окна ещё не означает, что все ссылки на соответствующий figure уничтожены.
    # Эта функция отвечает за очистку следов figure:
    # https://github.com/matplotlib/matplotlib/blob/master/lib/matplotlib/_pylab_helpers.py#L50
    # Её же вызывает plt.close(). Она всего лишь убирает ссылки на figure из внутреннего состояния
    # matplotlib, после чего вызывает сборщик мусора. Поскольку ссылки на figure всё ещё остаются
    # (внутри z, через z.figure), figure из памяти не удаляется.

    old_fig_number = z[0, 0].figure.number
    plt.close(old_fig_number)

    # Теперь matplotlib забыл о существовании figure, но объект всё ещё доступен через z.figure.
    # z -- это всего лишь ndarray из Axes:

    import numpy as np

    assert isinstance(z, np.ndarray)
    assert z.shape == (3, 2)

    # Теперь можно создать новый figure и присоединить к нему старые Axes:
    fig = plt.figure("new figure", figsize=A4_SIZE_PORTRAIT)

    for row in z:
        for ax in row:
            assert isinstance(ax, matplotlib.axes.Axes)
            ax.figure = fig
            fig.add_subplot(ax)

    # Появится одно окно с заголовком "new figure"
    plt.show()

    # not todo/issue:
    # с меньшим количеством лет ориентация подписей по оси х некрасивая +  на англ. яз.   

    df = get_dataframe(get_var_list(), "m", "1999-01")
    df1 = df.iloc[:,3]
    one_plot(df1)    