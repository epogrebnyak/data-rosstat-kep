import unittest

import kep.parser.containers as containers

# TODO: make pytests
assert containers.is_year('20161)2)') is True

# most cases
assert containers.get_year('2015') == 2015
# some cells with comment
assert containers.get_year('20161)') == 2016
# some cells with two comments
assert containers.get_year('20161)2)') == 2016
# will not match with extra space
assert containers.get_year(' 20161)2)') is None
# not valid year
assert containers.get_year('1. Сводные показатели') is None
assert containers.get_year('27000,1-45000,0') is None


assert containers.is_year('20161)2)')


assert containers.parse_section_name('1. Сводные показатели') ==  '1'
assert containers.parse_section_name('2016') is None
assert containers.parse_section_name('4.8 Численность населения с денежными доходами') == '4.8'
assert containers.parse_section_name('4.8. Численность населения с денежными доходами') == '4.8'

                                    
assert containers.detect("Canada", ["ana", "bot"]) == 'ana'
assert containers.detect("Canada", ["bot", "ana"]) == 'ana'
assert containers.detect("Canada", ["dog", "bot"]) is None
                                    
if __name__ == '__main__':
    unittest.main()
