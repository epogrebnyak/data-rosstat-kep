from kep.common.inputs import TempfolderFile, CSV, YAML
 
def test_File():
    # NOTE: works unless last line is \n 
    testline = """123\n\n456"""
    f = TempfolderFile("temp.txt").save_text(testline)    
    assert testline == f.read_text()
    f.remove()

def test_YAML():        
    txt = """a: 1\nb: 2\n---\n ddd"""
    f = TempfolderFile("temp.txt").save_text(txt)
    assert YAML(txt).content == YAML(f.filename).content
    assert YAML(txt).content == [{'a': 1, 'b': 2}, 'ddd']
    f.remove()
        
def test_CSV():
    # NOTE: fails when \n inside list         
    test_list = [["123","456"], ["a","b"]] 
    test_string = "123\t456"+"\n"+"a\tb"
    assert test_list == CSV(test_string).rows 
    
if __name__ == "__main__":
    test_File()
    test_YAML()
    test_CSV()
    