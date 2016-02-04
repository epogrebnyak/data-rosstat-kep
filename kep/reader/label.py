# -*- coding: utf-8 -*-
'''Store individual variable labels like 'GDP_rog' in class Label() and walk through rows in csv file 
   with adjust_labels() procedure.'''

import itertools

# access DefaultDatabase().headlabel_desc_dicts - list of label vs header name 
from kep.database.db import DefaultDatabase

SEP = '_'
FILLER = '<...>'

UNITS_ABBR = {
# --- part from unit dicts
    'rog': 'в % к предыдущему периоду',
    'rub': 'рублей',
    'yoy': 'в % к аналог. периоду предыдущего года' ,
    'ytd': 'с начала года',
# --- part from header dicts
    'TWh':         'млрд. кВт·ч',
    'bln':         'млрд.',
    'bln_m3' :     'млрд. куб. м',
    'bln_rub':     'млрд. руб.',
    'bln_rub_fix': 'млрд. руб. (в фикс. ценах)',
    'bln_t_km':    'млрд. т-км',
    'bln_usd' :    'млрд. долл. США',
    'days_of_trade' : 'дней торговли',
    'eop':         'на конец периода',
    'gdp_percent': '% ВВП',
    'mln':         'млн.',
    'mln_m2':      'млн. м кв.', 
    'mln_pair' :   'млн. пар',
    'mln_rub' :    'млн. руб.',
    'mln_solid_m3' : 'млн м куб.',    
    'mln_t':       'млн. т',
    'percent':     '%',
    'th':          'тыс.',
    'th_t' :       'тыс. т',
    'units':       'штук'    
}


# add new masks here 
# MASK_DOC = '''TRADE_GOODS_EXPORT\tЭкспорт товаров
# TRADE_GOODS_IMPORT\tИмпорт товаров'''

MASK_DOC = '''CORP_DEBT_OVERDUE_BUDGET	Просроченная кредиторская задолженность предприятий - в бюджеты всех уровней
CORP_DEBT_OVERDUE_SUPPLIERS	Просроченная кредиторская задолженность предприятий - поставщикам
CORP_DEBT_OVERDUE	Просроченная кредиторская задолженность предприятий - всего
CORP_DEBT	Кредиторская задолженность предприятий
CORP_DUE	Дебиторская задолженность предприятий
CORP_RECEIVABLE_OVERDUE_BUYERS\tПросроченная дебиторская задолженность – задолженность покупателей
CORP_RECEIVABLE_OVERDUE\tПросроченная дебиторская задолженность
CORP_RECEIVABLE\tДебиторская задолженность
HH_FINANCE_DEPOSITS_SBERBANK\tОбъем депозитов населения в учреждениях Сбербанка России
RETAIL_SALES_FOOD_INCBEV_AND_TABACCO\tОборот розничной торговли - пищевые продукты, включая напитки, и табачные изделия
RETAIL_SALES_NONFOOD_GOODS\tОборот розничной торговли - непродовольственные товары
SOC_UNEMPLOYED_REGISTERED\tЧисленность официально зарегистрированных безработных
SOC_UNEMPLOYED_REGISTERED_BENEFITS\tИз официально зарегистрированных безработных - получают пособие по безработице
CPI_ALCOHOL	Индекс потребительских цен на алкогольные напитки
CPI_FOOD	Индекс потребительских цен на продукты питания
CPI_NONFOOD	Индекс потребительских цен на непродовольственные товары
CPI_SERVICES	Индекс потребительских цен на услуги
GOV_CONSOLIDATED_EXPENSE_ACCUM	Консолидированный бюджет - доходы (накопл.)
GOV_CONSOLIDATED_REVENUE_ACCUM	Консолидированный бюджет - расходы (накопл.)
GOV_FEDERAL_EXPENSE_ACCUM	Федеральный бюджет - расходы (накопл.)
GOV_FEDERAL_REVENUE_ACCUM	Федеральный бюджет - доходы (накопл.)
GOV_FEDERAL_SURPLUS_ACCUM	Федеральный бюджет - профицит (накопл.)
GOV_SUBFEDERAL_EXPENSE_ACCUM	Консолидированные бюджеты субъектов РФ - расходы (накопл.)
GOV_SUBFEDERAL_REVENUE_ACCUM	Консолидированные бюджеты субъектов РФ - доходы (накопл.)
GOV_SUBFEDERAL_SURPLUS_ACCUM	Консолидированные бюджеты субъектов РФ - профицит (накопл.)
NONFINANCIALS_PROFIT_CONSTRUCTION	Прибыль - Строительство
NONFINANCIALS_PROFIT_MANUF	Прибыль - Обрабатывающие производства
NONFINANCIALS_PROFIT_MINING	Прибыль - Добыча полезных ископаемых
NONFINANCIALS_PROFIT_POWER_GAS_WATER	Прибыль - Производство и распределение электроэнергии, газа и воды
NONFINANCIALS_PROFIT_TRANS_COMM	Прибыль - Транспорт и связь
PRICE_EGGS_rub_per_1000	Яйца куриные, рублей за тыс.штук
PRICE_INDEX_CONSTRUCTION	Индекс цен производителей на строительную продукцию
TRADE_GOODS_EXPORT	Экспорт товаров
TRADE_GOODS_IMPORT	Импорт товаров
TRANS_COM	Коммерческий грузооборот транспорта
TRANS_RAILLOAD	Погрузка грузов на железнодорожном транспорте'''

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
        return str(self.labeltext) # 'Label: ' + str(self.full) + ' (head: ' + str(self._head) + ', unit: ' + str(self._unit) + ')'
        
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
        self._head = 'UNKNOWN'
        self._unit = 'unknown'
           

def which_label_on_start(text, lab_dict):      
    for pat in lab_dict.keys():
        if text.strip().startswith(pat):
            return lab_dict[pat]
     
def which_label_in_text(text, lab_dict):
    for pat in lab_dict.keys():
        if pat in text:
            return lab_dict[pat]

def adjust_labels(textline, incoming_label, dict_headline, dict_unit):
    
    '''Set new primary and secondary label based on *line* contents. *line* is first element of csv row.    
    
    line = 'Производство транспортных средств и оборудования  / Manufacture of  transport equipment'                                                
            ... causes change in primary (header) label
    
    line = 'отчетный месяц в % к предыдущему месяцу  / reporting month as percent of previous mon'
            ... causes change in secondary (unit) label
    
    ASSUMPTIONS:
      - primary label appears only once in csv file (may not be true, need to use segments then)
      - primary label followed by secondary label 
      - secondary label always at start of the line 
      
    '''
        
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
    a = Label().headlabel_reverse_desc_dict['TRADE_GOODS_EXPORT'] 
    b = Label.mask_dict 

    
    
