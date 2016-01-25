import os
import sys
from unittest import TestLoader, TextTestRunner

if __name__ == "__main__":
    project_path = os.path.abspath(os.path.join(os.path.split(os.path.realpath(__file__))[0], '..', '..', '..'))
    sys.path.append(project_path)
    from kep.test.unittest.test_suites import TestSuites

    suite = TestLoader().loadTestsFromNames(TestSuites.all_tests)
    TextTestRunner(verbosity=2).run(suite)
