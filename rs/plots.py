# -*- coding: utf-8 -*-

import os
from datetime import datetime
import numpy as np
import matplotlib
import matplotlib.pyplot as plt # without this, matplotlib.style.use crashes with AttributeError
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import NullFormatter
from pandas.tseries.converter import TimeSeries_DateFormatter


matplotlib.style.use('ggplot')

# The default figsize is the size of an A4 sheet in inches
A4_SIZE_PORTRAIT = [8.27, 11.7]
TITLE_FONT_SIZE = 12


# -----------------------------------------------------
# PDF


def save_plots_as_pdf(df, filename, nrows=3, ncols=2, figsize=A4_SIZE_PORTRAIT,
                      title_font_size=TITLE_FONT_SIZE):
    vars_ = df.columns
    nvars = len(vars_)
    vars_per_page = nrows * ncols
    with PdfPages(filename) as pdf:
        for start_index in range(0, nvars, vars_per_page):
            page_vars = vars_[start_index:start_index + vars_per_page]
            axes = many_plots_per_page(df[page_vars], nrows, ncols, figsize, title_font_size)
            pdf.savefig()
            plt.close()


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
            format_ax(ax)
    return axes


# -----------------------------------------------------
# additional formatting for plot - in PDF and png

class CustomFormatter(TimeSeries_DateFormatter):
    def __init__(self, default_formatstr, *args, **kwargs):
        super(CustomFormatter, self).__init__(*args, **kwargs)
        self.default_formatstr = default_formatstr

    def _set_default_format(self, vmin, vmax):
        formatdict = super(CustomFormatter, self)._set_default_format(vmin, vmax)
        for loc in self.locs:
            formatdict.setdefault(loc, self.default_formatstr)
        return formatdict


def format_ax(ax):
    ax.set_xlabel('')

    # The default formatter for Pandas dataframes with dates as indices is
    # pandas.tseries.converter.TimeSeries_DateFormatter. The problem with it is
    # that it completely ignores modifications to major and minor ticks
    # and calculates all tick locations, types and labels internally by itself.
    # CustomFormatter is basically a patch that looks into the internals of
    # TimeSeries_DateFormatter and modifies whatever it has calculated so that
    # the custom tick locations are taken into account.
    major_formatter = CustomFormatter(
        default_formatstr='%Y',
        freq=ax.xaxis.get_major_formatter().freq,  # another peek into the internals
        minor_locator=False,
        dynamic_mode=True,
        plot_obj=ax
    )

    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.xaxis.set_major_formatter(major_formatter)

    xright = ax.get_xlim()[1]
    # According to matplotlib docs, time is plotted on x-axis after converting timestamps
    # to floats using special functions in matplotlib.dates: date2num and num2date.
    # Internally, they are basically wrappers around datetime.toordinal(), which, in turn,
    # returns the number of days since January 1, year 1 (as an integer).
    # However, here get_xlim() says that the limits are the numbers of months passed since epoch.
    # For example, 348.0 is the left limit and 348/12 = 29. This matches the beginning of year
    # 1999. Hence this recalculation.
    # I haven't investigated whether this is intentional or if Pandas simply doesn't follow
    # matplotlib's guidelines. This shows up in Pandas 0.17.1.
    new_xright = (datetime.now().year + 1 - 1970) * 12
    # new_xright = (2015 + 1 - 1970) * 12
    assert xright <= new_xright  # we'll know if the logic above breaks
    ax.set_xlim(right=new_xright)

    # ensuring that the last tick is major
    major_ticks = ax.get_xticks(minor=False)
    minor_ticks = ax.get_xticks(minor=True)
    if minor_ticks[-1] > major_ticks[-1]:
        last_tick = minor_ticks[-1]
        major_ticks = np.append(major_ticks, last_tick)
        minor_ticks = np.delete(minor_ticks, -1)
        ax.set_xticks(major_ticks, minor=False)
        ax.set_xticks(minor_ticks, minor=True)

    labels = ax.get_xticklabels()
    for l in labels:
        l.set_rotation('vertical')
    ax.xaxis.tick_bottom()


# -----------------------------------------------------
# PNG

def one_plot(df, nrows=3, ncols=2, figsize=A4_SIZE_PORTRAIT, title_font_size=TITLE_FONT_SIZE):
    # set single plot size propotional to paper and number of plot rows/columns per page
    # WARNING: updating figsize in-place means that A4_SIZE_PORTRAIT gets modified.
    # This leads to unexpected problems.
    ax = df.plot(legend=None, figsize=(figsize[0] / ncols, figsize[1] / nrows))
    ax.set_title(df.name, fontsize=title_font_size)

    # additional formatting for plot
    format_ax(ax)
    return ax


def make_png_filename(vn, dirpath):
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    return os.path.join(dirpath, "%s.png" % vn)


def write_png_pictures(df, folder):
    for vn in df.columns:
        # Indexing df as df[[vn]] produces a DataFrame, not a Series. Therefore,
        # it does not have a .name attribute, but it has .columns instead.
        ts = df[vn]

        # one_plot returns Axes and sets matplotlib's current figure to the plot it draws
        try:
            ax = one_plot(ts)
            filepath = make_png_filename(vn, folder)
            plt.subplots_adjust(bottom=0.15)
            plt.savefig(filepath)
            plt.close()
        except Exception as e:
            raise Exception("Error plotting variable: " + str(vn))


def generate_md(df, md_file):
    var_names = df.columns
    # сгенерировать markdown файл, в котором по 3 на строку
    # выведены все картинки var_names + ".png"
    IMAGES_PER_LINE = 3

    # MAYDO: use a specialized package for this?
    with open(md_file, 'w') as f:
        for row_start in range(0, len(var_names), IMAGES_PER_LINE):
            line_vars = var_names[row_start:row_start + IMAGES_PER_LINE]
            f.write(' '.join('![](png/%s.png)' % var_name for var_name in line_vars) + '\n')

def sample_plot():
    # sample plot
    # from end_user import get_ts
    # ts = get_ts('IND_PROD_yoy', "m", "1999-01")
    # one_plot(ts)
    # plt.close()
    pass

# NOTE: с меньшим количеством лет ориентация подписей по оси х некрасивая +  на англ. яз.
