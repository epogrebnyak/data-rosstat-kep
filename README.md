##Краткосрочные экономические показатели Российской Федерации  

Ряды данных в формате Excel: [kep.xls][kep-at-git]

Исходные данные: [www.gks.ru][gks-stei]

[kep-at-git]: https://github.com/epogrebnyak/rosstat-kep-data/blob/master/kep.xls?raw=true
[gks-stei]: http://www.gks.ru/wps/wcm/connect/rosstat_main/rosstat/ru/statistics/publications/catalog/doc_1140080765391

##Short-Term Economic Indicators of the Russian Federation  

Time series Excel file: [kep.xls][kep-at-git]

Compiled from MS Word files published by Rosstat at [www.gks.ru][gks-stei]


## Development notes:

Extract, store and export economic indicator times series from Rosstat 'KEP' publication.

Main file: src/kep.py

Workflow:
```
    (1) Convert from Word to raw CSV
        single word file -> csv1        
        doc_to_csv(file)
        
        folder with doc files -> csv1
        folder_to_csv(folder)
    
    (2) Label CSV using yaml config file with variable names 
        csv1 + yaml -> csv2
        labelize_csv(file)
    
    (3) Store CSV in flat database (sqlite)
        csv2 -> db          
        csv_to_database(file)
    
    (4) Export data to CSV and Excel files
        db -> csv + xls   
        database_to_xl()
        
    Supplementary jobs:
    (5)  csv1 -> headers -> yaml file     Create headers and yaml config file
```
