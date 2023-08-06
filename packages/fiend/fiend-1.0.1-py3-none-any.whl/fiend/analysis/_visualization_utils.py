"""
Convenience tools for visualizing scalar fields (dolfin.Functions).
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as tri

import dolfin as df


def plot_scalarfield(ax: plt.Axes,
                     function: df.Function,
                     log_scale=False,
                     vmin_cap=1e-10,
                     triangulation=None,
                     **kwargs) -> None:
    """
    Plots the scalarfield on the axes.

    Parameters
    ----------
    ax : matplotlib.pyplot.Axes
        Axes where we draw the graph
    function : df.Function
        Scalar field which we draw
    log_scale : bool
        Whether to modify the data for log-scale visualization
    meshtri : matplotlib.triangulation.Triangulation
    Returns
    -------
    Handle to visualized matplotlib object
    """

    mesh = function.function_space().mesh()

    vals = function.compute_vertex_values(mesh)

    if log_scale:
        vals = np.fabs(vals)
        vals[vals <= vmin_cap] = vmin_cap

    coords = mesh.coordinates()
    if triangulation:
        meshtri = triangulation
    else:
        meshtri = tri.Triangulation(coords[:, 0], coords[:, 1], mesh.cells())

    return ax.tripcolor(meshtri, vals, rasterized=True, **kwargs), meshtri
