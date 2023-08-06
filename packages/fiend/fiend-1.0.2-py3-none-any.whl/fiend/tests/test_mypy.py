import unittest
import mypy.api


class TestTypes(unittest.TestCase):

    def test(self):
        """Run the static type checker MYPY on the code base"""
        mypy.api.run(['-p', 'fiend', '--ignore-missing-imports'])
