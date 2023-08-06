"""
Tests for TISE
"""

import unittest
import numpy as np
from scipy.special import jn_zeros
try:
    import dolfin as df
    import mshr
    from ufl import bessel_J
    import_dolfin_ok = True
except BaseException:
    import_dolfin_ok = False

from fiend.tise.tise import solve_tise
from fiend.utils.predefined_potentials import atom_potential_times_rho_expr
from fiend.utils.mesh import mesh_of_sphere_in_cylindrical_coordinates,\
        mesh_domain


@unittest.skipIf(not import_dolfin_ok, "Could not load dolfin")
class TestTISE(unittest.TestCase):
    
    def test_1_hydrogen_eigenvalues(self):
        """Test eigenenergies and eigenstates of Hydrogen"""
        mesh = mesh_of_sphere_in_cylindrical_coordinates(
            radius=30.0,
            core_radius=4.0,
            refinement_radius=15.0,
            cellradius=1.0,
            core_cellradius=0.1)

        rhoV = atom_potential_times_rho_expr('H', mesh)

        evals, evecs = solve_tise(mesh=mesh,
                                  how_many=4,
                                  pot_x_rho=rhoV,
                                  eigensolver_type='rqcg',
                                  eigensolver_tol=1e-6,
                                  eigensolver_max_iterations=100000)
        # Eigenenergies
        np.testing.assert_allclose(evals, [-1 / 2, -1 / (2 * 2**2), -1 / (2 * 2**2),
                                           -1 / (2 * 3**2)], rtol=1e-2)

        V = df.FunctionSpace(mesh, 'Lagrange', 1)
        x = df.SpatialCoordinate(mesh)
        rho = x[0]
        z = x[1]
        r = df.sqrt(rho * rho + z * z)

        # Test eigenstates against analytical solutions
        psi1s = np.sqrt(2) * df.exp(-r)
        diff_dens = df.assemble((psi1s**2 - evecs[0]**2) * rho * df.dx)
        self.assertAlmostEqual(diff_dens, 0)

        psi2s = 0.25 * (2 - r) * df.exp(-r / 2)
        diff_dens = df.assemble((psi2s**2 - evecs[1]**2) * rho * df.dx)
        self.assertAlmostEqual(diff_dens, 0)

        psi2p = 0.25 * z * df.exp(-r / 2)
        diff_dens = df.assemble((psi2p**2 - evecs[2]**2) * rho * df.dx)
        self.assertAlmostEqual(diff_dens, 0)

        psi3s = np.sqrt(2 / 3) / 81 * (27 - 18 * r +
                                       2 * r * r) * df.exp(-r / 3)
        diff_dens = df.assemble((psi3s**2 - evecs[3]**2) * rho * df.dx)
        self.assertAlmostEqual(diff_dens, 0, places=2)

    def test_2_hydrogen_eigenvalues(self):
        """Test eigenenergies and eigenstates of Hydrogen with 2nd order basis"""
        mesh = mesh_of_sphere_in_cylindrical_coordinates(
            radius=30.0,
            core_radius=4.0,
            refinement_radius=15.0,
            cellradius=2.0,
            core_cellradius=0.2)

        rhoV = atom_potential_times_rho_expr('H', mesh)

        evals, evecs = solve_tise(mesh=mesh,
                                  how_many=4,
                                  pot_x_rho=rhoV,
                                  eigensolver_type='rqcg',
                                  eigensolver_tol=1e-6,
                                  eigensolver_max_iterations=100000,
                                  functionspace=('Lagrange', 2))
        # Eigenenergies
        np.testing.assert_allclose(evals, [-1 / 2, -1 / (2 * 2**2), -1 / (2 * 2**2),
                                           -1 / (2 * 3**2)], rtol=1e-2)

        # Test eigenstates agains analytical solutions
        V = df.FunctionSpace(mesh, 'Lagrange', 2)
        x = df.SpatialCoordinate(mesh)
        rho = x[0]
        z = x[1]
        r = df.sqrt(rho * rho + z * z)

        psi1s = np.sqrt(2) * df.exp(-r)
        diff_dens = df.assemble((psi1s**2 - evecs[0]**2) * rho * df.dx)
        self.assertAlmostEqual(diff_dens, 0)

        psi2s = 0.25 * (2 - r) * df.exp(-r / 2)
        diff_dens = df.assemble((psi2s**2 - evecs[1]**2) * rho * df.dx)
        self.assertAlmostEqual(diff_dens, 0)

        psi2p = 0.25 * z * df.exp(-r / 2)
        diff_dens = df.assemble((psi2p**2 - evecs[2]**2) * rho * df.dx)
        self.assertAlmostEqual(diff_dens, 0)

        psi3s = np.sqrt(2 / 3) / 81 * (27 - 18 * r +
                                       2 * r * r) * df.exp(-r / 3)
        diff_dens = df.assemble((psi3s**2 - evecs[3]**2) * rho * df.dx)
        self.assertAlmostEqual(diff_dens, 0, places=2)

    def test_box_partialneumann_eigenstates(self):
        L=2
        R=2
        domain = mshr.Rectangle(df.Point(0,-L), df.Point(R,L))

        from fiend.utils.misc import set_logging
        set_logging(True,0,False,True)
        def refinement_function(rho, z, cr):
            return cr>0.05

        mesh = mesh_domain(domain, refinement_function)

        def db(x, on_boundary):
            return on_boundary and x[0]>0 and x[1] < L

        evals, evecs = solve_tise(mesh=mesh,
                                  how_many=4,
                                  pot_x_rho=df.Constant(0.0),
                                  eigensolver_type='krylovschur',
                                  eigensolver_tol=1e-6,
                                  eigensolver_max_iterations=1000,
                                  dirichlet_boundaries=[db])
        
        rho, z = df.SpatialCoordinate(mesh)
        def get_exact_eigenstate(nrho, nz):
            jnz = jn_zeros(0, nrho)[nrho-1]
            k = (np.pi+nz*2*np.pi)/(4*L)
            fun = bessel_J(0, jnz*rho/R) * df.cos(k*(z-L))
            n2 = df.assemble(fun*fun*rho*df.dx)
            return fun/np.sqrt(n2)
       
        olap = np.abs(df.assemble(evecs[0]*get_exact_eigenstate(1,0)*rho*df.dx))**2
        self.assertAlmostEqual(olap, 1, places=4)

        olap = np.abs(df.assemble(evecs[1]*get_exact_eigenstate(1,1)*rho*df.dx))**2
        self.assertAlmostEqual(olap, 1, places=4)

        olap = np.abs(df.assemble(evecs[2]*get_exact_eigenstate(1,2)*rho*df.dx))**2
        self.assertAlmostEqual(olap, 1, places=4)

        olap = np.abs(df.assemble(evecs[3]*get_exact_eigenstate(2,0)*rho*df.dx))**2
        self.assertAlmostEqual(olap, 1, places=4)

