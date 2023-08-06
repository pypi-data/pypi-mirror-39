"""
Tests for propagators
"""
import unittest
import os
from mpi4py import MPI
import numpy as np

try:
    import dolfin as df
    from fiend.tdse.tdse import tdse_setup, save_tdse_preparation
    from fiend.utils.predefined_potentials import atom_potential_times_rho_expr
    from fiend.utils.mesh import mesh_of_sphere_in_cylindrical_coordinates
    import_dolfin_ok = True
except BaseException:
    import_dolfin_ok = False


@unittest.skipIf(not import_dolfin_ok, "Could not load dolfin")
class PreparePropagationTests(unittest.TestCase):

    def test_prepare(self):
        """Prepare initial state for propagation tests"""
        mesh = mesh_of_sphere_in_cylindrical_coordinates(
            radius=30.0,
            core_radius=4.0,
            refinement_radius=10,
            cellradius=0.5,
            core_cellradius=0.01
        )

        rhoV = atom_potential_times_rho_expr('H', mesh)

        V = df.FunctionSpace(mesh, 'Lagrange', 1)
        rho, z = df.SpatialCoordinate(mesh)
        r = df.sqrt(rho * rho + z * z)

        psi_1s = np.sqrt(2) * df.exp(-r)
        psi_2s = 0.25 * (2 - r) * df.exp(-r / 2)

        psi0 = 1 / np.sqrt(2) * (psi_1s + psi_2s)

        psi_1s = df.project(psi_1s, V)
        psi_2s = df.project(psi_2s, V)

        S, S0, S1, H0, partialRho, partialZ, Rho, Z, CAP, ACC \
            = tdse_setup(
                mesh,
                atom_potential_times_rho_expr('H', mesh),
                0.0, 1.0, ('Lagrange', 1))

        save_tdse_preparation(MPI.COMM_WORLD, mesh, [psi_1s, psi_2s],
                              H0, S, S0, S1, partialRho, partialZ, Rho, Z, CAP, ACC)
