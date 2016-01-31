import sys
import codecs

from kep.reader.rs import CurrentMonthRowSystem
c = CurrentMonthRowSystem()

assert c.all_2014_count() > 200
assert c.all_2014_count() == sum(n for line, header, n, unknowns, labs in c.section_content())
c.toc()
   