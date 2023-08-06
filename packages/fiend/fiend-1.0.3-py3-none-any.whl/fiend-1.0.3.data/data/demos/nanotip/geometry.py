"""
This file includes functions for defining the nanotip geometry and how to mesh
it.
"""
import numpy as np
from scipy.optimize import minimize

import dolfin as df
import mshr

from fiend.utils.mesh import mesh_domain

class PotentialWellTimesRho(df.UserExpression):

    """
    Definition of the static potential (well)
    """

    def __init__(self, parent, potential_drop, **kwargs):
        self.parent = parent
        self.potential_drop = potential_drop
        super().__init__(kwargs)

    def eval(self, value, x):
        if self.parent._is_inside_tip(x[0], x[1]):
            value[0] =  -self.potential_drop*x[0]
        else:
            value[0] = 0.0
    
    def value_shape(self):
        return []

class Nanotip:

    """
    A class for some handy tools working with nanotip geometry
    """


    def __init__(self, apex_radius,
                       full_opening_angle ):
        self._radius = apex_radius
        self._alpha = full_opening_angle/180. * np.pi
        self._a = self._radius / np.tan(self._alpha/2)
        self._b = self._a / np.tan(self._alpha/2)
    

    def _tip_surface(self, v):
        """
        Returns tip surface curve in cylindrical coordinates

        Parameters
        ----------
        v : float in range [0, infinity[
            The curve parametrization

        Returns
        -------
        rho : float
        z : float
        """

        rho = self._a*np.sinh(v)
        z = self._b*( np.cosh(v) - 1 )
        return rho, z

    def _distance_to_tip(self, rho, z):
        """
        Computes the euclidian distance of the point to the tip surface.

        Parameters
        ----------
        rho : float
            rho-coordinate 
        z : float
            z-coordinate

        Returns
        -------
        distance : float
        """
        def dist2(v):
            v_rho, v_z = self._tip_surface(np.fabs(v))
            return np.sqrt( (rho-v_rho)**2 + (z-v_z)**2 )

        if z > 0:
            v0 = np.mean([ np.arcsinh(rho/self._a), np.arccosh(z/self._b + 1) ])
        else:
            v0 = 0
        res = minimize(dist2, x0 = v0, method='cobyla')

        return res.fun

    def _is_inside_tip(self, rho, z):
        """
        Returns true if point is inside the nanotip, false otherwise.

        Parameters
        ----------
        rho : float
            rho-coordinate
        z : float
            z-coordinate
        """
        v_tip = np.arcsinh(rho/self._a)
        z_tip = self._b * ( np.cosh(v_tip) - 1)
        return z > z_tip

    def _refinement_function(self, rho, z, cr, refined_mesh_distance,
                             transition_distance, cell_minrad, cell_maxrad,
                             box_topz):
        """
        Defines whether the mesh element should be refined further

        Parameters
        ----------
        rho : float
            rho-coordinate the mesh element incenter
        z : float
            z-coordinate of the mesh element incenter
        cr : circumradius of the mesh element

        Returns
        -------
        bool : true if should be refined further, false if not
        """
            
        r = np.array([self._distance_to_tip(rho, z),
                      np.fabs(box_topz-z), np.fabs(z+box_topz), np.fabs(rho)]).min()
        if r < refined_mesh_distance:
            return cr > cell_minrad
        elif r < (refined_mesh_distance+transition_distance):
            return cr >((r-refined_mesh_distance)/transition_distance*\
                    (cell_maxrad-cell_minrad)+cell_minrad)
        else:
            return cr >cell_maxrad



    def get_mesh(self, boxsize, refined_mesh_distance,
                 transition_distance, cell_minrad, cell_maxrad,
                 vacuum_length=None):
        rho_width = boxsize[0]
        z_length = boxsize[1]/2
        if vacuum_length:
             domain = mshr.Rectangle( df.Point(0.0, -vacuum_length),
                                 df.Point(rho_width, z_length) )
        else:
            domain = mshr.Rectangle( df.Point(0.0, -z_length),
                                 df.Point(rho_width, z_length) )
        
        refinement = lambda rho, z, cr: self._refinement_function(rho, z, cr,
                                                                  refined_mesh_distance,
                                                                  transition_distance,
                                                                  cell_minrad,
                                                                  cell_maxrad,
                                                                  boxsize[1]/2)
        return mesh_domain(domain, refinement)


    def get_potential_times_rho(self, potential_drop):
        """Returns ρ V(ρ, z) as ufl expression"""
        return PotentialWellTimesRho(self, potential_drop, degree=1,
                                     cell=df.triangle)

