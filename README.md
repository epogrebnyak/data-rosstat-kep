##Краткосрочные экономические показатели Российской Федерации  

Исходная публикация на сайте Росстата: [www.gks.ru][gks-stei] 

Ряды данных: 
- в формате Excel: [kep.xlsx][kep-at-git] * TODO: [_] issue #24: генерировать xls файл и вставить ссылку на него *
- в формате csv: 
  - [годовые](https://raw.githubusercontent.com/epogrebnyak/rosstat-kep-data/master/src/output/data_annual.txt) 
  - [квартальные](https://raw.githubusercontent.com/epogrebnyak/rosstat-kep-data/master/src/output/data_qtr.txt)
  - [месячные](https://raw.githubusercontent.com/epogrebnyak/rosstat-kep-data/master/src/output/data_monthly.txt) 

Список переменных: 
- [varnames.md](https://github.com/epogrebnyak/rosstat-kep-data/blob/master/src/output/varnames.md)

Графики:
- [PDF](https://github.com/epogrebnyak/rosstat-kep-data/blob/master/src/output/monthly.pdf)
- .png *TODO - [_] дать ссылку на md-аналог PDF файла со всеми картинками - это issue #27: make full list of .png files as markdown file +  issue #29*

[kep-at-git]: https://github.com/epogrebnyak/rosstat-kep-data/blob/master/src2/output/kep.xlsx?raw=true
[gks-stei]: http://www.gks.ru/wps/wcm/connect/rosstat_main/rosstat/ru/statistics/publications/catalog/doc_1140080765391


## Основные показатели

*TODO
- [ ] на первую страницу выводить ключевые картинки + ссылку на md файл со всеми картинками - Issues #27/ #29*
- [ ] указатьна какую дату +  генерировать

## API - интерфейс для получения данных

Типовые вызовы:
```python
#Пример кода с get_time_series(), get_dataframe()
```

## Структура программы (program flow)
```
1. Converter
doc - > raw csv
(word.py)
2. Parser
raw csv + specification -> labelled csv -> flat stream -> database
         (load_spec.py)   (label_csv.py)  (stream.py)    (database.py)
3. Selector
database -> dfm, dfq, dfa -> get_ts(), get_df()
                      ... -> get_varnames()   
(query.py)
4. Plotting
(plot.py)
```

##Todo

Самое важное сейчас:
- [ ] issue #30
- [ ] issue #31
 
Экспорт данных
- [ ] issue #24 - экспорт данных: xls файл
- [ ] issue  #1 - экспорт данных: улучшение форматирования xls(x) файлов / apearance of xlsx file
- [ ] issue #26 - Упрощение формата csv, use native pandas export for csv files
 
Парсинг и импорт 
- [ ] issue #30 - прочитать данные из csv c иcпользованием нескольких файлов разметки - read raw csv using config file and two spec files 
- [ ] make varlist, including segments
- [ ] make varlist in order of appearance in markupfile + include segments

Тестирование
- [ ] issue #31 - запустить py.test внутри пакета (вместе c __init__.py) - Testing: run test_1.py executable with py.test 

Текущие ошибки парсинга 
- [ ] https://github.com/epogrebnyak/rosstat-kep-data/issues/14 
- [ ] не читается переменная PROFIT

Рисунки:
- [ ] issue #29: Save all monthly plots as .png files 
- [ ] issue #27: make full list of .png files as markdown file 

Докуменатция:
- [ ] issue #25: улучшить скрипт построения документации
- [ ] issue #32: написать примеры использвоания API - write API examples for README.md

##Not todo

Новые функции
- [ ] таблицы с нестандартным количеством столбцов
- [ ] разбивка png-md или pdf файла на разделы
- [ ] новый шаблон pdf файла
- [ ] sql dump of database

Некритические
- [ ] transfer useful functions from old_src at src branch
- [ ] генерировать tab_headers.txt - использовать make_headers(p) в label_csv из ветки old_src
- [ ] integrity check of database
- [ ] may remove first 'readers functions' part in spec file
- [ ] issue #6: orderly sequence of variables in xlsx file - in columns
- [ ] groups/sections of variables in pdf/md-png
- [ ] rename common to io +  move load_spec to common + make test_load_spec.py
- [ ] check if header (eg "Объем платных услуг населению") has multiple appearances in raw csv file 
- [ ] substitute 'tabulate' module with simple pure python function to write table
- [ ] maybe move 'output' folder to root  


##Итоговое использование
1. Ряды со снятием сезонности
2. Переменная состояния среды (фильтр Калмана по 3-5 переменным)
3. Индекс промышленного производства через натуральные показатели
4. Индекс инвестиций через инвестицонные товары 
5. Описание недостающих переменных и блоков (экспортные цены на нефть, например)
