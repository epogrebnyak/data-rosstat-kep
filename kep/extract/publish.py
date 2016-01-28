"""Write Excel files and graphic output."""

import pandas as pd       

from kep.config import XLSX_FILE, XLS_FILE
from kep.config import PDF_FILE, MD_FILE, PNG_FOLDER, VARNAMES_FILE, OUTPUT_DIR 
from kep.common.inputs import File
from kep.extract.dataframes import Varnames
from kep.reader.label import Label
import kep.extract.plots as plots
        
class Publisher(Varnames):    
    
    def write_xl(self):
       """Save dataset as xls and xlsx files."""

       def _write_to_xl(file):
            with pd.ExcelWriter(file) as writer:
                self.dfa.to_excel(writer, sheet_name='year')
                self.dfq.to_excel(writer, sheet_name='quarter')
                self.dfm.to_excel(writer, sheet_name='month')
                self.df_vars().to_excel(writer, sheet_name='variables')   
                   
       for file in [XLSX_FILE, XLS_FILE]:
            _write_to_xl(file)
    
    #def write_csv(self):
    #   """Save dataset as csv files."""
    #   self.save_dfs()

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
       #NOTE: csvs are written by default by Rowsystem()
       #print("Writing CSV files...")
       #self.write_csv()
       print("Writing markdown file with variable names...")
       self.write_varnames_markdown()
       
       # Task: following two commands take quite long time even on fast machine
       #       need add two progress bars: known and unknown length using library in sample below
       #       https://github.com/epogrebnyak/rosstat-kep-data/blob/master/notes/issues/progress_bar_sample.py       
       
       print("Writing PDF...")
       self.write_monthly_pdf()
       # TODO 1: length of process is unknown - need add a rotating progressbar line / | \ - etc        
       
       length = len(self.dfm.columns) 
       print("Writing {} PNG files...".format(str(len(self.dfm.columns))))
       self.write_monthly_png()
       # TODO 2: length of process is unknown - need add a bar-line progress bar [******     ] 
       
       print("Output located at: " + OUTPUT_DIR)
       