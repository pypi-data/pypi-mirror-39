#!/bin/bash

# Create data directory
mkdir -p data

ml petsc/real

# Solve TISE
python3 -m fiend.lin_pol.solve_tise --atom_type H --radius 30 --core_radius 2 --refinement_radius 10 \
  --cellradius 1 --core_cellradius 0.01 --num_states 2 --eigensolver_tol 1e-6 \
  --debug --eigensolver_type rqcg

# Prepare matrices for TDSE
python3 -m fiend.lin_pol.prepare_tdse --radius 700 --core_radius 5 --refinement_radius 20 \
  --cellradius 0.2 --core_cellradius 0.01 --cap_width 50 --cap_height 1.0

# Setup laser
cp laser data/laser

ml petsc/complex

# Propagate
python3 -m fiend.lin_pol.propagate --vecpot data/laser \
    --initial_state 0 --observables norm dipole_z wavefunction acceleration_z \
    --save_interval 10 --gauge velocity --propagator petsc_cn \
    --delta_t 0.07 --debug --solver_type krylov --inverse_tolerance 1e-20
