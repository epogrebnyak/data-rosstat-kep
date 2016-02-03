from kep.common.tabulate import pure_tabulate, add_tail, chunks, TABLE_HEADER

def test_pt():
    textlist = ['35462356', 'wrt', 'wergwetrgwegwetg', 'qrgfwertgwqert', 'abc']
    result = """| Код      | Описание | Ед.изм.          | Частота        |
|:---------|:---------|:-----------------|:---------------|
| 35462356 | wrt      | wergwetrgwegwetg | qrgfwertgwqert |
|:---------|:---------|:-----------------|:---------------|
| abc      |          |                  |                |
|:---------|:---------|:-----------------|:---------------|"""  
    result2 = '| Код      | Описание | Ед.изм.          | Частота        |\n|:---------|:---------|:-----------------|:---------------|\n| 35462356 | wrt      | wergwetrgwegwetg | qrgfwertgwqert |\n|:---------|:---------|:-----------------|:---------------|\n| abc      |          |                  |                |\n|:---------|:---------|:-----------------|:---------------|' 
    z = pure_tabulate(chunks(add_tail(textlist, n = 4), n = 4), header=TABLE_HEADER)
    assert z == result2
    assert result == result2
