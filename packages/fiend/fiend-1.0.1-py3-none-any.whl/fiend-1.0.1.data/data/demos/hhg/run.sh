#!/bin/bash

# Docker command which uses a persistent cache 
DOCKER_CMD='docker run --privileged --rm -v '`pwd`'/data:/home/fiend/data:Z
  -v '`echo ${HOME}`'/.cache:/home/feqdyn/.cache:Z
  -e OPENBLAS_NUM_THREADS=6 -v /tmp/.X11-unix/:/tmp/.X11-unix:ro 
  -e DISPLAY='`echo ${DISPLAY}`' fiend'

# Create data directory
mkdir -p data

# Solve TISE
${DOCKER_CMD} fiend_linpol_tise --atom_type H --radius 30 --core_radius 2 --refinement_radius 10 \
  --cellradius 1 --core_cellradius 0.01 --num_states 2 --eigensolver_tol 1e-6 \
  --debug --eigensolver_type rqcg

# Prepare matrices for TDSE
${DOCKER_CMD} fiend_linpol_prepare_tdse --radius 200 --core_radius 5 --refinement_radius 20 \
  --cellradius 0.3 --core_cellradius 0.01 --cap_width 50 --cap_height 1

# Setup laser
cp laser data/laser

# Propagate
${DOCKER_CMD} fiend_linpol_propagate --vecpot data/laser --initial_state 0 \
  --observables norm dipole_z velocity_z acceleration_z --save_interval 10 \
  --gauge velocity --propagator petsc_cn \
  --delta_t 0.07 --debug --solver_type krylov --inverse_tolerance 1e-20

# Plot results
${DOCKER_CMD} fiend_draw_acceleration --max-energy 3 --stft-color-min-intensity 1e-8
