import re

_COMMENT_CATCHER = re.compile("\D*([\d.,]*)\s*(?=\d\))")
def kill_comment(text):
    return _COMMENT_CATCHER.match(text).groups()[0]


def as_float(text):
    try:
        return float(text)
    except ValueError:
        raise ValueError("Cannot parse to float: " + str(text))
    
def filter_value(text):
    """Converts *text* to float number assuming it may contain 'comment)'  
       or other unexpected contents."""
    if text == "" or text == "…":
        return None
    if " " in text:
        return filter_value(text.split(" ")[0]) 
    if ')' in text:
        text = kill_comment(text)
    return as_float(text.replace(",", "."))
        
assert kill_comment('6762,31)2)') == '6762,3'     
assert kill_comment('6762.31)2)') == '6762.3'   
assert filter_value('6762,31) 6512,3 ') == 6762.3  