class DictStream():
    
    def __init__(self, csv_dicts):
        self.csv_dicts = csv_dicts
    
    @staticmethod      
    def is_matched(pat, textline):
        if pat:
            return textline.startswith(pat)
        else:
            return False 
            
    def pop_segment(self, start, end):
        """Pops elements of self.csv_dicts between [start, end). 
           Recognises only first occurences."""
        remaining_dicts = self.csv_dicts.copy()
        we_are_in_segment = False
        segment = []
        for row in self.csv_dicts:
            line = row['head']
            if is_matched(start, line):
                we_are_in_segment = True
            if is_matched(end, line):
                break
            if we_are_in_segment:
                segment.append(row)
                remaining_dicts.remove(row) 
        self.csv_dicts = remaining_dicts
        return segment


assert DictStream.is_matched("a", "abc") is True
assert DictStream.is_matched("ab", "abc") is True
assert DictStream.is_matched("z", "abc") is False
assert DictStream.is_matched("b", "abc") is False
assert DictStream.is_matched(None, "abc") is False

# testing            
csv_dicts = [{'head':s} for s in list("ab-123-c-456-def-000")]

def as_str(csv_dicts):
    return "".join([d['head'] for d in csv_dicts])

# test1
seg = DictStream(csv_dicts).pop_segment('b', 'c') 
assert as_str(seg) == "b-123-"

# test2
ds = DictStream(csv_dicts)
ds.pop_segment('b', 'c')
seg = ds.pop_segment('f', None) 
assert as_str(seg) == "f-000"

# test 3
ds = DictStream(csv_dicts)
assert DictStream(csv_dicts).pop_segment(None, None) == []
assert csv_dicts == ds.csv_dicts