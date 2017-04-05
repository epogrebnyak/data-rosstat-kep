## Примеры загрузки данных

### Excel

Вы можете скачать файлы в формате Excel и выбрать в столбцах необходимые ряды данных:  [kep.xlsx][kep-at-git-xlsx], [kep.xls][kep-at-git-xls]

[kep-at-git-xlsx]: https://github.com/epogrebnyak/rosstat-kep-data/blob/master/output/kep.xlsx?raw=true
[kep-at-git-xls]: https://github.com/epogrebnyak/rosstat-kep-data/blob/master/output/kep.xls?raw=true  

### Python 

Данные могут импортироваться из CSV файлов с небольшим преобразованием типа дат. Скрипт ниже загружает данные через интернет:

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

### R

Пример импорта данных в R: [interface.r](interface.r)
