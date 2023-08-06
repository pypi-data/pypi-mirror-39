"""
Setup of matrices and vectors for time propagation.
"""

import logging
import numpy as np
from collections import OrderedDict

from mpi4py import MPI
from petsc4py import PETSc

import dolfin as df

from fiend.utils.mesh import mesh_of_sphere_in_cylindrical_coordinates,\
    remesh_function
from fiend.utils.dolfin import wfnorm, normalize, dirichlet_boundary
from fiend.utils.misc import set_logging, parse_functionspace_argument, \
    fiend_setup
from fiend.utils.predefined_potentials import atom_potential_times_rho_expr
from fiend.utils.petsc_utils import petsc_save, petsc_convert_to_complex
from fiend.tdse.tdse import tdse_setup, save_tdse_preparation
from fiend.tise.tise import load_tise_states


def prepare_tdse_main():
    """
    A standalone function for preparing matrices used for propagating time
    dependent Schrödinger equation. Reads parameters from command line, data
    from a previous solution of time independent Schrödinger equation, and
    prepares the matrices accordinly.
    """

    master, rank, comm = fiend_setup()

    import argparse
    import configparser

    # Read data from presolved time-independent Schrödinger equation
    config = configparser.ConfigParser()
    try:
        config.read("data/config")
        tise_config = config['TISE parameters']
    except BaseException:
        raise RuntimeError("No config data from a TISE simulation.")

    # Add command line interface
    parser = argparse.ArgumentParser(
        description="Sets up of matrices and vectors for time propagation.",
        argument_default=argparse.SUPPRESS,
        epilog=("Please note that you should solve the time-independent "
                "Schrödinger equation before using this command. "
                "See, e.g., the script solve_tise.")
    )

    parser.add_argument("--radius", "-R", type=float,
                        default=tise_config.getfloat('radius'),
                        help=("Radius of the simulated domain. Dirichlet "
                              "boundary conditions will be set at this "
                              "distance from the origin.")
                        )
    parser.add_argument("--core_radius", type=float,
                        default=tise_config.getfloat('core_radius'),
                        help=("What region is to be considered as the 'atomic "
                              "core', i.e., where the mesh is denser.")
                        )
    parser.add_argument("--refinement_radius", type=float,
                        default=tise_config.getfloat("refinement_radius"),
                        help=("Up to which distance from the origin should "
                              "we refine the mesh")
                        )
    parser.add_argument("--cellradius", type=float,
                        default=tise_config.getfloat("cellradius"),
                        help=("Maximum radius of a circle enclosing a mesh "
                              "element far away from the origin")
                        )
    parser.add_argument("--core_cellradius", type=float,
                        default=tise_config.getfloat("core_cellradius"),
                        help=("Maximum radius of a circle enclosing "
                              "a mesh element near the origin.")
                        )
    parser.add_argument('--cap_width', type=float, default=0,
                        help=("Width of the imaginary absorbing potential.")
                        )
    parser.add_argument('--cap_height', type=float, default=0,
                        help=("Height of the imaginary absorbing potential.")
                        )
    parser.add_argument("--functionspace", type=str,
                        default=tise_config.get("functionspace"),
                        help=("Functionspace to use for TDSE. Should be "
                              "a pair separated by a comma. The first "
                              "argument sets the basis function type "
                              "and the second the maximum degree of the "
                              "basis functions.")
                        )
    parser.add_argument("--debug", action='store_true', default=False,
                        help="Debug information from all MPI processes")
    parser.add_argument("--debug_master", action='store_true', default=False,
                        help="Debug information from the rank 0 MPI process")

    parser.add_argument("--quadrature_degree", type=int)
    args = vars(parser.parse_args())
    if 'quadrature_degree' in args:
        df.parameters['form_compiler']['quadrature_degree'] = args['quadrature_degree']

    # Append parameters from TISE simulation
    args['atom_type'] = tise_config['atom_type']

    set_logging(master, rank, args['debug'], args['debug_master'])

    # Load TISE mesh and state
    logging.info("Reading TISE mesh...")

    tise_funspace = parse_functionspace_argument(tise_config['functionspace'])
    tdse_funspace = parse_functionspace_argument(args['functionspace'])

    num_states = tise_config.getint('num_states')
    tise_mesh, Vtise, _, tise_states = load_tise_states(comm, num_states,
                                                        tise_funspace)

    # Check if TISE and TDSE meshes are the same. Skip remeshing if they are.

    tise_and_tdse_same_meshes = np.isclose(args['radius'],
                                           tise_config.getfloat('radius')) \
        and np.isclose(args['core_radius'],
                       tise_config.getfloat('core_radius')) \
        and np.isclose(args['refinement_radius'],
                       tise_config.getfloat('refinement_radius')) \
        and np.isclose(args['cellradius'],
                       tise_config.getfloat('cellradius')) \
        and np.isclose(args['core_cellradius'],
                       tise_config.getfloat('core_cellradius'))
    tise_and_tdse_same_functionspace = tdse_funspace == tise_funspace

    if tise_and_tdse_same_meshes and tise_and_tdse_same_functionspace:
        logging.info("TISE and TDSE have the same mesh and basis functions.")
        mesh = tise_mesh
        V = Vtise
        states = tise_states
    else:
        logging.info(("TISE and TDSE have different meshes or functionspaces, "
                      "interpolating states to the new functionspace"))
        # Compute TDSE mesh
        if tise_and_tdse_same_meshes:
            mesh = tise_mesh
        else:
            mesh = mesh_of_sphere_in_cylindrical_coordinates(
                radius=args['radius'],
                core_radius=args['core_radius'],
                refinement_radius=args['refinement_radius'],
                cellradius=args['cellradius'],
                core_cellradius=args['core_cellradius']
            )
        # Interpolate our TISE solution to the new functionspace

        V = df.FunctionSpace(mesh, tdse_funspace[0], tdse_funspace[1])
        states = np.empty(num_states, dtype=df.Function)
        for i in range(num_states):
            states[i] = remesh_function(V, tise_states[i])
            normalize(states[i])

    # Obtain matrices for TDSE
    S, S0, S1, H0, partialRho, partialZ, Rho, Z, CAP, ACC = tdse_setup(mesh,
                                                                       atom_potential_times_rho_expr(
                                                                           args['atom_type'], mesh),
                                                                       args['cap_height'], args['cap_width'],
                                                                       tdse_funspace)

    logging.info("Saving files...")
    # Save matrices and wavefunctions to file
    save_tdse_preparation(comm, mesh, states, H0, S, S0, S1, partialRho, partialZ, Rho, Z,
                          CAP, ACC)

    # Save simulation parameters
    try:
        config.add_section('TDSE parameters')
    except BaseException:
        pass

    for key, val in sorted(args.items()):
        config.set('TDSE parameters', key, str(val))

    if master:
        with open("data/config", "w") as f:
            config.write(f)

    comm.Barrier()
    logging.debug("Exiting...")


if __name__ == '__main__':
    prepare_tdse_main()
