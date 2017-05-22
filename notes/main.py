from kep.reader import get_spec, get_csv_dicts
from kep.parser import get_blocks, get_datapoints, emit_a, emit_q, emit_m, make_df
from kep.ini import get_data_folder

from pathlib import Path

class Dataset():
    def __init__(self, csv_dicts, spec):
        blocks = get_blocks(csv_dicts, spec)
        self.datapoints = get_datapoints(blocks)
     
    def get_dfa(self):
        return make_df(emit_a(self.datapoints))
     
    def get_dfq(self):
        return make_df(emit_q(self.datapoints))
     
    def get_dfm(self):
        return make_df(emit_m(self.datapoints))
        
class MonthlyDataset(Dataset):
    def __init__(self, year, month):
        spec = get_spec()
        csv_dicts = get_csv_dicts(year, month)
        super().__init__(csv_dicts, spec)

    def save_all(self):
        # TODO: save df     
        return None

# inputs
print("Loading parsing definitions...")
spec = get_spec()
year, month = 2017, 2
print("Loading raw csv file for {1}.{0}...".format(year, month))
csv_dicts = list(get_csv_dicts(year, month))

# parsing
print("Splitting raw csv file by table...")
blocks = list(get_blocks(csv_dicts, spec)) 

print("Reading datapoints from tables...")
datapoints = list(get_datapoints(blocks))

# slicing datapoints at (a)nnual, (q)uarterly and (m)onthly frequencies
pts_a = emit_a(datapoints)
pts_q = emit_q(datapoints)
pts_m = emit_m(datapoints)

print("Creating dataframes...")
dfa = make_df(pts_a)
dfq = make_df(pts_q)
dfm = make_df(pts_m)

print("Saving dataframes...")
# TODO: save to csv using ini.py output file location

print("Finished script")

# TODO: show inspection result for blocks
# TODO: show inspection result for datapoints
# TODO: show inspection result for dataframes
