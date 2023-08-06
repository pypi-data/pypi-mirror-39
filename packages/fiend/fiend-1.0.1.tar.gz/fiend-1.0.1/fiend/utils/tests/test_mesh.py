"""
Tests for mesh generation
"""

import unittest

# These tests should be run only if dolfin can be imported
try:
    import dolfin as df
    import numpy as np
    from fiend.utils.mesh import mesh_of_sphere_in_cylindrical_coordinates as\
        get_mesh
    from fiend.utils.mesh import extract_shell
    from fiend.utils.misc import triangle_incenter
    import_dolfin_ok = True
except Exception as e:
    print(repr(e))
    import_dolfin_ok = False


@unittest.skipIf(not import_dolfin_ok, "Could not load dolfin")
class TestHalfCircleMesh(unittest.TestCase):

    def test_max_resolution1(self):
        """Test that all circumradii of elements are less than max."""
        max_cell_circumradius = 2.0
        mesh = get_mesh(radius=50.0,
                        core_radius=2.0,
                        refinement_radius=1.0,
                        cellradius=max_cell_circumradius,
                        core_cellradius=1.0)

        cell_circumradii = np.array([cell.circumradius() for cell in
                                     df.cells(mesh)])

        all_cells_small_enough = np.all(
            cell_circumradii <= max_cell_circumradius)

        self.assertTrue(all_cells_small_enough)

    def test_mesh_overall_refinement(self):
        """Test refined mesh element sizes"""
        max_cell_circumradius = 10.0
        A = 0.01
        a = 5.0
        b = 200.0
        mesh = get_mesh(radius=500.0,
                        core_radius=5.0,
                        refinement_radius=b,
                        cellradius=max_cell_circumradius,
                        core_cellradius=A * 5)

        def get_distance(cell):
            vrtx_coordinates = cell.get_vertex_coordinates()
            rho_c, z_c = triangle_incenter(
                np.array(vrtx_coordinates).reshape(3, 2))

            return np.sqrt(rho_c**2 + z_c**2)

        cell_data = np.array([[get_distance(cell),
                               cell.circumradius()]
                              for cell in df.cells(mesh)])
        r = cell_data[:, 0]
        expected_max_circumradii = (1 - (1 - A) * a / (r + 1e-18) * np.tanh(r / a)
                                    * np.exp(- (r / b)**2)) * max_cell_circumradius
        idx = np.where(r == 0)[0]
        expected_max_circumradii[idx] = 0.02 * max_cell_circumradius
        cell_data_ok = cell_data[:, 1] <= expected_max_circumradii
        self.assertTrue(np.all(cell_data_ok))


@unittest.skipIf(not import_dolfin_ok, "Could not load dolfin")
class TestMeshUtils(unittest.TestCase):

    def test_shell_extraction(self):
        """Test extraction of a small part of mesh"""
        mesh = get_mesh(5, 5, 5, 0.1, 0.1)

        def path(s):
            return 4 * np.array([np.sin(s * np.pi),
                                 np.cos(s * np.pi)])

        smesh = extract_shell(mesh, path)

        for cell in df.cells(smesh):
            center = triangle_incenter(
                np.array(cell.get_vertex_coordinates()).reshape(3, 2))
            self.assertLess(np.fabs(np.linalg.norm(center) - 4), 0.15)
