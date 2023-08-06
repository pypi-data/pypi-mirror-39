"""
Tests for custom matrix classes
"""
import unittest
import numpy as np
from petsc4py import PETSc
from fiend.utils.custom_matrices import *


class TestCustomMatrices(unittest.TestCase):

    def setUp(self):
        """
        Initializes three 3x3 matrices S, A, and B and two vectors v and v2.
        S = [ [1,  2, 3],
              [-3, 2, 1],
              [1,  0, 2] ]

        A = [ [0.5,  2.0, 3.7],
              [-3.9, 0.0, 1.0],
              [1.0,  0.0, 2.0] ]

        B = [ [0.5,  2.0,  3.7 ],
              [-3.9, 1./7, 1.0 ],
              [1.0,  0.0,  2./3] ]

        v  = [ -1, 0.2, 1 ]
        v2 = [ -1, 0.3, 1 ]
        """
        # Initialize S
        S = PETSc.Mat()
        S.create(PETSc.COMM_WORLD)
        S.setType('aij')
        S.setSizes([3, 3])
        S.setUp()
        S.setValue(0, 0, 1.0)
        S.setValue(0, 1, 2.0)
        S.setValue(0, 2, 3.0)
        S.setValue(1, 0, -3.0)
        S.setValue(1, 1, 2.0)
        S.setValue(1, 2, 1.0)
        S.setValue(2, 0, 1.0)
        S.setValue(2, 1, 0.0)
        S.setValue(2, 2, 2.0)
        S.assemble()

        self.S = S

        # Initialize A
        A = PETSc.Mat()
        A.create(PETSc.COMM_WORLD)
        A.setType('aij')
        A.setSizes([3, 3])
        A.setUp()
        A.setValue(0, 0, 0.5)
        A.setValue(0, 1, 2.0)
        A.setValue(0, 2, 3.7)
        A.setValue(1, 0, -3.9)
        A.setValue(1, 1, 0.0)
        A.setValue(1, 2, 1.0)
        A.setValue(2, 0, 1.0)
        A.setValue(2, 1, 0.0)
        A.setValue(2, 2, 2.0)
        A.assemble()

        self.A = A

        # Initialize B
        B = PETSc.Mat()
        B.create(PETSc.COMM_WORLD)
        B.setType('aij')
        B.setSizes([3, 3])
        B.setUp()
        B.setValue(0, 0, 0.5)
        B.setValue(0, 1, 2.0)
        B.setValue(0, 2, 3.7)
        B.setValue(1, 0, -3.9)
        B.setValue(1, 1, 1.0 / 7)
        B.setValue(1, 2, 1.0)
        B.setValue(2, 0, 1.0)
        B.setValue(2, 1, 0.0)
        B.setValue(2, 2, 2.0 / 3)
        B.assemble()
        self.B = B

        # Initialize v
        v = PETSc.Vec().create(PETSc.COMM_WORLD)
        v.setType('mpi')
        v.setSizes(3)
        v.setUp()
        v.setValues([0, 1, 2], [-1, 0.2, 1])
        v.assemble()
        self.v = v

        # Initialize v2
        v = PETSc.Vec().create(PETSc.COMM_WORLD)
        v.setType('mpi')
        v.setSizes(3)
        v.setUp()
        v.setValues([0, 1, 2], [-1, 0.3, 1])
        v.assemble()
        self.v2 = v

    def test_matvec(self):
        """Test PETSc mat-vec product"""
        res = self.S * self.v

        np.testing.assert_allclose(res.getValues(range(3)), [2.4, 4.4, 1])

    def test_exp(self):
        """Test matrix exponential"""
        Sexp = MatFN_oper(PETSc.COMM_WORLD, self.S, 'exp').getPETScMat()

        res = Sexp * self.v

        np.testing.assert_allclose(res.getValues(range(3)),
                                   [15.381014977347077567,
                                    -8.6897038032975282481,
                                    13.636961218257825004])

    def test_sqrt(self):
        """Test matrix sqrt"""
        Ssqrt = MatFN_oper(PETSc.COMM_WORLD, self.S, 'sqrt').getPETScMat()

        res = Ssqrt * self.v

        np.testing.assert_allclose(res.getValues(range(3)),
                                   [-0.067306986856594604425,
                                    2.1667001462418235191,
                                    0.92807972824722351022])

    def test_invsqrt(self):
        """Test matrix invsqrt"""
        Sinvsqrt = MatFN_oper(PETSc.COMM_WORLD, self.S,
                              'invsqrt').getPETScMat()

        res = Sinvsqrt * self.v

        np.testing.assert_allclose(res.getValues(range(3)),
                                   [-1.05402895378188054459,
                                    -0.99322052805918507103,
                                    0.99105434101455202741])

    def test_matsum(self):
        """Test matrix sum"""

        S_p_2A = MatSum_oper(PETSc.COMM_WORLD, self.S, self.A,
                             2.0).getPETScMat()

        res = S_p_2A * self.v

        np.testing.assert_allclose(res.getValues(range(3)),
                                   [9.6, 14.2, 3])

    def test_matsum2(self):
        """Test matrix sum with matexp for the 2nd mat"""
        expA = MatFN_oper(PETSc.COMM_WORLD, self.A, 'exp').getPETScMat()
        S_p_2expA = MatSum_oper(PETSc.COMM_WORLD, self.S, expA,
                                2.0).getPETScMat()

        res = S_p_2expA * self.v

        np.testing.assert_allclose(res.getValues(range(3)),
                                   [29.014734647082374991,
                                    -16.662660400661411371,
                                    27.807554117419606798])

    def test_matmult(self):
        """Test matrix product"""
        SA = MatMult_oper(PETSc.COMM_WORLD, self.S, self.A).getPETScMat()

        res = SA * self.v

        np.testing.assert_allclose(res.getValues(range(3)),
                                   [16.400000000000000000, 0,
                                    5.6000000000000000000])

    def test_combination(self):
        """Test combination S^-1/2 (A+r*B) S^-1/2"""
        Sinvsqrt = MatFN_oper(PETSc.COMM_WORLD, self.S,
                              'invsqrt').getPETScMat()
        A_rB_oper = MatSum_oper(PETSc.COMM_WORLD, self.A, self.B, 1.0)
        A_rB = A_rB_oper.getPETScMat()

        P1 = MatMult_oper(PETSc.COMM_WORLD, Sinvsqrt, A_rB).getPETScMat()
        TOTAL = MatMult_oper(PETSc.COMM_WORLD, P1, Sinvsqrt).getPETScMat()

        res = TOTAL * self.v

        np.testing.assert_allclose(res.getValues(range(3)),
                                   [-1.6459689727581641371,
                                    4.3694421111106155991,
                                    1.15259205739882429709])

        # Change the value of r in the sum, check that it propagates through
        # the reference chain
        A_rB_oper.set_scalar(2.5)

        res = TOTAL * self.v

        np.testing.assert_allclose(res.getValues(range(3)),
                                   [-2.5128974257726763837,
                                    8.1712208061866906985,
                                    1.19109968387179219502])

    def test_matinvdirect(self):
        """Test matrix inverse using a direct solver"""
        Sinv = MatInvDirect_oper(PETSc.COMM_WORLD, self.S,
                                 lusolver='superlu').getPETScMat()

        res = Sinv * self.v

        np.testing.assert_allclose(res.getValues(range(3)),
                                   [-11 / 15., -43 / 30., 13 / 15.])

        self.assertLessEqual(Sinv.norm(PETSc.NormType.NORM_2), 4.426964295)

    def test_matinvkrylov(self):
        """Test matrix inverse using a direct solver"""
        Sinv = MatInvKrylov_oper(
            PETSc.COMM_WORLD, self.S, self.S).getPETScMat()

        res = Sinv * self.v

        np.testing.assert_allclose(res.getValues(range(3)),
                                   [-11 / 15., -43 / 30., 13 / 15.])

        self.assertLessEqual(Sinv.norm(PETSc.NormType.NORM_2), 4.426964295)
