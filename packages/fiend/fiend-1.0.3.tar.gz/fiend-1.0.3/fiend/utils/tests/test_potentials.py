"""
Tests for predefined potentials
"""

import unittest

# These tests should be run only if dolfin can be imported
try:
    import dolfin as df
    import numpy as np
    from fiend.utils.predefined_potentials import atom_potential_times_rho_expr
    from fiend.utils.mesh import mesh_of_sphere_in_cylindrical_coordinates
    import_dolfin_ok = True
except BaseException:
    import_dolfin_ok = False


@unittest.skipIf(not import_dolfin_ok, "Could not load dolfin")
class TestPotentials(unittest.TestCase):
    def setUp(cls):
        cls.mesh = mesh_of_sphere_in_cylindrical_coordinates(
            radius=50.0,
            core_radius=3.0,
            refinement_radius=40.0,
            cellradius=1.0,
            core_cellradius=0.001)

        cls.V = df.FunctionSpace(cls.mesh, 'Lagrange', 2)

    def test_hydrogen(self):
        """Test Hydrogen potential"""

        ρV = atom_potential_times_rho_expr('H', self.mesh)
        ρVfun = df.project(ρV, self.V)

        # Tolerance is low because we have already projected to a functionspace
        res = np.array([0.0])
        ρVfun.eval(res, [1.0, 0.0])
        self.assertAlmostEqual(res[0], -1.0,
                               places=4)

        ρVfun.eval(res, [0.01, 0.2])
        self.assertAlmostEqual(res[0], -0.04993761694,
                               places=4)

    def test_lithium(self):
        """Test Lithium potential"""
        ρV = atom_potential_times_rho_expr('Li', self.mesh)
        ρVfun = df.project(ρV, self.V)

        res = np.array([0.0])
        ρVfun.eval(res, [1.0, 0.0])
        self.assertAlmostEqual(res[0], -1.197096010397791,
                               places=4)

        ρVfun.eval(res, [0.5, 7.0])
        self.assertAlmostEqual(res[0], -0.07124705026435496,
                               places=4)
