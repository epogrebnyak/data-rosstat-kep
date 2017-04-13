Где все происходит
==================

[reader.py](https://github.com/epogrebnyak/data-rosstat-kep/blob/kep2/kep2/reader.py)

```python
from config import get_default_spec_path, get_default_csv_path
from csv_data import CSV_Reader
from datapoints import Datapoints
from parsing_definitions import ParsingDefinition

# data
csv_path = get_default_csv_path()
csv_dicts = list(CSV_Reader(csv_path).yield_dicts())

# parsing instruction
specfile_path = get_default_spec_path()
pdef = ParsingDefinition(specfile_path)

# dataset
d = Datapoints(row_dicts = csv_dicts, spec = pdef)

# streams of dicts
annual = list(d.emit('a'))
quarterly = list(d.emit('q'))
monthly = list(d.emit('m'))
 
```

Основной end-to-end тест, показывающий конвертацию исходного CSV файла при помощи параметров парсинга в поток данных (точек) находится также в [reader.py](https://github.com/epogrebnyak/data-rosstat-kep/blob/kep2/kep2/reader.py)


О структуре проекта
===================

<https://github.com/epogrebnyak/data-rosstat-kep/issues/135>


Текущие задачи
==============

<https://github.com/epogrebnyak/data-rosstat-kep/issues/136>
