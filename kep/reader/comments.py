# -*- coding: utf-8 -*-
ABBR_DICT = {'DUPL':'переменные содержат дублирующую информацию'
          , 'SCOPE':'переменные вне рамок рассмотрения проекта или избыточная детализация'
		    , 'FMT':'импорт невозможен из-за формата данных'
		   , 'TODO':'необходимо добавить переменные'}
# DUPL
# Не даем показатель "внешнеторговый оборот"
# Индекс потребительских цен дублируется в разделе 3
# Реальные доходы - избыточные
 
PARSING_DOC = """DUPL  @ 1.10. Внешнеторговый оборот – всего1), млрд.долларов США / Foreign trade turnover – total1), bln US dollars
DUPL  @ 1.15. Индекс потребительских цен в % к предыдущему месяцу
DUPL  @ 2.4.1. Кредиторская задолженность, млрд.рублей / Creditor indebtedness, bln rubles
DUPL  @ 2.4.2. Дебиторская задолженность, млрд.рублей / Debtor indebtedness, bln rubles
DUPL  @ 4.2.2. Реальная начисленная заработная плата работников организаций / Accrued average monthly wages per employee
DUPL  @ 4.3.1. Средний размер назначенных пенсий (до 2001г. – с учетом компенсации) / Average awarded pension (till 2001 with compensation)
DUPL  @ 4.3.2. Реальный размер назначенных пенсий1) / Real awarded pensions1)
FMT   @ 1.7.1. Инвестиции в основной капитал организаций (без субъектов малого предпринимательства) по источникам финансирования, млрд.рублей / Fixed capital investments of organizations (without small entrepreneurship) by sources of financing, bln rubles
FMT   @ 2.3. Кредиты, депозиты и прочие размещенные средства, предоставленные организациям, физическим лицам и кредитным организациям (в рублях и иностранной валюте) 1), включая кредиты, предоставленные иностранным государствам и юридическим лицам-нерезидентам (на начало периода), млрд.рублей (по данным Банка России) / Credits, deposits and other allocated funds, granted to enterprises, individuals and credit institutions (in rubles and foreign currency) 1), including credits, granted to foreign governments and non-resident legal entities (beginning of period), bln rubles (data of Bank of Russia)
FMT   @ 4.4. Денежные доходы (в среднем на душу населения) / Money income (average per capita)
FMT   @ 4.4.1. Реальные денежные доходы / Real money income
FMT   @ 4.4.3. Структура использования денежных доходов населения, в процентах / Use of money income, percent
FMT   @ 4.7. Величина прожиточного минимума в среднем на душу населения, в месяц / Average monthly subsistence minimum per capita
FMT   @ 4.8. Численность населения с денежными доходами ниже величины прожиточного минимума / Population with money income below the subsistence minimum
SCOPE @ 1.10.1. Внешнеторговый оборот со странами дальнего зарубежья – всего, млрд.долларов США / Foreign trade turnover with far abroad countries – total, bln US dollars
SCOPE @ 1.10.2.Внешнеторговый оборот с государствами-участниками СНГ – всего, млрд.долларов США / Foreign trade turnover with CIS countries – total, bln US dollars
SCOPE @ 2.1.1. Доходы (по данным Федерального казначейства)2) / Revenues (data of the Federal Treasury)2)
SCOPE @ 2.1.2. Расходы (по данным Федерального казначейства)1) / Expenditures (data of the Federal Treasury)1)
SCOPE @ 2.2. Сальдированный финансовый результат по видам экономической деятельности, млн.рублей / Balanced financial result by economic activity, mln rubles
SCOPE @ 4.1.4. Потребность в трудоустройстве населения,2) на конец месяца / Placement need of population,2) at end of month
TODO  @ 1.2.1. Индексы производства по видам деятельности (без исключения сезонности и фактора времени) / Industrial Production indices by Industry (without seasonal and time factor adjustment)
TODO  @ 1.4. Производство продуктов животноводства в хозяйствах всех категорий / Livestock production at all establishment types
TODO  @ 3.1. Индексы цен производителей промышленных товаров1) (на конец периода, в % к концу предыдущего периода) / Industrial producer price indices1) (end of period, percent of end of previous period)
TODO  @ 3.1.1. Средние цены производителей на энергоресурсы и продукты нефтепереработки / Average producer prices of fuel and energy resources and refined products (на конец периода) / (end of period)
TODO  @ 3.2.1. Средние цены производителей на продукцию животноводства / Average producer prices of livestock products
TODO  @ 5.2.1. Производство пищевых продуктов, включая напитки, и табака / Manufacture of food products, including beverages, and tobacco
TODO  @ 5.2.10. Производство машин и оборудования / Manufacture of mach: nery and equ: pment
TODO  @ 5.2.11. Производство электрооборудования, электронного и оптического оборудования / Manufacture of electrical, electronic and optical equipment
TODO  @ 5.2.2. Текстильное и швейное производство / Manufacture of textiles and textile products
TODO  @ 5.2.4. Обработка древесины и производство изделий из дерева / Manufacture of wood and wood products
TODO  @ 5.2.6. Производство кокса и нефтепродуктов / Manufacture of coke and refined petroleum products
TODO  @ 5.2.7. Химическое производство / Manufacture of chemicals and chemical products
TODO  @ 5.2.8. Производство прочих неметаллических минеральных продуктов / Manufacture of other non-metallic mineral products
TODO  @ 5.2.9. Металлургическое производство и производство готовых металлических изделий / Manufacture of basic metals and fabricated metal products"""

PARSING_COMMENTS = [(ABBR_DICT[e[0].strip()], e[1].split('/')[0]) for e in [line.split(' @ ') for line in PARSING_DOC.split('\n')]]
