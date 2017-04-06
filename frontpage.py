"""
ID  | Название  | Ед.изм.  | Последнее значение  |  Sparkline
--- | --------- | -------- | ------------------- | --------------------
CPI | Индекс потребительских цен | изменение к предыдущему месяцу | 1.015 (02.2017) |![](https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/Sparkline_dowjones_new.svg/189px-Sparkline_dowjones_new.svg.png)

- связь CPI - название и размерность переменной
- найти последнее значение
- частоты значений AQM
- последнее значение какой частоты?
- рисовать спарклайн
- проваливаться при нажатии
- генерировать в readme?
- индивидуальные показатели
"""

import os
import matplotlib.pyplot as plt

FILE = "frontpage.md"
from tabulate import pure_tabulate

from kep import KEP
import kep.config as config


def get_last(df, lab):
    s = df[lab]
    ix = ~s.isnull()
    last_value = s[ix][-1]
    last_date = s.index[ix][-1]
    return str(round(last_value,2)), last_date.strftime("%m.%Y")

def make_png_filename(vn, dirpath):
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    return os.path.join(dirpath, "%s_spark.png" % vn)

def spark(data):    
    fig = plt.figure(figsize=(2, 0.5))
    ax = fig.add_subplot(111)
    ax.plot(data)
    for k,v in ax.spines.items():
        v.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    
    #plt.plot(len(data) - 1, data[len(data) - 1], 'r.')
    #ax.fill_between(range(len(data)), data, len(data)*[min(data)], alpha=0.1)
    
    return ax 

def write_sparkline_pngs(df, folder = config.PNG_FOLDER):
    for vn in df.columns:
       ts = df[vn]
       # one_plot returns Axes and sets matplotlib's current figure to the plot 
       # it draws        
       ax = spark(ts)
       filepath = os.path.join(folder, spark_png_fn(vn))
       plt.subplots_adjust(bottom=0.15)
       plt.savefig(filepath)
       plt.close()


def spark_png_fn(varname):
    return "%s_spark.png" % varname

def insert_image_to_md(varname): 
    path = "output\\png\\%s" % spark_png_fn(varname)
    return '![](%s)' % path

def stream_table_rows():
    dfm = KEP().dfm.drop(['year', 'month'], 1)
    for name in dfm.columns:
       value, date = get_last(dfm, name) 
       img = insert_image_to_md(name)
       yield name, value, date, img
   
def get_md_code():
    header = ["Код", "Значение", "Дата", ""]
    rows = list(stream_table_rows())
    return pure_tabulate(rows, header)
    

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
            
write_md()
dfm = KEP().dfm.drop(['year', 'month'], 1)    
lab = 'RUR_EUR_eop'
assert len(get_last(dfm, lab)) == 2
s = dfm[lab]\
       
spark(s) 
write_sparkline_pngs(dfm)

def generate_md(md_file):
    md_code = get_md_code()
    with open(md_file, 'w', encoding = 'utf-8') as f:
        f.writelines(md_code)
        
generate_md("frontpage.md")        
