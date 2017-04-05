## Краткосрочные экономические показатели Российской Федерации

### Основные показатели
![](output/png/IND_PROD_yoy.png)
![](output/png/TRANS_COM_bln_t_km.png)
![](output/png/I_yoy.png)
![](output/png/CPI_rog.png)
![](output/png/RETAIL_SALES_yoy.png)
![](output/png/RUR_USD_eop.png)
![](output/png/SOC_WAGE_yoy.png)
![](output/png/GOV_FEDERAL_SURPLUS_ACCUM_bln_rub.png)

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


### Как обновить данные

- Cкачать и распаковать последний обзор с [сайта Росстата][gks-stei] в папку [data](https://github.com/epogrebnyak/data-rosstat-kep/tree/master/data)

- Запустить [update_kep.py](https://github.com/epogrebnyak/data-rosstat-kep/blob/move_specs_2/update_kep.py). Будет выполнено:

```python
from kep import KEP, parse_doc_files

# convert most recent doc files to csv
parse_doc_files()
# parse csv
k = KEP().update()
# obtain dataframes
dfa, dfq, dfm = k.get_all()
# dump outputs
k = k.write_xl()
k.write_monthly_pdf()
k.write_monthly_png()
```
