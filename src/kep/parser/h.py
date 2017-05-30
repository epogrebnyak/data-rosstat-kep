import kep.reader.access as reader
import kep.parser.segments as segments

csv_dicts = list(reader.get_csv_dicts())  
spec = reader.get_spec()
segments.heads(csv_dicts)