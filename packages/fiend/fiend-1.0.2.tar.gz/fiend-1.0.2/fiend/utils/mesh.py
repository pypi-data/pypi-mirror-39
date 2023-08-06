"""
Meshing tools
"""

import logging
import os
from typing import Callable, Text
import pathlib

import numpy as np
import scipy.optimize
import scipy.misc
from mpi4py import MPI
import progressbar

import dolfin as df
from mshr import Circle, Rectangle, generate_mesh

from fiend.utils.misc import triangle_incenter


def mesh_domain(domain,
                refinement_function: Callable[[float, float, float], bool]) -> df.Mesh:
    """
    Returns a mesh of a domain in (ρ,z)-coordinates.

    Parameters
    ----------
    domain : mshr domain
    refinement_function : callable(ρ_incenter, z_incenter, cellradius)
        Function that returns true if the cell should be refined, false
        otherwise

    Returns
    -------
    mesh : dolfin.Mesh
    """
    logging.debug("Beginning mesh generation")
    comm = df.MPI.comm_world

    # Create initial mesh on all processes
    mesh = generate_mesh(domain, 2)

    # Refine cells until no more refinement needed
    # Each MPI process refines its local cells
    # Redistribution of the mesh is done afterwards
    while True:

        cell_markers = df.MeshFunction("bool", mesh, mesh.topology().dim())
        cell_markers.set_all(False)
        # Find cells that need to be refined
        for cell in df.cells(mesh):
            r = cell.distance(df.Point(0.0, 0.0))
            vrtx_coordinates = cell.get_vertex_coordinates()
            rho_c, z_c = triangle_incenter(
                np.array(vrtx_coordinates).reshape(3, 2))

            cellradius = cell.circumradius()
            if refinement_function(rho_c, z_c, cellradius):
                cell_markers[cell] = True

        num_local_cells_to_refine = np.sum(cell_markers.array())
        num_cells_to_refine = comm.allreduce(sendobj=num_local_cells_to_refine,
                                             op=MPI.SUM)
        logging.debug(" cells to refine: %d" % num_cells_to_refine)

        # Refine the grid if needed, otherwise continue
        if num_cells_to_refine > 0:
            mesh = df.refine(mesh, cell_markers, False)
        else:
            break

    logging.debug("..finished mesh refinement.")

    # Redistribute mesh across processes
    cell_markers = df.MeshFunction("bool", mesh, mesh.topology().dim())
    cell_markers.set_all(False)

    mesh = df.refine(mesh, cell_markers, True)
    numcells = comm.allreduce(sendobj=mesh.num_cells(), op=MPI.SUM)

    logging.debug("Final mesh has %d cells." % numcells)

    return mesh


def mesh_of_sphere_in_cylindrical_coordinates(radius: float,
                                              core_radius: float,
                                              refinement_radius: float,
                                              cellradius: float,
                                              core_cellradius: float) -> df.Mesh:
    """
    Returns a mesh of a sphere in (ρ,z)-coordinates, i.e., a half-circle
    in (ρ,z)-plane. Mesh is generated so that it's more dense near the origin
    and less so far away.

    Parameters
    ----------
    radius : float
        Radius of the sphere we're meshing
    core_radius : float
        Radius of dense mesh around the origin
    refinement_radius : float
        Radius where mesh refinement stops
    cellradius : float
        Maximum circumradius of a triangular mesh element
    core_cellradius : float
        Maximum circumradius of a mesh element inside `core_radius`

    Returns
    -------
    mesh : dolfin.Mesh
    """

    comm = df.MPI.comm_world

    # Define the half-circle domain
    domain = Circle(df.Point(0.0, 0.0), radius) \
        - Rectangle(df.Point(-radius, -radius),
                    df.Point(0, radius))

    # Construct a function for checking if a mesh element needs refinement
    A = core_cellradius / cellradius
    a = core_radius
    b = refinement_radius

    def meshscale(r: float) -> float:
        if r == 0:
            return A
        return 1 - (1 - A) * a / r * np.tanh(r / a) * np.exp(-(r / b)**2)

    def refinement_function(rho: float, z: float, h: float) -> bool:
        r = np.hypot(rho, z)
        return h > meshscale(r) * cellradius

    return mesh_domain(domain, refinement_function)


def remesh_function(Vfunspace: df.FunctionSpace,
                    old_solution: df.Function) -> df.Function:
    """Interpolates a function to new functionspace"""
    psi = df.Function(Vfunspace)
    df.LagrangeInterpolator.interpolate(psi, old_solution)
    return psi


def load_mesh(comm: MPI.Comm,
              filepath: Text) -> df.Mesh:
    """Loads a dolfin mesh"""
    with df.HDF5File(comm, filepath, 'r') as meshfile:
        mesh = df.Mesh(comm)
        meshfile.read(mesh, 'mesh', False)
    return mesh


def save_mesh(filepath: Text,
              mesh: df.Mesh) -> None:
    """Saves a dolfin mesh"""
    path = pathlib.PurePath(filepath)
    os.makedirs(path.parent, exist_ok=True)
    with df.HDF5File(mesh.mpi_comm(), filepath, 'w') as meshfile:
        meshfile.write(mesh, 'mesh')


def curve_mesh(path_function: Callable, num_elements: int) -> df.Mesh:
    """
    Creates a 1D mesh embedded in the 2D domain. The mesh discretizes
    the path inputted to the function with 'num_elements' cells. The mesh is
    created on a single MPI process, not a shared mesh."""
    tdim, gdim = 1, 2

    mesh = df.Mesh(MPI.COMM_SELF)
    editor = df.MeshEditor()
    editor.open(mesh, 'interval', 1, 2)
    editor.init_vertices(num_elements + 1)
    editor.init_cells(num_elements)

    mesh_points = path_function(np.linspace(0, 1, num_elements + 1))

    for vi, v in enumerate(mesh_points):
        editor.add_vertex(vi, v)

    for ci in range(num_elements):
        editor.add_cell(ci, np.array([ci, ci + 1], dtype='uintp'))

    editor.close()
    return mesh


def extract_equiradial_shell(mesh: df.Mesh,
                             radius: float) -> df.Mesh:
    """Returns a new mesh consisting only of the cells of the original mesh
    which are on the surface of circle of radius 'radius'"""

    comm = mesh.mpi_comm()
    assert comm.size == 1, "extract_equiradial_shell works only on non-parallel meshes"

    is_master = MPI.COMM_WORLD.rank == 0

    def signed_distance_to_circle(p):
        return radius - np.sqrt(np.dot(p, p))

    def on_surface(cell):
        vtxs = np.array(cell.get_vertex_coordinates()).reshape(3, 2)
        distances = [signed_distance_to_circle(v) for v in vtxs]
        sgns = np.sign(distances)
        all_outside = np.all(sgns == 1)
        all_inside = np.all(sgns == -1)
        return not all_outside and not all_inside

    logging.info("Finding cells on the surface")
    if logging.getLogger('').isEnabledFor(logging.INFO) and is_master:
        iterable = progressbar.progressbar(df.cells(mesh),
                                           max_value=mesh.num_cells())
    else:
        iterable = df.cells(mesh)

    surface_cells = [
        cell for cell in iterable
        if on_surface(cell)]

    logging.info("Constructing smaller mesh")
    surface_cell_vertices = np.zeros((2, 3 * len(surface_cells)))
    for i, cell in enumerate(surface_cells):
        vtxs = np.array(cell.get_vertex_coordinates()).reshape(3, 2)
        surface_cell_vertices[:, 3 * i] = vtxs[0]
        surface_cell_vertices[:, 3 * i + 1] = vtxs[1]
        surface_cell_vertices[:, 3 * i + 2] = vtxs[2]

    surface_cell_vertices, indices = np.unique(surface_cell_vertices,
                                               return_inverse=True,
                                               axis=1)

    smesh = df.Mesh()
    editor = df.MeshEditor()
    editor.open(smesh, 'triangle', 2, 2)
    editor.init_cells(len(surface_cells))
    editor.init_vertices(surface_cell_vertices.shape[1])

    for vi in range(surface_cell_vertices.shape[1]):
        editor.add_vertex(vi,
                          surface_cell_vertices[:, vi])

    for ci in range(len(surface_cells)):
        v0 = indices[3 * ci]
        v1 = indices[3 * ci + 1]
        v2 = indices[3 * ci + 2]
        editor.add_cell(ci, [v0, v1, v2])

    editor.close()
    return smesh


def extract_shell(mesh: df.Mesh,
                  path: Callable) -> df.Mesh:
    """Returns a new mesh consisting only of the cells of the original mesh
    which are crossed by the provided path.

    Parameters
    ----------
    path : df.Mesh
        Original mesh
    path : callable with signature float -> (float, float)
        Should parametrize the path with argument ranging from 0 to 1. Path
        should be oriented clockwise around (rho, z) = (0,0)/tests/test_mesh
    """

    comm = mesh.mpi_comm()
    assert comm.size == 1, "extract_shell works only on non-parallel meshes"
    is_master = MPI.COMM_WORLD.rank == 0

    def closest_point_on_path(p):

        def distance(s):
            p_on_path = path(s)
            return np.linalg.norm(p - p_on_path)

        res = scipy.optimize.minimize_scalar(distance,
                                             bounds=(0, 1),
                                             method='bounded')
        return res.x, path(res.x)

    def signed_distance_to_path(p):
        # Project to path norml on the closest point to get 'signed distance'
        s, p_on_path = closest_point_on_path(p)
        tangent = scipy.misc.derivative(path, x0=s, dx=1e-5)
        normal = np.array([-tangent[1], tangent[0]])
        normal /= np.linalg.norm(normal)
        return np.dot(p - p_on_path, normal)

    def on_surface(cell):
        vtxs = np.array(cell.get_vertex_coordinates()).reshape(3, 2)
        distances = [signed_distance_to_path(v) for v in vtxs]
        sgns = np.sign(distances)
        all_outside = np.all(sgns == 1)
        all_inside = np.all(sgns == -1)
        return not all_outside and not all_inside

    logging.info("Finding cells on the curve")
    if True:  # logging.getLogger('').isEnabledFor(logging.INFO) and is_master:
        iterable = progressbar.progressbar(df.cells(mesh),
                                           max_value=mesh.num_cells())
    else:
        iterable = df.cells(mesh)

    surface_cells = [
        cell for cell in iterable
        if on_surface(cell)]

    logging.info("Constructing smaller mesh")
    surface_cell_vertices = np.zeros((2, 3 * len(surface_cells)))
    for i, cell in enumerate(surface_cells):
        vtxs = np.array(cell.get_vertex_coordinates()).reshape(3, 2)
        surface_cell_vertices[:, 3 * i] = vtxs[0]
        surface_cell_vertices[:, 3 * i + 1] = vtxs[1]
        surface_cell_vertices[:, 3 * i + 2] = vtxs[2]

    surface_cell_vertices, indices = np.unique(surface_cell_vertices,
                                               return_inverse=True,
                                               axis=1)

    smesh = df.Mesh()
    editor = df.MeshEditor()
    editor.open(smesh, 'triangle', 2, 2)
    editor.init_cells(len(surface_cells))
    editor.init_vertices(surface_cell_vertices.shape[1])

    for vi in range(surface_cell_vertices.shape[1]):
        editor.add_vertex(vi,
                          surface_cell_vertices[:, vi])

    for ci in range(len(surface_cells)):
        v0 = indices[3 * ci]
        v1 = indices[3 * ci + 1]
        v2 = indices[3 * ci + 2]
        editor.add_cell(ci, [v0, v1, v2])

    editor.close()
    return smesh
