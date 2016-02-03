# -*- coding: utf-8 -*-
from kep.reader.label import which_label_on_start, which_label_in_text, adjust_labels, UnknownLabel, Label
    
text = "This is line 1 here"
lab_dict1 = {"This is": 1}
lab_dict2 = {"line": [2, 100]}

def test_inclusion_funcs():
    assert which_label_on_start(text, lab_dict1) == 1
    assert which_label_on_start(text, lab_dict2) is None
    assert which_label_in_text(text, lab_dict1) == 1
    assert which_label_in_text(text, lab_dict2) == [2, 100]

test_curlabel = Label('SOMETHING_here')
testline1 = "This is line 1 here"
testline2 = "what unit is this?"
testline3 = "..."
dict_headline = {"line 1": ['I', 'rub']}
dict_support  = {"what": 'usd'}

def test_adjust_labels():
    assert "I_rub"         == adjust_labels(testline1, test_curlabel, dict_headline, dict_support).labeltext
    assert "SOMETHING_usd" == adjust_labels(testline2, test_curlabel, dict_headline, dict_support).labeltext       
    assert UnknownLabel()  == adjust_labels(testline3, test_curlabel, dict_headline, dict_support)    
    
def test_head_desc():
    assert Label('GDP').head_description == 'Объем ВВП'
    assert Label().headlabel_reverse_desc_dict['TRADE_GOODS_EXPORT'] == 'Экспорт товаров'
    assert Label.headlabel_reverse_desc_dict['TRADE_GOODS_EXPORT'] == 'Экспорт товаров'
    # was:
    # assert Label('TRADE_GOODS_EXPORT_bln_usd').head_description == '/ of which: export of goods \u2013 total'
    # now:    
    assert Label('TRADE_GOODS_EXPORT').head_description == 'Экспорт товаров'

 
   
if __name__ == "__main__":
   #test_inclusion_funcs()
   #test_adjust_labels()
   #test_head_desc()

   z = adjust_labels('1.1.1. Объем ВВП, млрд.рублей /GDP, bln rubles'
              , "***"
              , {'Газ естественный, млрд.куб.м': ['PROD_NATURAL_AND_ASSOC_GAS', 'bln_m3'], 'Бензин автомобильный, млн.тонн': ['PROD_GASOLINE', 'mln_t'], 'Кредиторская задолженность': ['CORP_DEBT', 'bln_rub'], 'Сводный индекс цен на продукцию (затраты, услуги) инвестиционного назначения': ['PRICE_INDEX_INVESTMENT', 'rog'], 'Объем работ по виду деятельности ""Строительство""': ['CONSTR', 'bln_rub_fix', 1.8], 'Численность занятого в экономике населения': ['SOC_EMPLOYED', 'mln'], 'Индекс потребительских цен': ['CPI', 'rog'], 'Обувь, млн.пар': ['PROD_FOOTWEAR', 'mln_pair'], 'Freight loading on railway transport': ['TRANS_RAILLOAD', 'mln_t', '1.6.2'], 'Вагоны грузовые магистральные, штук': ['PROD_RAILWAY_CARGO_WAGONS', 'units'], 'Официальный курс доллара США': ['RUR_USD', 'eop', '1.11.1'], 'Автомобили легковые, тыс.штук': ['PROD_AUTO_PSGR', 'th'], 'Древесина деловая': ['PROD_WOOD_INDUSTRIAL', 'mln_solid_m3', 1.5], 'Вагоны пассажирские магистральные, штук': ['PROD_RAILWAY_PSGR_WAGONS', 'units'], 'индекс цен производителей на строительную продукцию': ['PRICE_INDEX_CONSTRUCTION', 'rog'], 'Стоимость и изменение стоимости фиксированного набора потребительских товаров и услуг': ['CPI_RETAIL_BASKET', 'rub', '1.15.2'], 'Просроченная задолженность по заработной плате на начало месяца': ['SOC_WAGE_ARREARS', 'mln_rub'], 'Древесина необработанная': ['PROD_WOOD_ROUGH', 'mln_solid_m3', 1.5], 'Оборот розничной торговли': ['RETAIL_SALES', 'bln_rub', 1.13], 'Ввод в действие жилых домов организациями': ['DWELL', 'mln_m2', 1.9], 'Стоимость и изменение стоимости условного (минимального) набора продуктов питания': ['CPI_FOOD_BASKET', 'rub', '1.15.1'], 'Инвестиции в основной капитал': ['I', 'bln_rub', 1.7], 'Уровень безработицы': ['SOC_UNEMPLOYMENT', 'percent'], 'Автобусы, штук': ['PROD_AUTO_BUS', 'units'], 'Грузооборот транспорта, включая коммерческий и некоммерческий грузооборот': ['TRANS', 'bln_t_km', 1.6], 'Средний размер назначенных пенсий': ['SOC_PENSION', 'rub'], 'Дебиторская задолженность': ['CORP_DUE', 'bln_rub'], 'Сталь, тыс.тонн': ['PROD_STEEL', 'th_ton'], 'Дефицит ( – ), профицит консолидированного бюджета': ['GOV_CONSOLIDATED_DEFICIT', 'bln_rub', 1.12], 'Товарные запасы в организациях розничной торговли, на конец периода': ['RETAIL_STOCKS', 'bln_rub', '1.13.2'], 'Уголь, млн.тонн': ['PROD_COAL', 'mln_t'], 'Электроэнергия, млрд. кВт·ч': ['PROD_E', 'TWh'], 'Нефть добытая, млн.тонн': ['PROD_OIL', 'mln_t'], 'Автомобили грузовые (включая шасси) (кроме автосамосвалов)': ['PROD_AUTO_TRUCKS_AND_CHASSIS', 'th'], 'Среднемесячная номинальная начисленная заработная плата': ['SOC_WAGE', 'rub'], 'Обеспеченность оборота розничной торговли запасами, дней торговли': ['RETAIL_STOCKS', 'days_of_trade', '1.13.2'], 'Объем платных услуг населению': ['RETAIL_USLUGI', 'bln_rub', 1.14], 'Яйца куриные, рублей за тыс.штук': ['PRICE_EGGS', 'rub_per_1000'], 'Яйца, млн.штук': ['PROD_EGGS', 'mln', 1.4], 
  'Объем ВВП': ['GDP', 'bln_rub', 1.1], 
  'Грузовые автомобили, тыс.штук': ['PROD_AUTO_TRUCKS', 'th'], 'Индекс промышленного производства': ['IND_PROD', 'None', 1.2], 'Велосипеды (без детских), тыс.штук': ['PROD_BYCYCLES', 'th'], 'Коммерческий грузооборот транспорта': ['TRANS_COM', 'bln_t_km', '1.6.1'], 'продукты питания': ['CPI_FOOD', 'rog'], 'Общая численность безработных': ['SOC_UNEMPLOYED', 'bln'], 'алкогольные напитки': ['CPI_ALCOHOL', 'rog'], 'Официальный курс евро по отношению к рублю': ['RUR_EUR', 'eop', '1.11.2']}
              , {'в % к соответствующему периоду предыдущего года': 'yoy', 'отчетный месяц в % к соответствующему месяцу предыдущего года': 'yoy', 'отчетный месяц в % к предыдущему месяцу': 'rog', 'млн.рублей': 'mln_rub', 'в % к предыдущему месяцу': 'rog', 'в % к предыдущему периоду': 'rog', 'в % к соответствующему месяцу предыдущего года': 'yoy', 'в % к ВВП': 'gdp_percent', 'период с начала отчетного года': 'ytd', 'рублей / rubles': 'rub'},
              ).labeltext
