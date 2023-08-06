# Nanotip geometry
# ----------------

apex_radius =  188.972613 # in a.u.
full_opening_angle = 20 # in degrees

# Parameters for computation of the spatial profile of the field
# --------------------------------------------------------------

eps_tip_re = -24.061
eps_tip_im = 1.5068

eps_vacuum = 1

f_boxsize = (1000, 3000)
f_refined_mesh_distance = 30
f_transition_distance = 200
f_cell_minrad = 1
f_cell_maxrad = 50

# Parameters for the solution of time-independent Schrödinger equation
# --------------------------------------------------------------------

work_function = -0.1951

ti_boxsize = (500, 800)
ti_refined_mesh_distance = 30
ti_transition_distance = 200
ti_cell_minrad = 1
ti_cell_maxrad = 50
ti_num_states = 1

# Parameters for the solution of time-dependent Schrödinger equation
# --------------------------------------------------------------------
td_boxsize = (500, 800)
td_refined_mesh_distance = 30
td_transition_distance = 200
td_cell_minrad = 1
td_cell_maxrad = 50
td_cap_width = 100
td_cap_height = 1
