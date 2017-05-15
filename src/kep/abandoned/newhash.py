# TODO:
# - pick revised datapoints
# - plot revision
# - describe revision types


# TODO:
# add __str__ to HashedValues
# use HashPoint to pass x[0][1] == x[1][1]

from kep.parser.emitter import key_hash

from collections import namedtuple
hashed_point = namedtuple("HashedPoint", "key value")

class HashedValues():
    def __init__(self, datapoints):
        self.hash_value_tuples = [hashed_point(key_hash(d), d['value']) for d in datapoints]
        # [HashPoint(key='a^I__bln_rub^2013', value=13450.3), 
        #  HashPoint(key='a^I__bln_rub^2013', value=4378.4)]
        
        self.dups = self.duplicates()

    def items(self, key):
        #dict-like acces to hashed values by key
        return [x for x in self.hash_value_tuples if x.key == key]

    def duplicates(self):
        hashes = [x.key for x in self.hash_value_tuples]
        seen_set = set()
        duplicate_set = set(x for x in hashes if x in seen_set or seen_set.add(x))
        return [self.items(k) for k in duplicate_set]

    def safe_duplicates(self):
        return [dp for dp in self.dups if dp[0].value == dp[1].value]

    def error_duplicates(self):
        return [dp for dp in self.dups if x[0].value != x[1].value]

if __name__ == "__main__":
    
    # inputs
    import kep.reader.access as reader
    pdef = reader.get_pdef()
    csv_dicts = reader.get_csv_dicts()   
    
    # dataset
    from kep.parser.emitter import Datapoints
    d = Datapoints(csv_dicts, pdef)    
    h = HashedValues(d.emit('a'))    