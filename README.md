##Краткосрочные экономические показатели Российской Федерации  

Временные ряды по краткосрочным экономическим показателям хранятся в папке 
[output](https://github.com/epogrebnyak/rosstat-kep-data/blob/master/output/) в трех csv файлах (годовые, квартальные, месячные данные), а также в файлах xls и xls(x). 

Оглавление и список переменных:
- [оглавление](https://raw.githubusercontent.com/epogrebnyak/rosstat-kep-data/master/data/2015/ind12/toc.txt) 
- [список переменных](https://github.com/epogrebnyak/data-rosstat-kep/blob/master/output/varnames.md)

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

Исходная публикация на сайте Росстата: [www.gks.ru][gks-stei]

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


## Как использовать эти данные 

###Excel

Вы можете скачать файлы в формате Excel и выбрать в столбцах необходимые ряды данных.  

###Python 

Для работы с датафреймами pandas данные могут импортироваться из CSV файлов с небольшим преобразованием типа дат. Скрипт ниже загружает данные через интернет:

```python
import pandas as pd

URL_DIR = "https://raw.githubusercontent.com/epogrebnyak/rosstat-kep-data/master/output/"
dfa = pd.read_csv(URL_DIR  + "data_annual.txt", index_col = 0)
dfm = pd.read_csv(URL_DIR  + "data_monthly.txt", converters = {'time_index':pd.to_datetime}, 
                                                 index_col = 'time_index')
dfq = pd.read_csv(URL_DIR  + "data_quarter.txt", converters = {'time_index':pd.to_datetime}, 
                                                 index_col = 'time_index')
```
 
После этого временные ряды доступны в датафреймах ```dfa```, ```dfq``` и ```dfm```, например:

```
>>> print(dfa.GDP_yoy)
year
1999    106.4
2000    110.0
2001    105.1
2002    104.7
2003    107.3
2004    107.2
2005    106.4
2006    108.2
2007    108.5
2008    105.2
2009     92.2
2010    104.5
2011    104.3
2012    103.5
2013    101.3
2014    100.7
2015     96.3
Name: GDP_yoy, dtype: float64
```

Код импорта данных содержится в файле [interface.py](interface.py)

###R

Пример импорта данных в R: [interface.r](interface.r)

##Как обновить данные

По мере выхода новых данных файлы в папке output будут обновляться. Для этого администатор скачивает и распаковывает архив с файлами MS Word и запускает скрипт [update.py](update.py), после чего изменения вносятся в репозитарий. Подробнее о деталях см. [здесь](https://github.com/epogrebnyak/rosstat-kep-data/issues/104).

График обновления данных в 2016 году: <http://www.gks.ru/gis/images/graf-oper2016.htm>

