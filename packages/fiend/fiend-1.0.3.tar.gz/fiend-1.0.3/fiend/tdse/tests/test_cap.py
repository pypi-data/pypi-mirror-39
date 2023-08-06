"""
Tests for absorbing potentials
"""
import unittest

try:
    import dolfin as df
    import numpy as np
    from fiend.utils.predefined_potentials import atom_potential_times_rho_expr
    from fiend.utils.mesh import mesh_of_sphere_in_cylindrical_coordinates
    from fiend.tdse.absorbing_boundaries import get_cap
    import ufl
    import_dolfin_ok = True
except Exception as e:
    import_dolfin_ok = False


@unittest.skipIf(not import_dolfin_ok, "Could not load dolfin")
class TestComplexAbsorbingPotential(unittest.TestCase):
    def setUp(cls):
        cls.mesh = mesh_of_sphere_in_cylindrical_coordinates(
            radius=50.0,
            core_radius=3.0,
            refinement_radius=40.0,
            cellradius=1.0,
            core_cellradius=0.1)

        cls.V = df.FunctionSpace(cls.mesh, 'Lagrange', 1)

    def test_cap(self):
        """Test imaginary absorbing potential"""

        # Get CAP and project it to our simple functionspace
        cap = get_cap(50.0, 30.0, 2.0, self.mesh)
        capfun = df.project(cap, self.V)

        # Evaluate CAP at different points in the simulation domain
        # and compare them to exact values
        res = np.array([0.0])
        capfun.eval(res, [0.0, 0.0])
        self.assertAlmostEqual(res[0], 0.0)

        capfun.eval(res, [36.0, 33.0])
        self.assertAlmostEqual(res[0], 1.992586024118203,
                               places=2)

        capfun.eval(res, [36.0, 33.0])
        self.assertAlmostEqual(res[0], 1.992586024118203,
                               places=2)

        capfun.eval(res, [14.0, -3.0])
        self.assertAlmostEqual(res[0], 0.0,
                               places=2)

        capfun.eval(res, [20.0, -3.0])
        self.assertAlmostEqual(res[0], 0.0002744904950936554,
                               places=3)
