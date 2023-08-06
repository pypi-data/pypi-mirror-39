import unittest
import pathlib
import re

from scipy.integrate import quad
import numpy as np
import dolfin as df
import mshr
from mpi4py import MPI

from fiend.pulseconfig_parser.laser import Laser
from fiend.pulseconfig_parser.singlecolorlaserpulse import SingleColorLaserPulse
from fiend.analysis._pes_tsurff import compute_vectorpotential_and_integrals,\
    _compute_derivatives,\
    compute_instantaneous_amplitude_wo_prefactor,\
    get_facet_normal, photoelectron_amplitude
from fiend.utils.mesh import mesh_of_sphere_in_cylindrical_coordinates\
    as get_mesh
from fiend.utils.mesh import save_mesh, load_mesh
from fiend.utils.mesh import extract_equiradial_shell
from fiend.utils.dolfin import extract_arcspaces, project_cylindrical


class TestTsurffPES(unittest.TestCase):
    def test_vecpot_related_computations(self):
        """Test preprocessing of vector potential"""

        Afield = Laser()
        Afield.add_pulse(SingleColorLaserPulse(A=0.1,
                                               w=0.0569,
                                               k=0,
                                               tau=20,
                                               sigma=200,
                                               phi=np.pi / 3))

        time = np.linspace(Afield.beginning_of_pulse(), Afield.end_of_pulse(),
                           1000)

        Avals, Aint, A2int = compute_vectorpotential_and_integrals(
            MPI.COMM_SELF, time, Afield)
        np.testing.assert_allclose(Avals, Afield(time))

        Aint_ref = [quad(Afield, time[0], t)[0] for t in time]
        np.testing.assert_allclose(Aint, Aint_ref, rtol=0, atol=1e-5)

        A2int_ref = [quad(lambda tau: Afield(tau)**2, time[0], t)[0] for t in
                     time]
        np.testing.assert_allclose(A2int, A2int_ref, rtol=0, atol=1e-5)

    def test_bkt_wo_prefactor(self):
        # Prepare functionspace
        dx = 0.01
        rmax = 3.1
        num_angles = 1000

        rmesh = get_mesh(rmax, rmax, rmax, dx, dx)
        rfunspace = df.FunctionSpace(rmesh, 'Lagrange', 1)

        # Prepare fake wavefunction
        rho, z = df.SpatialCoordinate(rmesh)
        function_re = df.project(rho * z * 0.5 + df.cos(z), rfunspace)
        function_im = df.project(df.exp(-rho * z**2) * df.sin(rho), rfunspace)

        lfunspace, sfunspace = extract_arcspaces(rfunspace, 3, num_angles)
        lfunspace2 = df.VectorFunctionSpace(lfunspace.mesh(), 'Lagrange', 1,
                                            dim=2)
        sfunspace2 = df.VectorFunctionSpace(sfunspace.mesh(), 'Lagrange', 1,
                                            dim=2)
        normal = get_facet_normal(lfunspace.mesh())
        lfun_re, grad_lfun_re = _compute_derivatives(function_re,
                                                     sfunspace,
                                                     lfunspace,
                                                     sfunspace2,
                                                     lfunspace2)
        lfun_im, grad_lfun_im = _compute_derivatives(function_im,
                                                     sfunspace,
                                                     lfunspace,
                                                     sfunspace2,
                                                     lfunspace2)
        rho, z = df.SpatialCoordinate(lfunspace)
        At = 0.1
        krho = 0.2
        kz = 0.2

        kr = df.Expression('krho * x[0] + kz * x[1]', krho=krho, kz=kz,
                           degree=1)

        beta = df.Constant((0.5 * krho, At + 0.5 * kz))
        krho = df.Constant(krho)
        kz = df.Constant(kz)
        coskr = df.cos(krho * rho + kz * z)
        sinkr = df.sin(krho * rho + kz * z)

        bkt_wo_prefactor = compute_instantaneous_amplitude_wo_prefactor(
            coskr,
            sinkr,
            beta,
            lfun_re,
            lfun_im,
            grad_lfun_re,
            grad_lfun_im,
            normal)
        bkt_wo_prefactor_ref = -0.23637948800021108 + 3.193552298203715j

        self.assertAlmostEqual(np.abs(bkt_wo_prefactor -
                                      bkt_wo_prefactor_ref), 0.0, places=2)

    def test_analytical_result(self):
        """Compare PES of computed vs analytical result"""

        # Prepare functionspace
        rmax = 30.1
        num_angles = 1000
        tsurff_radius = 25
        krho = 1
        kz = 1
        omega= 0.5
        if pathlib.Path('pes_test_mesh.h5').exists():
            rmesh = load_mesh(MPI.COMM_WORLD, 'pes_test_mesh.h5')
        else:
            rmesh = get_mesh(rmax, 
                         core_radius = 5, 
                         refinement_radius = 20,
                         cellradius = 0.3,
                         core_cellradius = 0.01)

            save_mesh('pes_test_mesh.h5', rmesh)


        rfunspace = df.FunctionSpace(rmesh, 'Lagrange', 1)
        
        pattern = re.compile('data/tdse_wavefunction/(?P<type>(imag|real))part_iteration_(?P<iter>\d+)_real')

        Afield = Laser()
        Afield.add_pulse(SingleColorLaserPulse(A=0.0,
                                               w=0.0569,
                                               k=0,
                                               tau=20,
                                               sigma=30,
                                               phi=np.pi / 3))

        time = np.linspace(Afield.beginning_of_pulse(), Afield.end_of_pulse(),
                           100)
        saveslot_indices = np.arange(0, len(time), 1, dtype=int)
        Avals, Aint, A2int = compute_vectorpotential_and_integrals(
            MPI.COMM_SELF, time, Afield)
        
        def function_loader(name, funspace):
            m = pattern.match(name)
            ctype = m.group('type')
            iteration = int(m.group('iter'))
            t = time[iteration]     
            rho, z = df.SpatialCoordinate(funspace.mesh())
            r = df.sqrt(rho**2+z**2)
            if ctype == 'real':
                expr = df.cos(omega*t-krho*rho-kz*z)
            elif ctype == 'imag':
                expr = df.sin(omega*t-krho*rho-kz*z)
            else:
                raise RuntimeError("Programming error")

            return project_cylindrical(expr, funspace)

        bp = photoelectron_amplitude(MPI.COMM_WORLD, tsurff_radius, num_angles,
                                     rfunspace, time[0], time,
                                     saveslot_indices, Avals, Aint, A2int,
                                     custom_load_function =
                                     function_loader)

        bmesh = get_mesh(3,3,3,0.1,0.1)
        bfunspace = df.FunctionSpace(bmesh, 'Lagrange', 1)
        Arpes = df.project(bp[0]**2+bp[1]**2, bfunspace)
        import IPython; IPython.embed()
