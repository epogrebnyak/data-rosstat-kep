## Краткосрочные экономические показатели Российской Федерации (временные ряды) 

### Основные показатели
![](output/png/IND_PROD_yoy.png)
![](output/png/TRANS_COM_bln_t_km.png)
![](output/png/I_yoy.png)
![](output/png/CPI_rog.png)
![](output/png/RETAIL_SALES_yoy.png)
![](output/png/RUR_USD_eop.png)
![](output/png/SOC_UNEMPLOYMENT_percent.png)
![](output/png/SOC_WAGE_yoy.png)
![](output/png/GOV_FEDERAL_SURPLUS_ACCUM_bln_rub.png)

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

Исходная публикация на сайте Росстата: [www.gks.ru][gks-stei]

[kep-at-git-xlsx]: https://github.com/epogrebnyak/rosstat-kep-data/blob/master/output/kep.xlsx?raw=true
[kep-at-git-xls]: https://github.com/epogrebnyak/rosstat-kep-data/blob/master/output/kep.xls?raw=true
[gks-stei]: http://www.gks.ru/wps/wcm/connect/rosstat_main/rosstat/ru/statistics/publications/catalog/doc_1140080765391


## Как обновить данные

- Cкачать последний обзор с [сайта Росстата][gks-stei] в папку [data](https://github.com/epogrebnyak/data-rosstat-kep/tree/master/data)
- Похимичиить c [word.py](https://github.com/epogrebnyak/data-rosstat-kep/blob/master/kep/reader/word.py)
- Внести изменения в [config.py](https://github.com/epogrebnyak/data-rosstat-kep/blob/move_specs_2/kep/config.py#L4)
```
# USER INPUT: change this when new data arrives
CURRENT_MONTH = 2017, 2
```
- Запустить [update_kep.py](https://github.com/epogrebnyak/data-rosstat-kep/blob/move_specs_2/update_kep.py)
```
from kep import KEP

k = KEP().update()
dfa, dfq, dfm = k.get_all()
k = k.write_xl()
k.write_monthly_pdf()
k.write_monthly_png()
```
