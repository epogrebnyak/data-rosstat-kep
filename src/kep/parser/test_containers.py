import unittest

import kep.containers as containers

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


if __name__ == '__main__':
    unittest.main()
