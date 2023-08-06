"""
Implementations of absorbing boundaries:
    Complex Absorbing Potential
"""

import numpy as np
import dolfin as df
import ufl  # Dolfin doesn't expose 'abs' at least in 2018.1.0
import scipy.optimize
from typing import Callable

def get_cap(radius: float,
            cap_width: float,
            cap_height: float,
            mesh: df.Mesh):

    x = df.SpatialCoordinate(mesh)
    rho = x[0]
    z = x[1]

    r = df.sqrt(rho * rho + z * z)

    return df.conditional(df.ge(r, radius), cap_height,
                          df.conditional(df.le(ufl.algebra.Abs(r - radius), cap_width),
                                         cap_height * df.cos(np.pi / (2 * cap_width) *
                                                             ufl.algebra.Abs(r - radius))**2,
                                         0))

def get_cap_from_signed_distance(sdistance : Callable,
                              cap_width : float,
                              cap_height : float):
     class Dist(df.UserExpression):
        
        def eval(self, values, x):
            values[0] = sdistance(x)

        def value_shape(self):
            return ()

     d = Dist()

     return df.conditional(df.ge(d, 0), 
                              cap_height,
                              df.conditional( df.ge(d,-cap_width),
                                  cap_height * df.cos(-np.pi/(2*cap_width)*d)**2,
                                  0)
                          )   
