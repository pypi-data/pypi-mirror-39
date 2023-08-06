"""
Implementation of time evolution operators
"""
from abc import ABC, abstractmethod
import logging
from typing import Callable, Text

from mpi4py import MPI
from petsc4py import PETSc
from slepc4py import SLEPc

from fiend.utils.custom_matrices import *


class saver_interfacer:
    def __init__(self, step_nbr: int,
                 time: float,
                 psi: PETSc.Vec,
                 laserfield: float):
        self.step_nbr = step_nbr
        self.time = time
        self.psi = psi
        self.laserfield = laserfield

    def getField(self) -> float:
        return self.laserfield

    def getTime(self) -> float:
        return self.time

    def getSolution(self) -> PETSc.Vec:
        return self.psi

    def getStepNumber(self) -> int:
        return self.step_nbr

    def __instancecheck__(self, instance):

        def _check_callable(name, instance):
            clb = getattr(instance, name, None)
            return callable(clb)

        has_methods = [name for name in ["getTime", "getSolution",
                                         "getStepNumber"]
                       if _check_callable(name, instance)]

        return len(has_methods) == 3


class Propagator(ABC):
    """
    Base class for propagators
    """

    def __init__(self):

        def default_post_step_handler(ts):
            logging.info("Step %d: t=%f" % (ts.getStepNumber(), ts.getTime()))

        self.post_step_handler = default_post_step_handler

        def default_pre_step_handler(ts):
            ...

        self.pre_step_handler = default_pre_step_handler

    @abstractmethod
    def propagate(self, psi0: PETSc.Vec):
        ...

    def set_post_step_handler(self, handler: Callable):
        """
        This sets the function that should be called after each time-step. It's
        call signature is f( time_stepper ) where time_stepper should be an
        instance of 'saver_interfacer'.
        """
        self.post_step_handler = handler

    def set_pre_step_handler(self, handler: Callable):
        """
        This sets the function that should be called before each time-step. It's
        call signature is f( time_stepper ) where time_stepper should be an
        instance of 'saver_interfacer'.
        """
        self.pre_step_handler = handler


class KrylovPropagator(Propagator):
    """Propagation using Krylov subspace to approximate the matrix exponential.
    Note that this differs from most other implementations since we use the
    overlap-induced inner product instead of the normal L2-norm of the vector
    space."""

    def __init__(self,
                 S: PETSc.Mat,
                 H0: PETSc.Mat,
                 W: PETSc.Mat,
                 laserfield: Callable, **kwargs):
        raise NotImplementedError("Expmid propagator is not currently working")
        self.dt = kwargs['delta_t']
        self.num_steps = int(kwargs['max_t'] / self.dt) + 1

        self.comm = MPI.COMM_WORLD

        self.H_oper = MatSum_oper(self.comm, H0, W, 0.0)
        self.H = self.H_oper.getPETScMat()
        self.H.name = 'TD Hamiltonian'
        self.S = S
        self.S.name = 'OVERLAP'

        inverse_tolerance = kwargs.get('inverse_tolerance',
                                       2 * np.finfo(float).eps)
        ilu_factor_levels = kwargs.get('ilu_factor_levels',
                                       5)

        if self.comm.size == 1:
            self._solver_type = kwargs.get('solver_type', 'superlu')
        else:
            self._solver_type = kwargs.get('solver_type', 'superlu_dist')
        if self._solver_type == 'krylov':
            self.Sinv = MatInvKrylov_oper(self.comm,
                                          self.S,
                                          self.S,
                                          self.S,
                                          inverse_tolerance,
                                          ilu_factor_levels=ilu_factor_levels,
                                          ilu_no_shift=True
                                          ).getPETScMat()
        else:
            self.Sinv = MatInvDirect_oper(
                self.comm, self.S,
                self._solver_type,
                inverse_tolerance
            ).getPETScMat()

        self.SinvH = MatMult_oper(self.comm, self.Sinv, self.H).getPETScMat()
        self.SinvH.name = 'S^-1 H(t)'
        self.expSinvH = MatFN_oper(self.comm, self.SinvH, 'exp',
                                   self.S, -1j * self.dt,
                                   tolerance=kwargs.get('matexp_tolerance',
                                                          2 * np.finfo(float).eps)).getPETScMat()
        self.wrk = self.S.getVecRight()
        self.laserfield = laserfield
        Propagator.__init__(self)

    def propagate(self, psi: PETSc.Vec) -> None:
        logging.debug("Beginning propagation from t=0 to t=%.1f" %
                      (self.num_steps * self.dt))

        iteration = 0
        lf = self.laserfield(iteration * self.dt + self.dt / 2.0)
        self.pre_step_handler(saver_interfacer(iteration, 0.0, psi, lf))
        self.post_step_handler(saver_interfacer(iteration,
                                                0.0,
                                                psi,
                                                lf))

        for iteration in range(self.num_steps):
            lf = self.laserfield(iteration * self.dt + self.dt / 2.0)
            time = iteration * self.dt
            self.pre_step_handler(saver_interfacer(iteration, time, psi, lf))

            self.H_oper.set_scalar(lf)
            self.expSinvH.mult(psi, self.wrk)
            psi.swap(self.wrk)

            time = (iteration + 1) * self.dt
            self.post_step_handler(
                saver_interfacer(iteration + 1, time, psi, lf))

        logging.debug("Propagation complete")


class PETScPropagator(Propagator):
    implemented_propagators = {
        'cn': (PETSc.TS.Type.CN, PETSc.TS.EquationType.ODE_EXPLICIT),
        'alpha': (PETSc.TS.Type.ALPHA, PETSc.TS.EquationType.ODE_EXPLICIT),
    }

    def __init__(self,
                 S: PETSc.Mat,
                 H0: PETSc.Mat,
                 W: PETSc.Mat,
                 laserfield: Callable,
                 propagatortype: Text,
                 **kwargs):
        super().__init__()
        self.comm = MPI.COMM_WORLD
        self.ts = PETSc.TS().create(comm=self.comm)

        # Set the time stepper correctly for the selected propagator
        logging.debug("Using propagator " + propagatortype)
        proptype, eqntype = self.implemented_propagators[propagatortype]
        self.ts.setType(proptype)
        self.ts.setProblemType(PETSc.TS.ProblemType.LINEAR)
        self.ts.setEquationType(eqntype)

        self.ts.setTimeStep(kwargs['delta_t'])
        self.ts.setMaxTime(kwargs['max_t'])
        self.ts.setExactFinalTime(PETSc.TS.ExactFinalTime.MATCHSTEP)

        # Set time-stepper's linear solver
        inverse_tolerance = kwargs.get('inverse_tolerance',
                                       2 * np.finfo(float).eps)
        ilu_factor_levels = kwargs.get('ilu_factor_levels',
                                       5)
        boundary_metric = kwargs.get('boundary_metric', None)
        logging.debug("Setting up linear solver of the propagator...")
        ksp = self.ts.getKSP()
        if self.comm.size > 1:
             set_ksp(ksp, S, S, preconditioner='lu',
                    inverse_tolerance=inverse_tolerance,
                    ilu_factor_levels=ilu_factor_levels, 
                    boundary_metric=boundary_metric)
        else:
            set_ksp(ksp, S, S, preconditioner='ilu',
                    inverse_tolerance=inverse_tolerance,
                    ilu_factor_levels=ilu_factor_levels,
                    boundary_metric=boundary_metric)

        # Set the equation of motion correctly for the given
        # equation type required by the time stepper
        self.S = S
        self.S.name = 'OVERLAP'

        if eqntype == PETSc.TS.EquationType.ODE_EXPLICIT:
            G = self.S.getVecRight()
            self.ts.setRHSFunction(PETSc.TS.computeRHSFunctionLinear, G)
            
            def RHSjac(ts, t, u, Amat, Pmat):
                H0.copy(Amat)
                Amat.axpy(laserfield(t), W,
                          structure=PETSc.Mat.Structure.SUBSET)

            RJAC = self.S.duplicate()

            if 'RHSjac' in kwargs:
                self.ts.setRHSJacobian(kwargs['RHSjac'], RJAC, self.S)
            else:
                self.ts.setRHSJacobian(RHSjac, RJAC, self.S)

            def LHSfun(ts, t, c, c_t, F):
                self.S.mult(c_t, F)
                F.scale(1j)

            F = self.S.getVecRight()
            self.ts.setIFunction(LHSfun, F)

            IJAC = self.S.duplicate()

            def LHSjac(ts, t, c, c_t, sigma, A, B):
                self.S.copy(A)
                A.scale(1j * sigma)

            self.ts.setIJacobian(LHSjac, IJAC)
        else:
            raise NotImplementedError

        if proptype == PETSc.TS.Type.ALPHA:
            if 'alpha_radius' in kwargs:
                alpha_radius = kwargs['alpha_radius']
                self.ts.setAlphaRadius(alpha_radius)
            if 'alpha_m' in kwargs:
                alpha_m = kwargs['alpha_m']
            else:
                alpha_m = None
            if 'alpha_f' in kwargs:
                alpha_f = kwargs['alpha_f']
            else:
                alpha_f = None
            if 'alpha_gamma' in kwargs:
                alpha_gamma = kwargs['alpha_gamma']
            else:
                alpha_gamma = None

            if alpha_m or alpha_f or alpha_gamma:
                self.ts.setAlphaParams(alpha_m=alpha_m, alpha_f=alpha_f,
                                       gamma=alpha_gamma)

    def propagate(self, psi: PETSc.Vec) -> None:
        self.ts.setPostStep(self.post_step_handler)
        self.ts.setPreStep(self.pre_step_handler)

        self.ts.setTime(0.0)
        self.ts.setSolution(psi)

        self.ts.setUp()
        self.post_step_handler(self.ts)  # To save the 0th iteration

        self.ts.solve(psi)
