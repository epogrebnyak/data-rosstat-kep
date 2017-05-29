doc="""1.2.1. ������� ������������ �� ����� ������������1) (��� ���������� ���������� � ������� �������) / Industrial Production indices by Industry (without seasonal and time factor adjustment)												
������ �������� ���������� / Mining and quarrying												
�������� ����� � % � ����������� ������ / reporting month as percent of previous month												
2015	94,6	91,4	110,9	96,2	102,7	98,0	103,4	100,9	99,1	103,9	95,9	104,2
2.2. �������������� ���������� ���������1) �� ����� ������������� ������������, ���.������ / Balanced financial result by economic activity, mln rubles												
������ �������� ���������� / Mining and quarrying												
2017		258752										
�������������� ������������ / Manufacturing												
2017		109158
��������� ����������� / Loss-making organizations												
������ �������� ���������� / Mining and quarrying												
���������� �����������, ����� / number of organizations, thou												
2017		391										
3. ���� / Prices																	
3.1. ������� ��� �������������� ������������ �������1),2) (�� ����� �������, � % � ����� ����������� �������) / Industrial producer price indices1),2 (end of period, percent of end of previous period)																	
2016	107,4	100,3	105,5	99,9	101,6	98,5	98,8	103,1	101,9	100,9	102,6	100,6	98,7	100,6	100,1	100,5	100,9
2017						103,3	100,8										
� ��� �����: / of which:																	
������ �������� ���������� / Mining and quarrying																	
2016	107,9	96,4	117,3	95,8	99,6	96,5	89,2	111,9	111,4	100,7	104,6	99,1	93,6	103,3	100,0	103,0	96,7
3.1.1. ������� ���� �������������� �� ������������� � �������� ���������������� / Average producer prices of fuel and energy resources and refined products (�� ����� �������) / (end of period)													
����� �����1) / Crude petroleum1)													
������ �� ����� / rubles per ton													
2016	12607	10344	8215	10466	12909	12980	14033	13949	12258	12926	13222	13633	12607"""

def doc_to_dicts(doc):
    rows = [row.split('\t') for row in doc.split('\n')]
    for row in rows:
        if row and row[0]:
            yield dict(head=row[0], data=row[1:])
            
stream = list(doc_to_dicts(doc))

# spec is some json/dict-like datastructure that controls parsing
spec = None

# todo: suggest parsing algorigthm accounting   
#       for multiple/incomplete name entries
#       important - must be able to generalise to larger file

# 'name' key can be different, this dictionary is used to point to values needed
parsing_result = [dict(name="������� ������������ - ������ �������� ����������", 
     year="2015", 
     value="94,6")
,dict(name="�������������� ���������� ��������� - ������ �������� ����������", 
     year="2017", 
     value="258752")
,dict(name="�������������� ���������� ��������� - �������������� �������������", 
     year="2017", 
     value="109158")
,dict(name="������� ��� ��������������", 
     year="2016", 
     value="107,4")
,dict(name="������� ��� �������������� - ������ �������� ����������", 
     year="2016", 
     value="107,9")
,dict(name="����� �����",
     year="2016",
     value="12607")] 
