Overview
========

FIEND is a software package for simulating time-dependent single-particle quantum
mechanics in cylindrically symmetric systems. This includes systems such as atoms and linear
molecules in linearly polarized laser field, metal nanotapers, and
nanoclusters.

FIEND employs the `FEniCS`_ FEM-suite for meshing and assembling the system
matrices, and `PETSc`_ and `SLEPc`_ for high-performance linear algebra.

.. _FEniCS: https://www.fenicsproject.org
.. _PETSc: https://bitbucket.org/petsc/petsc
.. _SLEPc: https://bitbucket.org/slepc/slepc

Package structure
-----------------

The package structure is as follows::

    .
    ├── docker
    │      Files for building Docker containers 
    │      for easy installation of Fiend
    │    
    ├── fiend
    │   ├── analysis
    │   │   │  Analysis scripts
    │   │   │
    │   │   ├── animate_density.py
    │   │   │     Animation of electron density in time
    │   │   ├── custom.mplparams
    │   │   ├── draw_acceleration.py
    │   │   │     Visualization of dipole acceleration
    │   │   ├── draw_dipole.py
    │   │   │     Visualization of dipole moment
    │   │   ├── draw_final_state.py
    │   │   │     Visualization of the final state of the propagation
    │   │   ├── draw_laser.py
    │   │   │     Visualization of the laser electric field
    │   │   ├── draw_mesh.py
    │   │   │     Visualization of meshes
    │   │   ├── draw_norm.py
    │   │   │     Visualization of wavefunction norm in time
    │   │   ├── draw_pes.py
    │   │   │     Computation of photoelectron spectrum (experimental)
    │   │   ├── draw_snapshot.py
    │   │   │     Visualization of electron density at single instant of time
    │   │   ├── draw_stationary_states.py
    │   │   │     Visualization of stationary states
    │   │   ├── draw_velocity.py
    │   │   │     Visualization of dipole velocity
    │   │   ├── __init__.py
    │   │   ├── _pes_tsurff.py
    │   │   │     Implementation of tsurff
    │   │   ├── tests
    │   │   │     Tests of the analysis scripts
    │   │   │   
    │   │   ├── _unit_conversions.py
    │   │   │     Unit conversion tools
    │   │   └── _visualization_utils.py
    │   │         Visualization tools
    │   ├── __init__.py
    │   ├── lin_pol
    │   │   │  Tools for propagation with linearly polarized pulses 
    │   │   │
    │   │   ├── __init__.py
    │   │   ├── prepare_tdse.py
    │   │   ├── propagate.py
    │   │   └── solve_tise.py
    │   ├── propagation
    │   │   │  Implementation of propagation-related stuff 
    │   │   │
    │   │   ├── __init__.py
    │   │   ├── observables.py
    │   │   │     Implementation of all observables
    │   │   ├── propagation_utils.py
    │   │   │     Helpful tools for loading system matrices
    │   │   ├── propagators.py
    │   │   │     All propagators are implemented here
    │   │   └── tests
    │   │         Tests for the propagators
    │   │
    │   ├── pulseconfig_parser
    │   │   │  Parser for laser pulse configuration files
    │   │   │
    │   │   ├── __init__.py
    │   │   ├── laser.py
    │   │   │     Implementation of Laser
    │   │   ├── parameter.py
    │   │   │     Implementation of const/non-const parameter
    │   │   ├── parser.py
    │   │   │     Implementation of Laser configurtion parser
    │   │   └── singlecolorlaserpulse.py
    │   │         Implementation of a single channel laser pulse
    │   │
    │   ├── tdse
    │   │   │  Tools for preparing the system matrices etc. for propagation
    │   │   │
    │   │   ├── absorbing_boundaries.py
    │   │   │     Complex absorbing boundary
    │   │   ├── __init__.py
    │   │   ├── tdse.py
    │   │   │     Preparation of system matrices for propagation
    │   │   │     and related IO tools
    │   │   └── tests
    │   │         Tests related to preparation of 
    │   │         system matrices
    │   │
    │   ├── tests
    │   │     Global tests (mypy)
    │   │   
    │   ├── tise
    │   │   ├── __init__.py
    │   │   ├── tests
    │   │   │     Tests for TISE solver
    │   │   │   
    │   │   └── tise.py
    │   │         TISE solver and related IO tools
    │   └── utils
    │       │  Helper tools that are used all over the code
    │       │
    │       ├── custom_matrices.py
    │       ├── dolfin.py
    │       ├── __init__.py
    │       ├── mesh.py
    │       ├── misc.py
    │       ├── mpi.py
    │       ├── petsc_utils.py
    │       ├── predefined_potentials.py
    │       └── tests
    │             Tests for the utilities
    │ 
    ├── license.txt
    ├── README.md
    │      Readme for Gitlab
    ├── README.rst
    │      Readme for PYPI
    ├── requirements.txt
    │      Dependencies of Fiend
    └── setup.py
           Python setuptools script


Solving the Schrödinger equation
--------------------------------

The time dependent Schrödinger equation (TDSE) (in `Hartree
atomic units`_) is

.. image:: https://latex.codecogs.com/svg.latex?\\Large&space;\\mathrm{i}\\partial_t\\vert{\\psi(t)}\\rangle=\\hat{H}(t)\\vert{\\psi(t)}\\rangle,\~\\vert{\\psi(t=0)}\\rangle=\\vert\\psi_0\\rangle

where |ket_psi_td| is the time-evolving state, |ket_psi_0| the initial state,
|Ht| the time-dependent Hamiltonian operator whose time-independent part
is given by |H0| with the stationary potential |V|.

The stationary states of the time-independent Hamiltonian can be solved
from the time-independent Schrödinger equation (TISE)

.. image:: https://latex.codecogs.com/svg.latex?\\Large&space;\\hat{H_0}\\vert\\psi_k\\rangle=E_k\\vert\\psi_k\\rangle,

where |Ek| and |psik| are the ith eigenenergy and eigenstate.

In a typical setup, the initial state for the time propagation, |ket_psi_0|, is one
of the stationary states. 

.. |ket_psi_td| image:: https://latex.codecogs.com/svg.latex?\\Large&space;\\vert{\\psi(t)}\\rangle 
.. |ket_psi_0| image:: https://latex.codecogs.com/svg.latex?\\Large&space;\\vert{\\psi_0}\\rangle 
.. |Ht| image:: https://latex.codecogs.com/svg.latex?\\Large&space;\\hat{H}(t)=\\hat{H}_0+\\hat{W}(t)
.. |H0| image:: https://latex.codecogs.com/svg.latex?\\Large&space;\\hat{H}_0=\\hat{T}+\\hat{V}
.. |V| image:: https://latex.codecogs.com/svg.latex?\\Large&space;\\hat{V}
.. |Ek| image:: https://latex.codecogs.com/svg.latex?\\Large&space;E_k
.. |psik| image:: https://latex.codecogs.com/svg.latex?\\Large&space;\\vert\\psi_k\\rangle
.. _Hartree atomic units: https://en.wikipedia.org/wiki/Atomic_units

Theoretical background
----------------------

For description on how TISE and TDSE have been discretized, please see 
`MyArticle`_.

.. _MyArticle: https://notpublished.yet

In short, we describe our system in cylindrical coordinates assuming zero
magnetic quantum number |m=0|. This allows us to describe the system in a 2D
slice of the cylindrical coordiante system. We select simulation domains 
|omegati| and |omegatd| for TISE and TDSE and mesh them with unstructured 
triangular meshes. Note that the simulation domains can be different so you
can, e.g., increase the simulation domain for TDSE calculations if need be.

After meshing, one selects the basis functions. They are Lagrange polynomials
up to some degree n with compact support on the mesh cells. Meshing and
choosing the basis allows us to discretize the Schrödinger equations to

.. image:: https://latex.codecogs.com/svg.latex?(\\mathbf{T}+\\mathbf{V})\\boldsymbol\\psi_k=\\mathbf{S}E_k\\boldsymbol\\psi_k

and

.. image:: https://latex.codecogs.com/svg.latex?\\mathrm{i}\\mathbf{S}\\boldsymbol{\\psi}(t)=\\left(\\mathbf{T}+\\mathbf{V}+\\mathbf{W}\\right)\\boldsymbol\\psi(t),

where |psiti| are vectors of the real-valued expansion coefficients of the
stationary states, |psitd| is a vector of the complex-valued expansion
coefficients of the time-dependent state, and the system matrices in the
Lagrange polynomial basis |basis| are given by

.. image:: https://latex.codecogs.com/svg.latex?\\Large&space;\\mathbf{S}_{ij}=\\langle\\psi_i\\vert\\psi_j\\rangle,

.. image:: https://latex.codecogs.com/svg.latex?\\Large&space;\\mathbf{T}_{ij}=-\\frac{1}{2}\\sum\\limits_{\\alpha=\\rho,z}\\langle\\partial_\\alpha\\phi_i\\vert\\partial_\\alpha\\phi_j\\rangle,

.. image:: https://latex.codecogs.com/svg.latex?\\Large&space;\\mathbf{V}_{ij}=\\langle\\psi_i\\vert{V(\\rho,z)}\\psi_j\\rangle,

and

.. image:: https://latex.codecogs.com/svg.latex?\\Large&space;\\mathbf{W}_{ij}=\\langle\\psi_i\\vert{W(\\rho,z,\\partial_\\rho,\\partial_z)}\\psi_j\\rangle.

Here the natural inner product is

.. image:: https://latex.codecogs.com/svg.latex?\\Large&space;\\langle\\chi\\vert\\psi\\rangle=\\int\\limits_{\\Omega_{\\mathrm{TI}/\\mathrm{TD}}}\\chi^*(\\rho,z)\\psi(\\rho,z)\,\\rho\,\\mathrm{d}\\rho\,\\mathrm{d}z.


Note that we have emposed continuity boundary condition at |rho0| and either
zero Dirichlet or zero Neumann boundary conditions elsewhere on the boundary.

.. |rho0| image:: https://latex.codecogs.com/svg.latex?\\rho=0

.. |basis| image:: https://latex.codecogs.com/svg.latex?\\{\\phi_i\\}_{i=0}^{N-1}

.. |psiti| image:: https://latex.codecogs.com/svg.latex?\\boldsymbol{\\psi}_k

.. |psitd| image:: https://latex.codecogs.com/svg.latex?\\boldsymbol{\\psi}(t)

.. |m=0| image:: https://latex.codecogs.com/svg.latex?m=0

.. |omegati| image:: https://latex.codecogs.com/svg.latex?\\Omega_{\\mathrm{TI}}

.. |omegatd| image:: https://latex.codecogs.com/svg.latex?\\Omega_{\\mathrm{TD}}


Interactions
++++++++++++

By default we implement three types of laser-matter interactions |Wint|:

the dipole approximation in the length gauge for linearly polarized vector
potentials |Alin|

.. image:: https://latex.codecogs.com/svg.latex?\\Large&space;W=z\\partial_t{f(t)}

the dipole approximation in the length gauge for linearly polarized vector
potentials |Alin|,

.. image:: https://latex.codecogs.com/svg.latex?\\Large&space;W=-\\mathrm{i}f(t)\\partial_z

and nonhomogeneous vector potentials |Anh|

.. image:: https://latex.codecogs.com/svg.latex?\\Large&space;W=f(t)\\mathbf{A}_s\\cdot\\mathbf{\\hat{p}}+\\frac{1}{2}f(t)^2\\Vert\\mathbf{A}_s\\Vert^2.

.. |Wint| image:: https://latex.codecogs.com/svg.latex?W(\\rho,z,\\partial_\\rho,\\partial_z)

.. |Alin| image:: https://latex.codecogs.com/svg.latex?\\mathbf{A}(\\rho,z,t)=f(t)\\boldsymbol{\\mathrm{e}}_z

.. |Anh| image:: https://latex.codecogs.com/svg.latex?\\mathbf{A}(\\rho,z,t)=\\mathbf{A}_s(\\rho,z)f(t)


Using FIEND
===========

A single time-dependent simulation consists of 4 steps:

1. **Solving the time-independent system to obtain an initial state**
2. **Preparing the system matrices for time evolution**
3. **Time evolution**
4. **Post-processing/analysis**

These steps are described in detail in the following when simulating atomic
systems under linearly polarized laser fields. For more complex cases, please
see the examples in ``demos/nanotip``.

Step 1. Solving TISE
--------------------

Time-independent system should always be solved first. Make sure that you have
loaded environment with a FEniCS installation supporting HDF5, PETSc, and
SLEPc. In the pre-installed Docker image, you can use the command 
``ml petsc/real``.

TISE can be solved with the script ``fiend_linpol_tise``. It solves an atomic system
within the single active electron approximation, and the atomic potential can
be selected with the command line option ``--atom_type``.

For a full list of options run  ``fiend_linpol_tise --help``. Examples can be found in
``demos/hhg/step1.sh`` and ``demos/hhg/step2.sh``.

New static potentials can be implemented in
``fiend.utils.predefined_potentials``, please see the module source for further
details.

``solve_tise`` saves the following files:

- ``data/tise_mesh.h5`` which includes the mesh used for
  solving TISE.
- ``data/tise_eigenvalues`` which is a list of eigenenergies
- ``data/tise_states.h5`` which contains the expansion coefficients for all the
  stationary states
- ``data/config`` which includes the simulation parameters used for solving
  the TISE

Step 2. Preparing system matrices for TDSE
------------------------------------------

After solving TISE, you should set up matrices for time dependent simulations.
For atomic systems in linearly polarized fields this can be accomplished with
the script ``fiend_linpol_prepare_tdse``, but for more complex setups see
``demos/nanotip/``. Make sure that you have loaded a FEniCS installation with 
hdf5, petsc, and slepc enabled. In the Docker image this can be achieved with
``ml petsc/real``.

The main feature of this step is that it can change the mesh from the TISE
simulation. This allows you to solve TISE in a small simulation domain
and use a larger simulation domain for time-dependent simulation.
A full list of options can be obtained with ``fiend_linpol_prepare_tdse --help``.
If some of the options are not given, the values used in solving the TISE are
used. So, e.g., if you only want to increase the radius of the meshed domain,
supply only ``--radius X`` where X is the new radius.

Complex absorbing potentials (CAP) can be included in the time propagation
simulations with options

- ``--cap_width`` which sets the width of the absorber from the domain
  boundary
- ``--cap_height`` which sets the strength of the absorber

Also other absorbers such as the smooth exterior complex scaling could easily be
implemented.

``prepare_tdse`` saves the following files using PETSc binary format

- ``data/tdse_CAP*`` containing the imaginary part of the CAP matrix
- ``data/tdse_H0*`` containing the time-independent part of the Hamiltonian matrix
- ``data/tdse_S*`` containing the overlap matrix
- ``data/tdse_rho*`` containing the |rho|-component of the dipole matrix
- ``data/tdse_Z*`` containing the z-component of the dipole matrix
- ``data/tdse_partialRho*`` containing matrix elements of |partialrho|
- ``data/tdse_partialZ*`` containing matrix elements of |partialz|
- ``data/tdse_state_N*`` containing the vector representation of the stationary
  states in the TDSE mesh

In addition, ``fiend_linpol_prepare_tdse`` saves the new mesh in
``data/tdse_mesh.h5`` and *appends* the new configuration parameters in ``data/config``.


**NOTE:** There are three versions of the overlap matrix, ``S``, ``S0``, and
``S1``. ``S`` is the pure overlap matrix, ``S0`` has the rows corresponding to
the Dirichlet boundaries zeroed, and ``S1`` is like ``S0`` but it has 1s on the
diagonals of the zeroed rows. For all other matrices, the rows corresponding to
the Dirichlet boundaries are always zeroed.

.. |rho| image::  https://latex.codecogs.com/svg.latex?\\rho

.. |partialrho| image:: https://latex.codecogs.com/svg.latex?\\partial_\\rho

.. |partialz| image:: https://latex.codecogs.com/svg.latex?\\partial_z

Step 3. Propagation
-------------------

Now you must load Python packages petsc4py, slepc4py, and mpi4py with support
for *complex numbers*. In the docker
image this can be done with ``ml petsc/complex``.
Unfortunately, currently (as of version 2018.1.0)
FEniCS doesn't support PETSc with complex numbers so we must resort to
two different versions of the python
packages, but hopefully in the near future we can remedy this.

Time propagation can be achieved with the command ``fiend_linpol_propagate``. It reads
the matrices prepared in step 2 and uses those for time propagation. A complete
list of options can be printed out with ``fiend_linpol_propagate --help``.

Note that you can request saving frequency with ``--save_interval``. E.g.,
``--save_interval 10`` saves every 10th time-step.
Time-propagation saves data to

- ``data/tdse_observables.npz`` which includes an array for each observable (except
  the density)
- ``data/tdse_wavefunction/realpart_iteration_N_real`` which is a PETSc vector of the expansion
  coefficients for the real part of the wavefunction at saveslot ``N``
- ``data/tdse_wavefunction/imagpart_iteration_N_real`` which is a PETSc vector of the expansion coefficients
  for the imaginary part of the wavefunction at saveslot ``N``
- ``data/config`` where it appends new configuration options

Setting laser field
+++++++++++++++++++

The laser-field can be set with option ``--vecpot path``. The file should be

1. a two-column file where the first column is time and second the
   time-dependent part of the vector potential, or
2. a multi-pulse configuration defining the time-dependent part of the vector
   potential with each wavelength channel defined as::

        [Pulse1]
        A = 0.1
        w = 0.0569
        k = 0
        tcenter = 0
        cep = 0.05
        fwhm = 150

   Here ``A`` is the electric field peak amplitude, ``w`` the carrier
   frequency, ``k`` the chirp, ``tcenter`` the time of envelope maximum,
   ``cep`` the carrier envelope phase, and ``fwhm`` the full with at half
   maximum for the envelope.


Step 4. Post-processing
-----------------------

``--save`` option for the post-processing scripts saves the figures to
``data/figures`` and data to ``data/postprocessing``.

``animate_density``
+++++++++++++++++++

This script reads data from ``data/tdse_wavefunction/`` and animates 
the electron density. This script needs FEniCS (``ml petsc/real`` 
when using Docker). 

``draw_norm``
+++++++++++++

For drawing the norm as a function of time. 

``draw_dipole`` / ``draw_velocity`` / ``draw_acceleration``
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

Draws the dipole moment/dipole velocity/dipole acceleration
as a function of time, the corresponding spectrum,
and stft of the spectrum. 

``draw_pes``
++++++++++++

Draws the angle-integrated and angle-resolved photoelectron spectra. Can use
MPI to speed up computation of the spectra.

PETSc and SLEPc options
-----------------------

PETSc and SLEPc have numerous options to fine-tune their operation. All
arguments passed to scripts after ``PETSC_ARGS`` are used to initialize the
PETSc options database and the arguments before that remain in sys.argv and are
used by the argumentparser of FIEND.

Installation
============

Using Docker
------------

We recommend using Docker images for running simulations on your personal
computer. For supercomputers and clusters, we recommend either installing 
the entire package from source or with ``pip``.

To use the prepared Docker image, first install `Docker
<https://www.docker.com>_` to your PC. The docker image for
`fiend <https://hub.docker.com/r/solanpaa/fiend>_` can fetched with the
command ``docker pull solanpaa/fiend``. Please note that the image is a few GB in size.

By default, running the docker image for interactive process,

    ``docker run -it fiend``

drops you in a Unix shell. All the scripts are pre-installed,
and you can switch between the complex and
real PETSc installations with commands ``ml petsc/real`` and
``ml petsc/complex``.

To enable GUIs for the scripts, you should launch the docker container with
the commands executed on the HOST machine (works on Linux)

``$ xhost +local:docker``

``$ docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:ro -it fiend``

As you probably wish to save the datafiles computed within the container, you
should create a directory ``data`` on your HOST and mount it to the container
with

``$ docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:ro -v
`pwd`/data:/home/fiend/data:Z -it fiend``

This also allows you to provide the laser parameters by saving it to a file
within ``data`` on the HOST and passing the argument ``--vecpot data/filename``
to ``docker run fiend fiend_linpol_propagate``.

For non-interactive use, you can pass the above command arguments corresponding
to the script you would like to execute together with its arguments, e.g.,

``$ docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:ro -v
`pwd`/data:/home/fiend/data:Z fiend fiend_linpol_tise --radius 10 --how_many 3``

Parallelization of the linear algebra backend can be achieved with the flag
``-e OPENBLAS_NUM_THREADS N`` of ``docker run``. MPI-parallelized simulations
can be achieved with the environment variable ``NMPIPROC``, e.g.,

``$ docker run -e NMPIPROC=3 -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix:ro -v
`pwd`/data:/home/fiend/data:Z fiend fiend_linpol_tise --radius 10 --how_many 3``


Installation with pip
---------------------

``pip3 install fiend`` should do the trick. Note that you have to manually install
real and complex PETSc, SLEPc, petsc4py, slepc4py, and FEniCS suite.

Installation from sources
-------------------------

The ``fiend`` package is hosted at `GitLab <https://gitlab.com/qcad.fi/fiend>_`.

``python3 setup.py install`` should install the package. Note that you have to 
manually install real and complex PETSc, SLEPc, petsc4py, slepc4py, and FEniCS 
suite.

Authors
=======

Janne Solanpää
