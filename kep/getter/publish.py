"""Write Excel files and graphic output."""

import pandas as pd       

from kep.config import XLSX_FILE, XLS_FILE
from kep.config import PDF_FILE, MD_FILE, PNG_FOLDER, VARNAMES_FILE, OUTPUT_DIR 
from kep.common.inputs import File
from kep.getter.dataframes import Varnames
from kep.reader.label import Label
import kep.getter.plots as plots
# from kep.getter.local_progressbar import progressbar


class Publisher(Varnames):

    def write_xl(self):
        """Save dataset as xls and xlsx files."""

        with pd.ExcelWriter(XLS_FILE) as writer:
            self.dfa.to_excel(writer, sheet_name='year')
            self.dfq.to_excel(writer, sheet_name='quarter')
            self.dfm.to_excel(writer, sheet_name='month')
            self.df_vars().to_excel(writer, sheet_name='variables')

        writer = pd.ExcelWriter(XLSX_FILE, engine='xlsxwriter')
        styles = set_styles(writer.book)
        write_sheet(writer, self.dfa, 'year', styles)
        write_sheet(writer, self.dfq, 'quarter', styles)
        write_sheet(writer, self.dfm, 'month', styles)
        write_sheet(writer, self.df_vars(), 'variables', styles)
        writer.save()

    def write_varnames_markdown(self):
       """Writes table of variables (label, desciption, unit) to src/output/varnames.md"""    
       tab_table_string = self.txt_vars_table()
       File(VARNAMES_FILE).save_text(tab_table_string)

    def write_monthly_pdf(self):
       df = self.dfm.drop(['year', 'month'], 1)
       plots.save_plots_as_pdf(df, PDF_FILE)
       
    def write_monthly_png(self):
       df = self.dfm.drop(['year', 'month'], 1)
       self._write_png_images(df)
       self._write_png_showcase_markdownfile(df)

    @staticmethod    
    def _write_png_images(df):
       plots.write_png_pictures(df, PNG_FOLDER)
    
    @staticmethod    
    def _write_png_showcase_markdownfile(df):
       plots.generate_md(df, MD_FILE)   
       
    def publish(self):
       print("\nWriting Excel files...")
       self.write_xl()

       print("Writing markdown file with variable names...")
       self.write_varnames_markdown()
       
       # Task: following two commands take quite long time even on fast machine
       #       need add two progress bars: known and unknown length using library in sample below
       #       https://github.com/epogrebnyak/rosstat-kep-data/blob/master/notes/issues/progress_bar_sample.py
       #       and https://github.com/epogrebnyak/rosstat-kep-data/blob/master/notes/issues/local_progressbar.py
       
       print("Writing PDF...")
       #pbar = progressbar(sign="#", length=50, infinite=False)
       #pbar.start()
       self.write_monthly_pdf()
       #pbar.stop()
       
       # TODO 1: length of process is NOT KNOWN - need add a rotating progressbar line / | \ - etc
       
       length = len(self.dfm.columns)
       print("Writing {} PNG files...".format(str(len(self.dfm.columns))))
       #pbar = progressbar(sign="#", length=50, infinite=False)
       #pbar.start()
       self.write_monthly_png()
       #pbar.stop()
       # TODO 2: length of process is KNOWN, equals len(self.dfm.columns)- need add a bar-line progress bar [******     ]
       
       print("Output located at: " + OUTPUT_DIR)
       

def set_styles(workbook):
    # setting excel workbook styles, once for a book

    return {
        'header': workbook.add_format({
            'bold': False,
            'font_name': 'Arial',
            'font_color': 'magenta',
            'font_size': 8,
            'align': 'left',
            'valign': 'top',
            'text_wrap': True,
            'border': 1}),
        'index': workbook.add_format({
            'bold': True,
            'font_name': 'Arial',
            'font_color': 'red',
            'font_size': 10,
            'align': 'center',
            'border': 1}),
        'data': workbook.add_format({
            'bold': False,
            'font_name': 'Arial',
            'font_color': 'blue',
            'font_size': 10,
            'align': 'right'})
    }


def write_sheet(writer, df, sheet_name, styles):
    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, index=False, header=False,
                startcol=1,  # first column is reserved for inserting index_data
                startrow=1,  # first row is reserved for inserting column_data
                sheet_name=sheet_name)
    sheet = writer.sheets[sheet_name]

    # Setup sheets cols and row sizes
    sheet.set_column('A:A', 18.0)
    sheet.set_column('B:DA', 12.0, styles['data'])
    sheet.set_row(0, 33.0)

    # Adding df.index as a first column
    sheet.write_column("A2", df.index, styles['index'])
    #import ipdb; ipdb.set_trace()
    sheet.write_row("A1", [df.index.name] + df.columns.tolist(), styles['header'])

