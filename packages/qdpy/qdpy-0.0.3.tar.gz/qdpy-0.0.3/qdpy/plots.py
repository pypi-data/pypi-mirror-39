#    This file is part of qdpy.
#
#    qdpy is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    qdpy is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with qdpy. If not, see <http://www.gnu.org/licenses/>.

"""A collection of functions to plot containers using Matplotlib."""

__all__ = ["plotMAP"]

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


########### Plots ########### {{{1

def plotMAP(performances, outputFilename, cmap, featuresBounds=[(0., 1.), (0., 1.)], fitnessBounds=(0., 1.), drawCbar = True, xlabel = "", ylabel = "", cBarLabel = "", nbTicks = 10):
    data = performances
    if len(data.shape) == 1:
        data = data.reshape((1, data.shape[0]))
    nbBins = data.shape

    figsize = [2.1 + 10. * nbBins[0] / (nbBins[0] + nbBins[1]), 1. + 10. * nbBins[1] / (nbBins[0] + nbBins[1])]
    aspect = "equal"
    if figsize[1] < 2:
        figsize[1] = 2.
        aspect = "auto"

    fig, ax  = plt.subplots(figsize=figsize)
    cax = ax.imshow(data.T, interpolation="none", cmap=cmap, vmin=fitnessBounds[0], vmax=fitnessBounds[1], aspect=aspect)
    #ax.set_aspect('equal')
    ax.invert_yaxis()

    if nbBins[0] > nbBins[1]:
        nbTicksX = nbTicks
        nbTicksY = int(nbTicksX * nbBins[1] / nbBins[0])
    elif nbBins[1] > nbBins[0]:
        nbTicksY = nbTicks
        nbTicksX = int(nbTicksY * nbBins[0] / nbBins[1])
    else:
        nbTicksX = nbTicksY = nbTicks
    if nbTicksX > nbBins[0] or nbTicksX < 1:
        nbTicksX = nbBins[0]
    if nbTicksY > nbBins[1] or nbTicksY < 1:
        nbTicksY = nbBins[1]

    # Set ticks
    ax.xaxis.set_tick_params(which='major', left=False, bottom=False, top=False, right=False)
    ax.yaxis.set_tick_params(which='major', left=False, bottom=False, top=False, right=False)
    xticks = list(np.arange(0, data.shape[0] + 1, data.shape[0] / nbTicksX))
    yticks = list(np.arange(0, data.shape[1] + 1, data.shape[1] / nbTicksY))
    plt.xticks(xticks, rotation='vertical')
    plt.yticks(yticks)
    deltaFeature0 = featuresBounds[0][1] - featuresBounds[0][0]
    deltaFeature1 = featuresBounds[1][1] - featuresBounds[1][0]
    ax.set_xticklabels([round(float(x / float(data.shape[0]) * deltaFeature0 + featuresBounds[0][0]), 2) for x in xticks], fontsize=20)
    ax.set_yticklabels([round(float(y / float(data.shape[1]) * deltaFeature1 + featuresBounds[1][0]), 2) for y in yticks], fontsize=20)

    # Draw grid
    ax.xaxis.set_tick_params(which='minor', direction="in", left=True, bottom=True, top=True, right=True)
    ax.yaxis.set_tick_params(which='minor', direction="in", left=True, bottom=True, top=True, right=True)
    ax.set_xticks(np.arange(-.5, data.shape[0], 1), minor=True)
    ax.set_yticks(np.arange(-.5, data.shape[1], 1), minor=True)
    ax.grid(which='minor', color=(0.8,0.8,0.8,0.5), linestyle='-', linewidth=0.1)

    ax.set_xlabel(xlabel, fontsize=25)
    ax.set_ylabel(ylabel, fontsize=25)

    if drawCbar:
        divider = make_axes_locatable(ax)
        #cax2 = divider.append_axes("right", size="5%", pad=0.15)
        cax2 = divider.append_axes("right", size=0.5, pad=0.15)
        cbar = fig.colorbar(cax, cax=cax2, format="%.2f")
        cbar.ax.tick_params(labelsize=20)
        cbar.ax.set_ylabel(cBarLabel, fontsize=22)

    ax.autoscale_view()
    plt.tight_layout()
    fig.savefig(outputFilename)


# MODELINE	"{{{1
# vim:expandtab:softtabstop=4:shiftwidth=4:fileencoding=utf-8
# vim:foldmethod=marker
