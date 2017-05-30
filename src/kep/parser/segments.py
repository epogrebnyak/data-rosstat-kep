"""Split *csv_dicts* to segment for each definition in *spec*."""


class DictStream():
    
    def __init__(self, csv_dicts):
        # consume *csv_dicts*, if it is a generator
        self.csv_dicts = [x for x in csv_dicts]
    
    @staticmethod      
    def is_matched(pat, textline):
        pat = pat.replace('"','') 
        textline = textline.replace('"','')
        if pat:
            return textline.startswith(pat)
        else:
            return False 
    
    def is_found(self, pat):
        for csv_dict in self.csv_dicts:
            if self.is_matched(pat, csv_dict['head']):
                return True
        return False
          
    def remaining_dicts(self):
        return self.csv_dicts

    def pop(self, pdef):
        return self.pop_segment_by_definition(pdef)
    
    def pop_segment_by_definition(self, pdef):
        for s,e in pdef.start_and_end_lines():
            self.validate_ends(s,e)
            if self.is_found(s) and self.is_found(e):
                return self.pop_segment(s, e)
        else:
            self.echo_error_ends_not_found(pdef)
            return []    
        
    def echo_error_ends_not_found(self, pdef):
        print("***  ERROR: start or end line not found in *csv_dicts*  ***")              
        for s,e in pdef.start_and_end_lines():
                print("   ", self.is_found(s), "<{}>".format(s))
                print("   ", self.is_found(e), "<{}>".format(e))                
        
    def validate_ends(self, start, end):
        if self.is_matched(start, end) or self.is_matched(end, start):
            print("***  ERROR: start and end lines not unique***")
            print(start)
            print(end)
    
    def pop_segment(self, start, end):
        """Pops elements of self.csv_dicts between [start, end). 
           Recognises occurences by index."""           
        remaining_csv_dicts = self.csv_dicts.copy()
        we_are_in_segment = False
        segment = []
        i = 0
        while i < len(remaining_csv_dicts):
            row = remaining_csv_dicts[i]
            line = row['head']
            if self.is_matched(start, line):
                we_are_in_segment = True
            if self.is_matched(end, line):
                break
            if we_are_in_segment:
                segment.append(row)
                del remaining_csv_dicts[i]
            else:    
                # else is very important, wrong index without it
                i += 1
        self.csv_dicts = remaining_csv_dicts
        return segment   


def heads(csv_dicts):
    print ("\n".join([x['head'] for x in csv_dicts if "".join(x['data']) == ""]))

if __name__ == "__main__":
    import kep.reader.access as reader
    csv_file = reader.__get_csv_path__()
    csv_dicts = list(reader.get_csv_dicts())  
    spec = reader.get_spec()
    heads(csv_dicts)

    print("\ntest 1 --------------------------")
    flag = 0
    for pdef in spec.extras:
         # searching in full csv file         
         seg = DictStream(csv_dicts).pop(pdef)
         if len(seg) == 0: 
            flag = 1            
            print ("\nERROR: returned segment with 0 length")
            print (pdef)
    if flag == 0:
        print("****************************************")
        print("All segment start/ends found in csv file")
        print("****************************************")       

    print("\ntest 2 --------------------------")    
    # removing segments and searching in leftover (desired algorithm) 
    ds = DictStream(csv_dicts)    
    for pdef in spec.extras:
        seg = ds.pop(pdef)
        if len(seg) == 0: 
            print("ERROR: returned segment with 0 length")
            print (pdef)        
            pass
        else:
            print ("SUCCESS: segment length is", len(seg), "rows")            
            print (pdef)  
            pass
        print()
        
    print(spec.main)
    seg = ds.remaining_dicts()
    print(len(seg))
    
   
    print("\ntest 3 --------------------------")    
    s = "2.1.1. Доходы (по данным Федерального казначейства)"
    e = "2.1.2. Расходы (по данным Федерального казначейства)"
                        
    z = DictStream(csv_dicts)
    #assert z.is_found(e)
    z.pop(pdef=spec.extras[0])
    rd = z.remaining_dicts()
    #heads(rd)    

    #assert z.is_found(e)
    k = z.pop_segment(s, e)
    #heads(k)     
    
    for pdef in spec.extras:
        s,e = next(pdef.start_and_end_lines())
        print(s.replace("\"",""))
        
    g = [next(pdef.start_and_end_lines())[0].replace('\"','') for pdef in spec.extras]   
    r = sorted(g)
    ix = [g.index(e) for e in sorted(g)]
    ordered_specs = [spec.extras[i] for i in ix]
        
    
    # TODO / PROBLEM:  find out reason for failure in test 2
    
    # in test 2 we have a failure:
    #***  ERROR: start or end line not found in csv_dicts  ***
    #True <2.1.1. Доходы (по данным Федерального казначейства)>
    #False <2.1.2. Расходы (по данным Федерального казначейства)>
    #*********************************************************
    #ERROR: returned segment with 0 length
    #3 variables between line <2.1.1. Доходы (по данным Федерального казначейства)> and <2.1.2. Расходы (по данным Федерального казначейства)> read with <fiscal>: 
    #GOV_CONSOLIDATED_REVENUE_ACCUM, GOV_FEDERAL_REVENUE_ACCUM, GOV_SUBFEDERAL_REVENUE_ACCUM

      
    # while in test 3 we see that this data is found in full csv_dicts
    # possible-reason - some other segment cuts out this information 
    #                   in test 2