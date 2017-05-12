import kep.reader.access as reader
pdef = reader.get_pdef()
csv_dicts = reader.get_csv_dicts()    

import kep.parser.emitter as emitter
d = emitter.Datapoints(csv_dicts, pdef)
output = list(x for x in d.emit('a') if x['year']==2016) 

def show_2016():
    print("Annual values for 2016:")
    msg = ",\n".join([x.__repr__() for x in output])
    print(msg) 
    return msg

if __name__ == "__main__":
    echo = show_2016()
    assert 'GDP__bln_rub' in echo
    assert '2016' in echo 
    assert '85881.0' in echo