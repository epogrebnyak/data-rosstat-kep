# ** DONE problem 1 - must introduce additional parsing defintions 
#                     to Block class, get_blocks and Datapoints 

import kep.ini as ini
from kep.reader.parsing_definitions import ParsingDefinition
import kep.reader.access as reader
import kep.parser.containers as containers  
import kep.parser.emitter as emitter  


# main_def and more_def contain all parsing defintions 
main_def = ParsingDefinition(path=ini.get_mainspec_filepath())
more_def = [ParsingDefinition(path) for path in ini.get_additional_filepaths()]

# *spec* replaces all definitions
spec = reader.get_spec()
assert spec.main == main_def
assert spec.main == main_def

# read data
csv_dicts = list(reader.get_csv_dicts())   

# make blocks by table
blocks = containers.get_blocks(csv_dicts, spec)
for b in blocks:
    #containers.uprint(b)
    #print()
    pass

    
containers.show_stats(blocks, spec)

# ERROR: .show_stats() does not account for *more_def* 
#        labs = set([main_def.unique_labels] + [d.unique_labels for d in more_def]) 

# IDEA: move show_stats() to test

# FIXME: detect duplicates early at blocks level
#varnames = [(b.label, i) for i,b in enumerate(blocks) if b.label is not None]

# IDEA: parse defintion on itself to see to validate it
#      (must fail on "Кирпичи" and "Кирпичи и черепица" in header dict)


# ** problem 2.1 - incomplete coverage + incomplete testpoints + undocumented residual (what is not read from file)

# ** problem 2.3 - duplicate datapoints


# dataset
d = emitter.Datapoints(csv_dicts, spec)
output = list(d.emit('a'))

print("\nParsing result on variable level")
print  ("================================")    

print("PROBLEM 2\n"
      "2.1. COVERAGE - Variables included in parsing definitions, but not imported"
      "\n   Possible reason: outdated parsing definition"
      "\n   Severity: HIGH")
# FIXME CRITICAL - d.not_imported() not working
#msg = ", ".join(d.not_imported())      
#print("   Variables:", msg) 
#print()


print("\nWait while finding duplicates...")
h = emitter.HashedValues(d.datapoints)

print("\n2.2 Safe duplicates (same values for same date)" 
      "\n   Possible reason: table appears in CSV file twice"
      "\n   Severity: LOW")

msg = ", ".join(h.safe_duplicates_varnames())
print("   Variables:", msg)
print()
      
def echo(x):
    print("    {}:".format(x[0].key), ", ".join([str(z.value) for z in x]))

for i, x in enumerate(h.safe_duplicates()):
    if i < 5:
        echo(x)
print("    First 5 shown, total:", i)         


print("\n2.3. Error duplicates (have different values for same date)"
      "\n   Possible reason: wrong header handling in algorithm or parsing defintiion"
      "\n   Severity: LOW")
      
msg = ", ".join(h.error_duplicates_varnames())
print("   Variables:", msg)
print()
for i, x in enumerate(h.error_duplicates()):
    if i < 5:
        echo(x)
print("    First 5 shown, total:", i)



# task 3 - work with time series vintages

# - generate multiple CSV files using kep.word2csv
#   <https://github.com/epogrebnyak/data-rosstat-kep/blob/dev/src/local_file_management/kep_data.py>


# - tune file acccess to multiple files


# - implement end-user access fucntions
"""
# Get latest dataset with all available variables as pandas DataFrame
dfa = get_dataset_a()
dfq = get_dataset_q()
dfq = get_dataset_m()    

# Get latest vintage of *varname* as pd.TimeSeries
gdp = get_ts(varname = "a_GDP_rog")    

# Get all (04.2009-<03.2017>) vintages of *varname* as pd.DataFrame
v_gdp = get_vintages(varname = "a_GDP_rog")
"""

# plot vintages/revisions for GDP 
# v_gdp.plot()


# task 4 - generate frontend markdown and images for repository


# task 5 - replicate/enhance datalab repo