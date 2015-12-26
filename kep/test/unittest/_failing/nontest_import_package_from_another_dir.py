import os
import subprocess
import sys
from unittest import TestCase

import kep


# ЕР: (1) пакет kep - не устанавливается через setuptools, от него нельзя требовать, чтобы он импортировался откуда угодно
#     такого требования не было при его проектировании 
# ЕР: (2) test_import - неудачное, слишком общее название
# ЕР: (3) сам этот тест на моей машине не только сбоит, но и вылетает питон на нем.
#       - нужна другая документация?

#
#@epogrebnyak 1) It's OK to lack proper packaging/pip support, but being dependent on current working directory is definitely a bug. That's why I added this test.
#2) Well, the name is generic, but what we are testing here is also generic. How about test_import_package for a file and test_import_package_from_another_dir for a function?
#3a) It seems that your Python installation is broken. Do you have a Windows VirtualBox machine? I don't have one, unfortunately, so I can't try it myself.
#3b) No, the ability to run this test is generally not connected to the ability to generate documentation.
#4) Instead of renaming the tests, it's better to use pytest skip feature. We can disable this test on Windows for now. How about that?
#


class ImportPackageFromAnotherDir(TestCase):

    def test_import_package_from_another_dir(self):
        """
        Test that package is importable regardless of working directory.

        This is especially important for docs generation.
        Everything should be importable without side-effects.
        """
        # Change to docs directory
        project_dir = os.path.normpath(os.path.join(os.path.dirname(kep.__file__), '..'))
        docs_dir = os.path.join(project_dir, 'docs')
        self.assertTrue(os.path.isdir(docs_dir))
        env = {'PYTHONPATH': project_dir}
        code = 'import kep'
        # Try to import kep from another directory in a separate python process
        returncode = subprocess.call([sys.executable, '-c', code],
                                     cwd=docs_dir, env=env)
        self.assertEqual(returncode, 0, '`{}` failed! ' \
                                'To find out why, try it manually ' \
                                'from another directory.'.format(code))
