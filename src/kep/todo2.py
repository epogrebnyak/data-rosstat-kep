import kep.reader.access as reader
pdef = reader.get_pdef()
csv_dicts = list(reader.get_csv_dicts())   

import kep.parser.emitter as emitter  

# dataset
d = emitter.Datapoints(csv_dicts, pdef)
output = list(d.emit('a'))

print("\nParsing result on variable level")
print  ("================================")    

print("PROBLEM 2\n"
      "2.1. COVERAGE - Variables included in parsing definitions, but not imported"
      "\n   Possible reason: outdated parsing definition"
      "\n   Severity: HIGH")
msg = ", ".join(d.not_imported())      
print("   Variables:", msg) 
print()


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
      "\n   Possible reason: wrong header handling in algorithm or specfile"
      "\n   Severity: LOW")
      
msg = ", ".join(h.error_duplicates_varnames())
print("   Variables:", msg)
print()
for i, x in enumerate(h.error_duplicates()):
    if i < 5:
        echo(x)
print("    First 5 shown, total:", i)
    