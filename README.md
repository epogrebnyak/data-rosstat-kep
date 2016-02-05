##Краткосрочные экономические показатели Российской Федерации  

Исходная публикация на сайте Росстата: [www.gks.ru][gks-stei]

Оглавление и список переменных:
- [оглавление](https://raw.githubusercontent.com/epogrebnyak/rosstat-kep-data/master/data/2015/ind12/toc.txt) 
- [список переменных](https://raw.githubusercontent.com/epogrebnyak/rosstat-kep-data/master/output/varnames.md)

Ряды данных:
- в формате Excel: [kep.xlsx][kep-at-git-xlsx], [kep.xls][kep-at-git-xls]
- в формате csv:
  - [годовые](https://raw.githubusercontent.com/epogrebnyak/rosstat-kep-data/master/output/data_annual.txt)
  - [квартальные](https://raw.githubusercontent.com/epogrebnyak/rosstat-kep-data/master/output/data_qtr.txt)
  - [месячные](https://raw.githubusercontent.com/epogrebnyak/rosstat-kep-data/master/output/data_monthly.txt)

Графики:
- [PDF](https://github.com/epogrebnyak/rosstat-kep-data/blob/master/output/monthly.pdf)
- [*.png](https://github.com/epogrebnyak/rosstat-kep-data/blob/master/output/images.md)

[kep-at-git-xlsx]: https://github.com/epogrebnyak/rosstat-kep-data/blob/master/output/kep.xlsx?raw=true
[kep-at-git-xls]: https://github.com/epogrebnyak/rosstat-kep-data/blob/master/output/kep.xls?raw=true
[gks-stei]: http://www.gks.ru/wps/wcm/connect/rosstat_main/rosstat/ru/statistics/publications/catalog/doc_1140080765391

## Примеры импорта данных 

Получение рядов данных в виде датафреймов pandas или R показано в файлах [interface.py](interface.py) и 
[interface.r](interface.r). 

Наиболее лаконичный способ иморта данных - из пакета ```kep``` в данном репозитарии:

```python
from kep.getter.dataframes import KEP
dfa, dfq, dfm = KEP().dfs()
```

Импорт также может осуществляться из сохраненных в данном репозитарии текстовых файлов:

```python
import pandas as pd

def add_index(dfq, dfm):
    # set time index
    dfq.index = pd.to_datetime(dfq.time_index)    
    dfm.index = pd.to_datetime(dfm.time_index)
    return dfq, dfm
   
URL_DIR = "https://raw.githubusercontent.com/epogrebnyak/rosstat-kep-data/master/output/"
dfa = pd.read_csv(URL_DIR  + "data_annual.txt", index_col = 0)
dfq = pd.read_csv(URL_DIR  + "data_quarter.txt")
dfm = pd.read_csv(URL_DIR  + "data_monthly.txt")
# set time index
dfq, dfm = add_index(dfq, dfm)
```

## Основные показатели

![](output/png/IND_PROD_yoy.png)
![](output/png/TRANS_COM_bln_t_km.png)
![](output/png/I_yoy.png)
![](output/png/CPI_rog.png)
![](output/png/RETAIL_SALES_yoy.png)
![](output/png/RUR_USD_eop.png)
![](output/png/SOC_UNEMPLOYMENT_percent.png)
![](output/png/SOC_WAGE_yoy.png)
![](output/png/GOV_FEDERAL_SURPLUS_ACCUM_bln_rub.png)

