import pandas as pd       

from inputs import File
from config import XLSX_FILE, XLS_FILE, ANNUAL_CSV, QUARTER_CSV, MONTHLY_CSV
from config import PDF_FILE, MD_FILE, PNG_FOLDER, VARNAMES_FILE, OUTPUT_DIR  
import plots as plots
import tabulate as tab

class Publisher():
    
    def write_xl(self):
       """Save dataset as xls and xlsx files."""
       
       def _write_to_xl(file, dfa, dfq, dfm, df_var_table = None):
            with pd.ExcelWriter(file) as writer:
                dfa.to_excel(writer, sheet_name='year')
                dfq.to_excel(writer, sheet_name='quarter')
                dfm.to_excel(writer, sheet_name='month')
                # TODO: make a sheet
                #df_var_table.to_excel(writer, sheet_name='variables')            
                   
                   
       for file in [XLSX_FILE, XLS_FILE]:
            _write_to_xl(file, dfa=self.annual_df()
                             , dfq=self.quarter_df()
                             , dfm=self.monthly_df()
                             )            
                   
    
    def write_csv(self):
       """Save dataset as csv files."""
    
       def _to_csv(df, filename):
           # as in DataFrame.to_csv(path_or_buf=None, sep=', ', na_rep='', float_format=None, columns=None, header=True, index=True, index_label=None, mode='w', encoding=None, quoting=None, quotechar='"', line_terminator='\n', chunksize=None, tupleize_cols=False, date_format=None, doublequote=True, escapechar=None, decimal='.', **kwds)
           df.to_csv(filename)
   
       _to_csv(self.annual_df(),  ANNUAL_CSV)
       _to_csv(self.quarter_df(), QUARTER_CSV)
       _to_csv(self.monthly_df(), MONTHLY_CSV) 
       
    def _get_var_table_in_markdown(self):        
       iter = self.yield_var_name_components() 
       return tab.pure_tabulate(iter)
        
    def _get_var_table_as_dataframe(self):
        _iter = self.yield_var_list_components()
        return pd.DataFrame(iter, columns = tab.TABLE_HEADER)

    def write_varnames_markdown(self):
       """Writes table of variables (label, desciption, unit) to src/output/varnames.md"""    
       tab_table_string = self._get_var_table_in_markdown()
       File(VARNAMES_FILE).save_text(tab_table_string)

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
       self.write_varnames_markdown()
       print("Writing PDF...")
       self.write_monthly_pdf()
       print("Writing PNG files...")
       self.write_monthly_png()
       print("Resulting output is at: " + OUTPUT_DIR)
      
       
        
# ----------------------------------------------------------------------------
FILLER = "<...>"

def get_title(name, ddict=None):
    if ddict is None:
        global default_dicts
        if default_dicts is None:
            default_dicts = get_complete_dicts(CURRENT_MONTH_DATA_FOLDER)
        ddict = default_dicts
    title_abbr = get_var_abbr(name)
    headline_dict = ddict[0]
    for title, two_labels_list in headline_dict.items():
        if title_abbr == two_labels_list[0]:
            return title
    return FILLER

UNITS_ABBR = {
# --- part from default_dicts [0]
    'rog':'в % к предыдущему периоду',
    'rub':'рублей',
    'yoy':'в % к аналог. периоду предыдущего года' ,
# --- part from default_dicts [1],
    'bln_t_km': 'млрд. т-км',
    'percent': '%',
    'bln_rub': 'млрд. руб.',
    'bln_rub_fix': 'млрд. руб. (в фикс. ценах)',
    'mln': 'млн. человек',
    'mln_t': 'млн. т',
    'TWh': 'млрд. кВт·ч',
    'eop': 'на конец периода',
    'bln': 'млрд.',
    'units': 'штук',
    'th': 'тыс.',
}

def get_unit(name):
    unit_abbr = get_unit_abbr(name)
    if unit_abbr in UNITS_ABBR.keys():
        return UNITS_ABBR[unit_abbr]
    else:
        return FILLER       