"""
Test miscellaneous helper functions
"""

import unittest

from fiend.utils.misc import *

import numpy as np


class TestFunctionSpaceArgumentParsing(unittest.TestCase):

    def test_argparse_functionspace_comma_separated(self):
        """Test parsing functionspace arguments"""

        name, deg = parse_functionspace_argument('Lagrange,1')
        self.assertEqual(name, "Lagrange")
        self.assertEqual(deg, 1)

    def test_argparse_functionspace_colon_separated(self):
        name, deg = parse_functionspace_argument('Lagrange:1')
        self.assertEqual(name, "Lagrange")
        self.assertEqual(deg, 1)

    def test_argparse_functionspace_semicolon_separated(self):
        name, deg = parse_functionspace_argument('Lagrange;1')
        self.assertEqual(name, "Lagrange")
        self.assertEqual(deg, 1)

    def test_argparse_functionspace_dot_separated(self):
        name, deg = parse_functionspace_argument('Lagrange.1')
        self.assertEqual(name, "Lagrange")
        self.assertEqual(deg, 1)

    def test_argparse_functionspace_extra_braces(self):
        name, deg = parse_functionspace_argument('(Lagrange:1)')
        self.assertEqual(name, "Lagrange")
        self.assertEqual(deg, 1)

    def test_argparse_functionspace_missing_arguments(self):
        with self.assertRaises(Exception) as ctx:
            name, deg = parse_functionspace_argument('(Lagrange:)')

        self.assertTrue('functionspace argument' in repr(ctx.exception))
