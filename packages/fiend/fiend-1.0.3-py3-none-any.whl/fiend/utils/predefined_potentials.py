"""
Definitions of stationary potentials (atomic potentials)
"""
import dolfin as df
import ufl


def _hydrogen_potential_times_rho(rho, z, r):
    """ -ρ/r """
    return df.conditional(df.gt(rho, 0), -rho / r, 0.0)


def _lithium_potential_times_rho(rho, z, r):
    """ -ρ/r * [Zt + (Z-Zt)*exp(-a1*r) + a2*r*exp(-a3*r) ] """
    Zt = 1
    Z = 3
    a1 = 3.395
    a2 = 3.212
    a3 = 3.207
    pot_x_rho = - rho / r * \
        (Zt + (Z - Zt) * df.exp(-a1 * r) + a2 * r * df.exp(-a3 * r))
    return df.conditional(df.gt(rho, 0), pot_x_rho, 0.0)

# Global list of all implemented atomic potential types
_atom_types = {'h': _hydrogen_potential_times_rho,
               'li': _lithium_potential_times_rho}


def atom_potential_times_rho_expr(atom_type: str, mesh: df.Mesh):
    """
    Returns an UFL Form for ρV(ρ, z)

    Parameters
    ----------
    atom_type : str
        The atomic species
    mesh : df.Mesh
        Mesh of the domain
    Returns
    -------
    UFL Expression
    """
    x = df.SpatialCoordinate(mesh)
    rho = x[0]
    z = x[1]
    r = df.sqrt(rho * rho + z * z)

    try:
        return _atom_types[atom_type.lower()](rho, z, r)
    except Exception as e:
        raise ValueError(
            "Atomic type not understood/implemented: " + atom_type)
