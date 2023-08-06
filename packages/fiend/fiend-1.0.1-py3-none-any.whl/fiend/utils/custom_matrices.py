"""
PETSc-compatible custom matrices that
do not compute the resulting matrix explicitely but
instead offer matrix-vector products.
"""

import logging
from typing import Dict, Union

from petsc4py import PETSc
from slepc4py import SLEPc
from mpi4py import MPI
import numpy as np
from abc import ABC, abstractmethod


def _ksp_custom_convergence_test(ksp, it, rnorm,
                                 metric_matrix, wrkvec1, wrkvec2,
                                 boundary_metric):
    """
    Custom convergence test for PETSc's sparse solvers. This will
    compute the residual norm ||Ax-b|| using the bilinear
    product induced by the metric matrix.

    Parameters
    ----------
    ksp : PETSc.KSP
        Solver
    it : int
        iteration number
    rnorm : float
        estimate of the residual norm computed by PETSc
    metric_matrix : petsc4py.PETSc.Mat
    wrkvec1 : petsc4py.PETSc.Vec
        a preallocated work vector
    wrkvec2 : petsc4py.PETSc.Vec
        a preallocated work vector

    Returns
    -------
    bool : true if computed residual norm is less than tolerance, false
           otherwise
    """
    tolerance = ksp.getTolerances()[1]
    ksp.buildResidual(wrkvec1)
    metric_matrix.mult(wrkvec1, wrkvec2)
    residual_norm = np.abs(wrkvec2.dot(wrkvec1))
    if boundary_metric: 
        boundary_metric[0].mult(wrkvec1, wrkvec2)
        boundary_residual = boundary_metric[1]*wrkvec2.norm(norm_type =
        PETSc.NormType.NORM_2)
    else:
        boundary_residual=0

    residual_norm += boundary_residual
    ksp.setResidualNorm(residual_norm)
    return residual_norm < tolerance


def _ksp_custom_monitor(ksp, it, rnorm):
    prefix = ksp.getOperators()[0].getName()
    logging.info(prefix + ": %d %f" % (it, rnorm))


def set_ksp(ksp, pcmat, metric, preconditioner, inverse_tolerance,
            ilu_factor_levels=None, lu_no_shift=True,
            debug=False, options_prefix=None,
            boundary_metric = None):
    """
    Sets a krylov subspace linear solver to use GMRES with QDYN's default
    options.

    Parameters
    ----------
    ksp : petsc4py.PETSc.KSP
    pcmat : petsc4py.PETSc.Mat
        Preconditioner matrix
    metric : petsc4py.PETSc.Mat
        Metric matrix
    preconditioner : string (either 'jacobi' or 'ilu')
    inverse_tolerance : float
        absolute tolerance of the method
    ilu_factor_levels : int
        Number of levels for ILU factorization of the preconditioner
    ilu_no_shift : bool
        Shift / no shift of ILU preconditioner
    """

    ksp.setType(PETSc.KSP.Type.GMRES)
    ksp.setTolerances(atol=inverse_tolerance)

    pc = ksp.getPC()
    logging.debug("    using residual norm with respect to " +
                  pcmat.name)

    logging.debug("    absolute tolerance: %g" % inverse_tolerance)
    wrk1 = pcmat.getVecRight()
    wrk2 = pcmat.getVecRight()
    if metric:
        ksp.setConvergenceTest(_ksp_custom_convergence_test,
                               args=(metric, wrk1, wrk2, boundary_metric))
    if debug:
        ksp.setMonitor(_ksp_custom_monitor)
    if preconditioner == 'jacobi':
        pc.setType('jacobi')
        pcname = 'jacobi'
    elif preconditioner == 'ilu':
        pc.setType('ilu')  # ILU seems to be faster than ICC for our
        # matrices, wonder why.
        assert isinstance(ilu_factor_levels, int)
        pc.setFactorLevels(ilu_factor_levels)
        if lu_no_shift:
            pc.setFactorShift(None)
        pcname = 'incomplete LU'
        ksp.setNormType(PETSc.KSP.NormType.NORM_PRECONDITIONED)
        logging.debug(
            "    with " + pcname + " preconditioner using " + pcmat.name.upper()
        )
    elif preconditioner == 'lu':
        pc.setType('lu')  # ILU seems to be faster than ICC for our
        # matrices, wonder why.
        if lu_no_shift:
            pc.setFactorShift(None)
        pcname = 'LU'
        ksp.setNormType(PETSc.KSP.NormType.NORM_PRECONDITIONED)
        logging.debug(
            "    with " + pcname + " preconditioner using " + pcmat.name.upper()
        )
        
    elif preconditioner is None or preconditioner == 'none':
        ...
    else:
        raise RuntimeError("Unknown preconditioner %s" % preconditioner)

    if options_prefix:
        ksp.setOptionsPrefix(options_prefix)
        pc.setOptionsPrefix(options_prefix)
    ksp.setFromOptions()
    pc.setFromOptions()

class CustomMatrixContext(ABC):

    """
    Base class for all fiend's custom matrix classes.
    """

    def __init__(self, comm: MPI.Comm):
        """
        Parameters
        ----------
        comm : mpi4py.MPI.Comm
        """
        self.comm = comm
        self.norms = {}
        self.rng = PETSc.Random().create(comm=self.comm)

    def getPETScMat(self):
        """
        Returns the matrix as PETSc.Mat.

        Returns
        -------
        mat : petsc4py.PETSc.Mat
        """

        mat = PETSc.Mat().create(comm=self.comm)
        mat.setType('python')

        # Use petsc4py.PETSc.Mat.setSizes to set the local
        # and block sizes correctly
        mat.setSizes(self.getSizes())
        mat.setPythonContext(self)

        mat.setUp()

        return mat

    @abstractmethod
    def getSizes(self):
        """
        Return the local and global sizesof the matrix.

        Returns
        -------
        tuple of two pairs:
            First pair is the local and global size of the first
            dimension of the matrix; second pair of the second dimension.
        """
        ...

    @abstractmethod
    def createVecRight(self):
        """
        Sets up a vector that's compatible with the right side
        of this matrix.

        Returns
        -------
        petsc4py.PETSc.Mat
        """
        ...

    @abstractmethod
    def getLocalSize(self):
        """
        Returns local size of this matrix. (Local = on this MPI process)

        Returns
        -------
        tuple
        """
        ...

    @abstractmethod
    def mult(self, M: PETSc.Mat, x: PETSc.Vec, y: PETSc.Vec):
        """
        Implements the multiplication y = M x.

        Parameters
        ----------
        self
        M : For petsc api compliance, not actually used
        x : petsc4py.PETSc.Vec
        y : petsc4py.PETSc.Vec

        Returns
        -------
        None
        """
        ...

    def __matmult__(self, v: PETSc.Vec,
                    out: PETSc.Vec = None) -> PETSc.Vec:
        """
        Implements the matrix-vector multiplication.

        Parameters
        ----------
        v : petsc4py.PETSc.Vec
            The matrix to be multiplied.
        out : petsc4py.PETSc.Vec (optional)
            The matrix where we save the result. Will be created if not
            supplied.

        Returns
        -------
        petsc4py.PETSc.Vec
        """

        if not out:
            out = self.createVecRight()

        self.mult(None, v, out)

        return out

    @abstractmethod
    def norm(self, M, norm_type: PETSc.NormType) -> float:
        """
        Computes (a lower approximation) of the matrix norm.

        Parameters
        ----------
        self
        M -- not needed
        norm_type : petsc4py.PETSc.NormType

        Returns
        -------
        float
        """
        ...


class MatMult_oper(CustomMatrixContext):
    """Product of two matrices A and B"""

    def __init__(self, comm: MPI.Comm,
                 matrixA: PETSc.Mat,
                 matrixB: PETSc.Mat):
        """
        Parameters
        ----------
        comm : mpi4py.MPI.Comm
        matrixA : petsc4py.PETSc.Mat
        matrixB : petsc4py.PETSc.Mat
        """
        CustomMatrixContext.__init__(self, comm)

        self.A = matrixA
        self.B = matrixB
        self.wrkBx = self.A.createVecRight()

    def getLocalSize(self):
        return self.A.getLocalSize()

    def getSizes(self):
        return self.A.getSizes()

    def createVecRight(self):
        return self.A.createVecRight()

    def mult(self, M, x: PETSc.Vec, y: PETSc.Vec):
        self.B.mult(x, self.wrkBx)
        self.A.mult(self.wrkBx, y)

    def multTranspose(self, M, x: PETSc.Vec, y: PETSc.Vec):
        self.A.multTranspose(x, self.wrkBx)
        self.B.multTranspose(self.wrkBx, y)

    def norm(self, M, norm_type: PETSc.NormType):
        return self.A.norm(norm_type) * self.B.norm(norm_type)


class MatSum_oper(CustomMatrixContext):
    """Computes y= A*x + r*B*x where A is a matrix,  r is a scalar, and B is a
    matrix."""

    def __init__(self, comm: MPI.Comm,
                 matrixA: PETSc.Mat,
                 matrixB: PETSc.Mat,
                 scalar: Union[float, complex]):
        """
        Parameters
        ----------
        comm : mpi4py.MPI.Comm
        matrixA : petsc4py.PETSc.Mat
        matrixB : petsc4py.PETSc.Mat
        scalar : float or complex (complex allowed only if PETSc.ScalarType()
                 is complex)
        """
        CustomMatrixContext.__init__(self, comm)

        self.A = matrixA
        self.B = matrixB
        self.scalar = scalar
        self.wrkrBx = self.A.createVecRight()

    def set_scalar(self, scalar: Union[float, complex]):
        self.scalar = scalar

    def getLocalSize(self):
        return self.A.getLocalSize()

    def getSizes(self):
        return self.A.getSizes()

    def createVecRight(self):
        return self.A.createVecRight()

    def mult(self, M, x: PETSc.Vec, y: PETSc.Vec):
        if self.scalar != 0:
            self.B.mult(x, self.wrkrBx)
            self.wrkrBx *= self.scalar

            self.A.multAdd(x, self.wrkrBx, y)
        else:
            self.A.mult(x, y)

    def multTranspose(self, M, x: PETSc.Vec, y: PETSc.Vec):
        if self.scalar != 0:
            self.B.multTranspose(x, self.wrkrBx)
            self.wrkrBx *= self.scalar

            self.A.multTransposeAdd(x, self.wrkrBx, y)
        else:
            self.A.multTranspose(x, y)

    def multHermitian(self, M, x: PETSc.Vec, y: PETSc.Vec):
        if self.scalar != 0:
            self.B.multTranspose(x, self.wrkrBx)
            self.wrkrBx *= np.conj(self.scalar)

            self.A.multTransposeAdd(x, self.wrkrBx, y)
        else:
            self.A.multTranspose(x, y)

    def norm(self, M, norm_type: PETSc.NormType):
        if norm_type == 2:
            rn = np.abs(self.scalar)**2
        else:
            rn = np.abs(self.scalar)

        return self.A.norm(norm_type) + rn * self.B.norm(norm_type)


class MatInvDirect_oper(CustomMatrixContext):
    """Matrix inverse (that is not explicitely evaluated) using a parallel
    direct solver (typically superlu or mumps)."""

    def __init__(self, comm: MPI.Comm,
                 matrix: PETSc.Mat,
                 lusolver: str = 'mumps',
                 tolerance: float = 10 * np.finfo(float).eps,
                 norm_ntests: int = 3):
        """
        Parameters
        ----------
        comm : mpi4py.MPI.Comm
        matrix : petsc4py.PETSc.Mat
        tolerance : float
            relative tolerance of matrix inverse times a vector
        norm_ntests : int
            Number of random sample vectors when computing the norm
        lusolver : str
            Name of the direct solver to use
        """

        CustomMatrixContext.__init__(self, comm)
        self.mat = matrix
        self.norm_ntests = norm_ntests

        self.matfun = PETSc.KSP().create(comm=comm)
        self.matfun.setType('preonly')
        self.matfun.setTolerances(rtol=tolerance)
        self.matfun.setOperators(self.mat)
        pc = self.matfun.getPC()
        if (lusolver == 'mumps' or lusolver ==
                'superlu_dist') and matrix.isSymmetricKnown()[1]:
            logging.debug(("Using MUMPS with Cholesky factorization for the "
                           "inverse of " + self.mat.name))
            factorization_type = PETSc.PC.Type.CHOLESKY
        else:
            logging.debug(("Using " + lusolver.upper() + " with LU factorization"
                           " for the inverse of " + self.mat.name))
            factorization_type = PETSc.PC.Type.LU

        logging.debug(("  with relative tolerance: %g" % tolerance))

        pc.setType(factorization_type)
        pc.setFactorSolverType(lusolver)
        pc.setUp()
        self.matfun.setNormType(PETSc.KSP.NormType.NORM_UNPRECONDITIONED)
        self.matfun.setUp()
        self.wrkvec = self.createVecRight()

    def getLocalSize(self):
        return self.mat.getLocalSize()

    def getSizes(self):
        return self.mat.getSizes()

    def createVecRight(self):
        return self.mat.createVecRight()

    def mult(self, M, x: PETSc.Vec, y: PETSc.Vec):
        """Multiplies the vector x and stores the result in y"""

        self.matfun.solve(x, y)

        return y

    def _calculate_norms(self, norm_type: PETSc.NormType):
        """Lazy evaluation of matrix norms"""
        # Estimate norm

        if norm_type == 4:  # i.e., compute L1 and L2 norms
            _tmp = np.zeros(2)
        else:
            _tmp = 0.0

        for i in range(self.norm_ntests):
            self.wrkvec.setRandom(self.rng)
            wrkvec2 = self.mat.createVecRight()
            self.matfun.solve(self.wrkvec, wrkvec2)
            nnorm = np.divide(wrkvec2.norm(norm_type),
                              self.wrkvec.norm(norm_type))
            _tmp = np.max([_tmp, nnorm],
                          axis=0)

        self.norms[norm_type] = _tmp

    def norm(self, M, norm_type: PETSc.NormType):
        if norm_type not in self.norms:
            self._calculate_norms(norm_type)
        return self.norms[norm_type]


class MatInvKrylov_oper(CustomMatrixContext):
    """Matrix inverse (that is not explicitely evaluated) using GMRES."""

    def __init__(self, comm: MPI.Comm,
                 matrix: PETSc.Mat,
                 pcmat: PETSc.Mat = None,
                 metric: PETSc.Mat = None,
                 tolerance: float = 10 * np.finfo(float).eps,
                 norm_ntests: int = 3,
                 ilu_factor_levels: int = 2,
                 ilu_no_shift: bool = True,
                 preconditioner: str = 'ilu',
                 debug: bool = False):
        """
        Parameters
        ----------
        comm : mpi4py.MPI.Comm
        matrix : petsc4py.PETSc.Mat
            Matrix whose inverse is to be computed
        pcmat : petsc4py.PETSc.Mat
            Preconditioner matrix
        metric : petsc4py.PETSc.Mat
            Metric matrix
        tolerance : float
            absolute tolerance of matrix inverse times a vector (if using
            preconditiner induced norm, otherwise this sets relative tolerance)
        norm_ntests : int
            Number of random sample vectors when computing the norm
        """

        CustomMatrixContext.__init__(self, comm)
        self.mat = matrix
        self.norm_ntests = norm_ntests
        self.ksp = PETSc.KSP().create(comm=comm)

        self.ksp.setOperators(self.mat, pcmat)

        logging.debug("Using GMRES for the inverse of " +
                      self.mat.name.upper())
        set_ksp(self.ksp, pcmat, metric=metric, preconditioner=preconditioner,
                inverse_tolerance=tolerance,
                ilu_factor_levels=ilu_factor_levels, ilu_no_shift=ilu_no_shift,
                debug=debug)
        self.ksp.setUp()

        self.wrkvec = self.createVecRight()

    def getLocalSize(self):
        return self.mat.getLocalSize()

    def getSizes(self):
        return self.mat.getSizes()

    def createVecRight(self):
        return self.mat.createVecRight()

    def mult(self, M, x: PETSc.Vec, y: PETSc.Vec):
        """Multiplies the vector x and stores the result in y"""
        self.ksp.solve(x, y)

    def _calculate_norms(self, norm_type: PETSc.NormType):
        """Lazy evaluation of matrix norms"""
        # Estimate norm

        if norm_type == 4:  # i.e., compute L1 and L2 norms
            _tmp = np.zeros(2)
        else:
            _tmp = 0.0

        for i in range(self.norm_ntests):
            self.wrkvec.setRandom(self.rng)
            wrkvec2 = self.mat.createVecRight()
            self.ksp.solve(self.wrkvec, wrkvec2)
            nnorm = np.divide(wrkvec2.norm(norm_type),
                              self.wrkvec.norm(norm_type))
            _tmp = np.max([_tmp, nnorm],
                          axis=0)

        self.norms[norm_type] = _tmp

    def norm(self, M, norm_type: PETSc.NormType):
        if norm_type not in self.norms:
            self._calculate_norms(norm_type)
        return self.norms[norm_type]


class MatFN_oper(CustomMatrixContext):
    """Matrix functions from SLEPc wrapped as PETSc matrices. Includes an
    iterative solver for matrix inverse"""

    def __init__(self, comm: MPI.Comm,
                 matrix: PETSc.Mat,
                 function_name: str,
                 metricmat: PETSc.Mat = None,
                 scalar: Union[float, complex] = 1.0,
                 tolerance: float = 10 * np.finfo(float).eps,
                 norm_ntests: int = 3):
        """
        Parameters
        ----------
        comm : mpi4py.MPI.Comm
        matrix : petsc4py.PETSc.Mat
        function_name : str
            Either 'exp', 'sqrt', 'invsqrt', or 'log'. Others have not
            been tested.
        metricmat : petsc4py.PETSc.Mat (optional)
            A matrix used for defining the inner product
        scalar : float or complex (optional)
            Scale s of the function, typically implemented as, e.g., exp(s*MAT)
        tolerance : float
            Relative tolerance of the matrix operator-vector product
        norm_ntests : int
            Number of test vectors used when computing the matrix norm
        """

        CustomMatrixContext.__init__(self, comm)
        self.mat = matrix
        self.norm_ntests = norm_ntests

        fn = SLEPc.FN().create(comm=comm)
        fn.setType(function_name)
        if scalar:
            fn.setScale(scalar)
        self.matfun = SLEPc.MFN().create(comm=comm)
        self.matfun.setFN(fn)
        self.matfun.setTolerances(tol=tolerance, max_it=None)
        self.matfun.setOperator(self.mat)
        logging.debug(("Computing matrix function " + function_name.upper() +
                       " of the matrix " + matrix.name))

        if function_name == 'exp':
            self.matfun.setType(SLEPc.MFN.Type.KRYLOV)

        bv = self.matfun.getBV()
        if metricmat:
            logging.debug(
                "    using inner product induced by " +
                metricmat.name)
            bv.setMatrix(metricmat, False)

        bv.setOrthogonalization(type=SLEPc.BV.OrthogType.CGS,
                                refine=SLEPc.BV.OrthogRefineType.IFNEEDED,
                                eta=0.9
                                )

        logging.debug("    with tolerance %g" % tolerance)

        # If we are debugging, enable MFN norm output
        if logging.getLogger('').isEnabledFor(logging.DEBUG):
            PETSc.Options().setValue('mfn_monitor', '')
            self.matfun.setFromOptions()

        self.matfun.setUp()

        self.wrkvec = self.mat.createVecRight()

    def getLocalSize(self):
        return self.mat.getLocalSize()

    def getSizes(self):
        return self.mat.getSizes()

    def createVecRight(self):
        return self.mat.createVecRight()

    def mult(self, M, x: PETSc.Vec, y: PETSc.Vec):
        """Multiplies the vector x and stores the result in y"""

        self.matfun.solve(x, y)

        return y

    def _calculate_norms(self, norm_type: PETSc.NormType):
        """Lazy evaluation of matrix norms"""
        # Estimate norm

        if norm_type == 4:  # i.e., compute L1 and L2 norms
            _tmp = np.zeros(2)
        else:
            _tmp = 0.0

        for i in range(self.norm_ntests):
            self.wrkvec.setRandom(self.rng)
            wrkvec2 = self.mat.createVecRight()
            self.matfun.solve(self.wrkvec, wrkvec2)
            nnorm = np.divide(wrkvec2.norm(norm_type),
                              self.wrkvec.norm(norm_type))
            _tmp = np.max([_tmp, nnorm],
                          axis=0)

        self.norms[norm_type] = _tmp

    def norm(self, M, norm_type: PETSc.NormType):
        if norm_type not in self.norms:
            self._calculate_norms(norm_type)
        return self.norms[norm_type]
