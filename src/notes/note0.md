8:36 14.05.2017
  1. Не считываются некоторые переменные из определения
  2. Дублируются три переменные с разными значениями
# DONE  3. Не все определения используются:
# DONE     # import_several_specs.py
# DONE     - считывать все вместе определения
# DONE     - очередь определений + бить файл на сегменты
# DONE     - три причины разных определений (удобство, повторы, разный reader)
  4. Недостаточно контрольных значений
  5. Диагностика 
     - в виде print(), a не тестов
     - много текстовых фикстур
     - нужны простые контрольные сумму
  6. Система каталогов может быть интегрирована с word2csv
  7. Писать версию csv в каталог


Done:
sphinx-apidoc -F -M -f -o docs src/kep

# NEXT:
# import_several_specs.py
# Compare pdef unique varname heads to Datapoints varname heads
#     - Datapoints varname heads
#     - pdef unique varname heads
#     - print both
#     - diff on list
#     - find in file
#     - decide why not imported +  fix specs? 
#     - think of test


REQUIREMENTS
(1) release all values from d.emit('a') and test them against  *testpoints_valid* 
    *FIXME - fialing unittest
        kep\parser\test_containers.py F
         kep\parser\test_datapoints.py FFF
(2) control there are no varnames with same value and year/month/quarter 
    *DONE through emitter.HasValues
(3) make sure all labels from ParsingDefinition(specfile_path) are read, at least at some frequency 
    *DONE in Datapoints.not_imported()
(4) every variable from specs has a *testpoints_valid*     

REMEDIES
# - merge some specs to increase coverage - see what is total numer of headers
# - run headers check against each other - see if checks can work on different header
# - restore mechanism to apply parsing definitions to segments of file
# - add more elements to testpoints_valid 
