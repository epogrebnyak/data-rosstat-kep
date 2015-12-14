# -*- coding: utf-8 -*-
# for testing and new features

# Scope of work:
# - read all variable names from spec/cfg files
# - read all variable names in database (all non-empty /  at specific frequency)
# - make and count headers (non-data rows) 

def count_entries(z, list_):
    count = 0
    for x in list_:
       if z == x:
           count += 1
    return count 

print(count_entries("a", ["a","a","b"]))
assert count_entries("a", ["a","a","b"]) == 2
assert count_entries("b", ["a","a","b"]) == 1