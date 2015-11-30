##Краткосрочные экономические показатели Российской Федерации  

Ряды данных: 
- в формате Excel: [kep.xlsx][kep-at-git]
- в формате csv: 
  - [годовые](https://raw.githubusercontent.com/epogrebnyak/rosstat-kep-data/master/src2/output/data_annual.txt) 
  - [квартальные](https://raw.githubusercontent.com/epogrebnyak/rosstat-kep-data/master/src2/output/data_qtr.txt)
  - [месячные](https://raw.githubusercontent.com/epogrebnyak/rosstat-kep-data/master/src2/output/data_monthly.txt) 

Графики:
- [PDF](https://github.com/epogrebnyak/rosstat-kep-data/blob/master/src2/output/monthly.pdf)
- .png

Список переменных:

<...>

Типовые вызовы:
```
Пример кода с get_time_series(), get_dataframe()
```

Справочно: исходная публикация на сайте Росстата: [www.gks.ru][gks-stei] 

[kep-at-git]: https://github.com/epogrebnyak/rosstat-kep-data/blob/master/src2/output/kep.xlsx?raw=true
[gks-stei]: http://www.gks.ru/wps/wcm/connect/rosstat_main/rosstat/ru/statistics/publications/catalog/doc_1140080765391


##Todo:
```
**Front-end** 
1. xls(s)
- [ ] выдавать xls 
- [ ] изменение форматирования файлов
2. картинки
- [ ] на первую страницу выводить ключевые картинки + ссылку на md файл со всеми картинками
- [ ] на первую страницу - ссылку на md файл со всеми картинками
3. список переменных
- [ ] в папку output выложить список переменных (название, единиа, описание/заголовок) + дать этот список в качестве страницы в xls файле + отдельным файлом

**Parsing**
5. наполнение 
- [ ] продолжить формирвоание файла спецификации
6. разделы 
- [ ] форматирование/комментирование разделов
- [ ] отдельные файлы для разделов
- [ ] указать, какие строки НЕ считываем
7. текущие ошибки парсинга 
- [ ] https://github.com/epogrebnyak/rosstat-kep-data/issues/14 
8. прочее
- [ ] таблицы с нестандартным количеством столбцов

**Uses**
9. Ряды со снятием сезонности
10. Переменная состояния среды (фильтр Калмана по 3-5 переменным)
11. Индекс промышленного производства через натуральные показатели
12. Индекс инвестиций через инвестицонные товары 
13. Воспроизвести другие известные расчеты 
14. Описание недостающих переменных и блоков (экспортные цены на нефть, например)
```

