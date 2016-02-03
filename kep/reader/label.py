# -*- coding: utf-8 -*-
"""Store individual variable labels like 'GDP_rog' in class Label() and walk through rows in csv file 
   with adjust_labels() procedure."""

import itertools

# access DefaultDatabase().headlabel_desc_dicts - list of label vs header name 
from kep.database.db import DefaultDatabase

SEP = "_"
FILLER = "<...>"

UNITS_ABBR = {
# --- part from unit dicts
    'rog': 'в % к предыдущему периоду',
    'rub': 'рублей',
    'yoy': 'в % к аналог. периоду предыдущего года' ,
    'ytd': 'с начала года',
# --- part from header dicts
    'bln_t_km':    'млрд. т-км',
    'percent':     '%',
    'bln_rub':     'млрд. руб.',
    'bln_rub_fix': 'млрд. руб. (в фикс. ценах)',
    'mln':   'млн. человек',
    'mln_t': 'млн. т',
    'TWh':   'млрд. кВт·ч',
    'eop':   'на конец периода',
    'bln':   'млрд.',
    'units': 'штук',
    'th':    'тыс.'
}


# add new masks here 
# MASK_DOC = """TRADE_GOODS_EXPORT\tЭкспорт товаров
# TRADE_GOODS_IMPORT\tИмпорт товаров"""

MASK_DOC = """CORP_DEBT_OVERDUE_BUDGET_bln_rub	Просроченная кредиторская задолженность предприятий - в бюджеты всех уровней
CORP_DEBT_OVERDUE_SUPPLIERS_bln_rub	Просроченная кредиторская задолженность предприятий - поставщикам
CORP_DEBT_OVERDUE_bln_rub	Просроченная кредиторская задолженность предприятий - всего
CORP_DEBT_bln_rub	Кредиторская задолженность предприятий
CORP_DUE_bln_rub	Дебиторская задолженность предприятий
CPI_ALCOHOL_rog	Индекс потребительских цен на алкогольные напитки
CPI_FOOD_rog	Индекс потребительских цен на продукты питания
CPI_NONFOOD_rog	Индекс потребительских цен на непродовольственные товары
CPI_SERVICES_rog	Индекс потребительских цен на услуги
GOV_CONSOLIDATED_EXPENSE_ACCUM_bln_rub	Консолидированный бюджет - доходы
GOV_CONSOLIDATED_REVENUE_ACCUM_bln_rub	Консолидированный бюджет - расходы
GOV_FEDERAL_EXPENSE_ACCUM_bln_rub	Федеральный бюджет - расходы
GOV_FEDERAL_REVENUE_ACCUM_bln_rub	Федеральный бюджет - доходы
GOV_FEDERAL_SURPLUS_ACCUM_bln_rub	Федеральный бюджет - профицит
GOV_SUBFEDERAL_EXPENSE_ACCUM_bln_rub	Консолидированные бюджеты субъектов РФ - расходы
GOV_SUBFEDERAL_REVENUE_ACCUM_bln_rub	Консолидированные бюджеты субъектов РФ - доходы
GOV_SUBFEDERAL_SURPLUS_ACCUM_bln_rub	Консолидированные бюджеты субъектов РФ - профицит
NONFINANCIALS_PROFIT_CONSTRUCTION_bln_rub	Прибыль - Строительство
NONFINANCIALS_PROFIT_MANUF_bln_rub	Прибыль - Обрабатывающие производства
NONFINANCIALS_PROFIT_MINING_bln_rub	Прибыль - Добыча полезных ископаемых
NONFINANCIALS_PROFIT_POWER_GAS_WATER_bln_rub	Прибыль - Производство и распределение электроэнергии, газа и воды
NONFINANCIALS_PROFIT_TRANS_COMM_bln_rub	Прибыль - Транспорт и связь
PRICE_EGGS_rub_per_1000	Яйца куриные, рублей за тыс.штук
PRICE_INDEX_CONSTRUCTION_rog	Индекс цен производителей на строительную продукцию
TRADE_GOODS_EXPORT_bln_usd	Экспорт товаров
TRADE_GOODS_EXPORT_rog	Экспорт товаров
TRADE_GOODS_EXPORT_yoy	Экспорт товаров
TRADE_GOODS_IMPORT_bln_usd	Импорт товаров
TRADE_GOODS_IMPORT_rog	Импорт товаров
TRADE_GOODS_IMPORT_yoy	Импорт товаров
TRANS_COM_bln_t_km	Коммерческий грузооборот транспорта
TRANS_COM_rog	Коммерческий грузооборот транспорта
TRANS_COM_yoy	Коммерческий грузооборот транспорта
TRANS_RAILLOAD_mln_t	Погрузка грузов на железнодорожном транспорте
TRANS_RAILLOAD_rog	Погрузка грузов на железнодорожном транспорте
TRANS_RAILLOAD_yoy	Погрузка грузов на железнодорожном транспорте"""

class Label():

    headlabel_reverse_desc_dict = DefaultDatabase().headlabel_desc_dicts.copy()
    mask_dict = dict(line.split('\t') for line in MASK_DOC.split('\n'))
    headlabel_reverse_desc_dict.update(mask_dict)
    
    def __init__(self, *arg):
        self._head = None
        self._unit = None
        
        if len(arg) == 1:
            if isinstance(arg[0], str):    
                self.labeltext = arg[0] 
        if len(arg) == 2:
            self._head = arg[0]
            self._unit = arg[1]
            
    @property
    def labeltext(self):        
        return self.combine(self._head, self._unit)

    @labeltext.setter
    def labeltext(self, value):
        self._head = self._get_head(value)
        self._unit = self._get_unit(value)

    @property
    def head(self):        
        return self._head
        
    @head.setter
    def head(self, value):
        self._head = value        
        
    @property     
    def unit(self):        
        return self._unit
        
    @unit.setter
    def unit(self, value):
        self._unit = value         
        
    def __repr__(self):
        return str(self.labeltext) # "Label: " + str(self.full) + " (head: " + str(self._head) + ", unit: " + str(self._unit) + ")"
        
    @property    
    def dict(self):
        return {'label':self.label, 'head':self._head, 'unit':self._unit}
        
    @staticmethod    
    def _get_head(name):
        words = name.split('_')
        return '_'.join(itertools.takewhile(lambda word: word.isupper(), words))

    @staticmethod
    def _get_unit(name):
        words = name.split('_')
        return '_'.join(itertools.dropwhile(lambda word: word.isupper(), words))

    @property    
    def unit_description(self):
        if self.unit in UNITS_ABBR.keys():
            return UNITS_ABBR[self.unit]
        else:
            return FILLER 

    @property    
    def head_description(self):
        try:
           return self.headlabel_reverse_desc_dict[self._head]
        except:
           return FILLER 
            
    @staticmethod
    def combine(head, unit):
        if len(str(head)+str(unit)):
           return str(head) + SEP + str(unit)
        else:
           return ''
        
    def __eq__(self, obj):
        if self._head == obj.head and self._unit == obj.unit:
            return True      
        else:
            return False   

    def is_unknown(self): 
        return self._head == UnknownLabel()._head

class UnknownLabel(Label):
     def __init__(self):
        self._head = "UNKNOWN"
        self._unit = "unknown"
           

def which_label_on_start(text, lab_dict):      
    for pat in lab_dict.keys():
        if text.strip().startswith(pat):
            return lab_dict[pat]
     
def which_label_in_text(text, lab_dict):
    for pat in lab_dict.keys():
        if pat in text:
            return lab_dict[pat]

def adjust_labels(textline, incoming_label, dict_headline, dict_unit):
    
    """Set new primary and secondary label based on *line* contents. *line* is first element of csv row.    
    
    line = 'Производство транспортных средств и оборудования  / Manufacture of  transport equipment'                                                
            ... causes change in primary (header) label
    
    line = 'отчетный месяц в % к предыдущему месяцу  / reporting month as percent of previous mon'
            ... causes change in secondary (unit) label
    
    ASSUMPTIONS:
      - primary label appears only once in csv file (may not be true, need to use segments then)
      - primary label followed by secondary label 
      - secondary label always at start of the line 
      
    """
        
    # *_sr stands for 'search result'
    
    headline_sr = which_label_in_text(textline, dict_headline)             
    unit_sr = which_label_on_start(textline, dict_unit)  
    
    if headline_sr:
       adjusted_label = Label(headline_sr[0],headline_sr[1])
    elif unit_sr:
       adjusted_label = Label(incoming_label.head, incoming_label.unit)
       adjusted_label.unit = unit_sr 
    else:
       adjusted_label = UnknownLabel()
       
    return adjusted_label
    
if __name__ == '__main__':
    pass

    
    
