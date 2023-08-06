import unittest
try:
    import dolfin as df
    import numpy as np
    from fiend.utils.mesh import mesh_of_sphere_in_cylindrical_coordinates as\
        get_mesh
    from fiend.utils.custom_matrices import set_ksp
    from fiend.utils.dolfin import project_fast, get_petsc_vec, wfnorm
    from petsc4py import PETSc
    from mpi4py import MPI
    import_dolfin_ok = True
except BaseException:
    import_dolfin_ok = False


@unittest.skipIf(not import_dolfin_ok, "Could not load dolfin")
class TestDolfinUtils(unittest.TestCase):

    def test_project_fast(self):
        """Test fast projection"""
        mesh = get_mesh(radius=10.0,
                        core_radius=10.0,
                        refinement_radius=10.0,
                        cellradius=0.05,
                        core_cellradius=0.05)

        funspace = df.FunctionSpace(mesh, 'Lagrange', 1)
        v = df.TestFunction(funspace)
        f = df.TrialFunction(funspace)

        overlap_form = v * f * df.dx
        overlap = df.assemble(overlap_form)
        pcmat = df.as_backend_type(overlap).mat()

        wrkmat = df.PETScMatrix(pcmat.duplicate(copy=False))
        wrkvec = df.PETScVector(pcmat.getVecRight())

        fun = df.Function(funspace)

        ksp = PETSc.KSP().create(comm=MPI.COMM_SELF)
        set_ksp(ksp, pcmat, pcmat, preconditioner='ilu',
                inverse_tolerance=1e-16, ilu_factor_levels=2)
        expr = df.Expression('x[0]*x[1]+2.0', degree=2)
        project_fast(expr, funspace, fun, wrkmat, wrkvec, ksp, pcmat)

        self.assertAlmostEqual(fun(0.1, 0.2), 0.1 * 0.2 + 2.0, places=3)


@unittest.skipIf(not import_dolfin_ok, "Could not load dolfin")
class TestGetPETScVec(unittest.TestCase):
    def setUp(cls):
        cls.mesh = get_mesh(
            radius=50.0,
            core_radius=3.0,
            refinement_radius=40.0,
            cellradius=1.0,
            core_cellradius=0.1)

        cls.V = df.FunctionSpace(cls.mesh, 'Lagrange', 2)

    def test(self):
        """Testing correctness of references"""
        fun = df.Function(self.V)

        pvec = get_petsc_vec(fun)

        pvec[0] = 154
        pvec.assemble()

        self.assertEqual(fun.vector().vec()[0], 154)


@unittest.skipIf(not import_dolfin_ok, "Could not load dolfin")
class TestWFNORM(unittest.TestCase):

    def test_wavefunction_norm_dolfin(self):
        mesh = get_mesh(radius=50.0,
                        core_radius=4.0,
                        refinement_radius=20.0,
                        cellradius=2,
                        core_cellradius=0.01)

        V = df.FunctionSpace(mesh, 'Lagrange', 1)
        x = df.SpatialCoordinate(mesh)
        rho = x[0]
        z = x[1]
        r = df.sqrt(rho * rho + z * z)
        psi = np.sqrt(1 / np.pi) * df.exp(-r)

        psi = df.project(psi, V)
        res = wfnorm(psi)
        self.assertAlmostEqual(res, 1 / (2 * np.pi),
                               places=4)
