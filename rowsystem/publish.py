import pandas as pd       
from rowsystem.config import XLSX_FILE, XLS_FILE, ANNUAL_CSV, QUARTER_CSV, MONTHLY_CSV
from rowsystem.config import PDF_FILE, MD_FILE, PNG_FOLDER, VARNAMES_FILE, OUTPUT_DIR  
import rowsystem.plots as plots

class Publisher():
    
    def write_xl(self):
       """Save dataset as xls and xlsx files."""
       
       def _write_to_xl(file, dfa, dfq, dfm, df_var_table = None):
            with pd.ExcelWriter(file) as writer:
                dfa.to_excel(writer, sheet_name='year')
                dfq.to_excel(writer, sheet_name='quarter')
                dfm.to_excel(writer, sheet_name='month')
                #df_var_table.to_excel(writer, sheet_name='variables')            
                   
                   
       for file in [XLSX_FILE, XLS_FILE]:
            _write_to_xl(file, dfa=self.annual_df()
                             , dfq=self.quarter_df()
                             , dfm=self.monthly_df()
                             )            
                   
    
    def write_csv(self):
       """Save dataset as csv files."""
    
       def _to_csv(df, filename):
           # DataFrame.to_csv(path_or_buf=None, sep=', ', na_rep='', float_format=None, columns=None, header=True, index=True, index_label=None, mode='w', encoding=None, quoting=None, quotechar='"', line_terminator='\n', chunksize=None, tupleize_cols=False, date_format=None, doublequote=True, escapechar=None, decimal='.', **kwds)
           df.to_csv(filename)
   
       _to_csv(self.annual_df(),  ANNUAL_CSV)
       _to_csv(self.quarter_df(), QUARTER_CSV)
       _to_csv(self.monthly_df(), MONTHLY_CSV) 
    
    def varnames_md(self):
       print("TODO: write varnames file")
       
    def write_monthly_pdf(self):
       df = self.monthly_df()
       plots.save_plots_as_pdf(df, PDF_FILE)
       
    def write_monthly_png(self):
       df = self.monthly_df().drop(['year', 'month'], 1)
       self._write_png_images(df)
       self._write_png_showcase_markdownfile(df)

    @staticmethod    
    def _write_png_images(df):
       plots.write_png_pictures(df, PNG_FOLDER)
    
    @staticmethod    
    def _write_png_showcase_markdownfile(df):
       plots.generate_md(df, MD_FILE)   
       
    def publish(self):
       print("Writing Excel files...")
       self.write_xl()
       print("Writing CSV files...")
       self.write_csv()
       self.varnames_md()
       print("Writing PDF...")
       self.write_monthly_pdf()
       print("Writing PNG files...")
       self.write_monthly_png()
       print("Done. For output see: " + OUTPUT_DIR)
       
       
       
       