##Краткосрочные экономические показатели Российской Федерации  

Исходная публикация на сайте Росстата: [www.gks.ru][gks-stei] 

Ряды данных: 
- в формате Excel: [kep.xlsx][kep-at-git] TODO: [_] генерировать xls файл и вставить ссылку на него 
- в формате csv: 
  - [годовые](https://raw.githubusercontent.com/epogrebnyak/rosstat-kep-data/master/src2/output/data_annual.txt) 
  - [квартальные](https://raw.githubusercontent.com/epogrebnyak/rosstat-kep-data/master/src2/output/data_qtr.txt)
  - [месячные](https://raw.githubusercontent.com/epogrebnyak/rosstat-kep-data/master/src2/output/data_monthly.txt) 
- [ ] ZZZ: может быть, давать sql dump 

Графики:
- [PDF](https://github.com/epogrebnyak/rosstat-kep-data/blob/master/src2/output/monthly.pdf)
- .png 

TODO
- [ ] дать ссылку на md-аналог PDF файла со всеми картинками

Список переменных:
<...> 
TODO
- [ ] в папку output выложить список переменных (название, единиа, описание/заголовок) отдельным md файлом 
- [ ] дать ссылку на md файл со списком переменных 
- [ ] дать этот список в качестве страницы в xls файле

Основные графики:
TODO
- [ ] на первую страницу выводить ключевые картинки + ссылку на md файл со всеми картинками

[kep-at-git]: https://github.com/epogrebnyak/rosstat-kep-data/blob/master/src2/output/kep.xlsx?raw=true
[gks-stei]: http://www.gks.ru/wps/wcm/connect/rosstat_main/rosstat/ru/statistics/publications/catalog/doc_1140080765391

##API

Типовые вызовы:
```python
#Пример кода с get_time_series(), get_dataframe()
```

## Program flow
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

##Todo:

- [ ] all TODO listed on this page

Экспорт данных 
- [ ] xls файл
- [ ] Улучшение форматирования xls файлов
- [ ] Упрощение формата csv, use native export
 
Парсинг и импорт 
- [ ] прочитать данные из csv c с ипользованием нескольких файлов разметки

Текущие ошибки парсинга 
- [ ] https://github.com/epogrebnyak/rosstat-kep-data/issues/14 

новые 
- [ ] таблицы с нестандартным количеством столбцов
- [ ] разбивка png/md файла на разделы


Итоговое использование
1.  Ряды со снятием сезонности
10. Переменная состояния среды (фильтр Калмана по 3-5 переменным)
11. Индекс промышленного производства через натуральные показатели
12. Индекс инвестиций через инвестицонные товары 
14. Описание недостающих переменных и блоков (экспортные цены на нефть, например)
