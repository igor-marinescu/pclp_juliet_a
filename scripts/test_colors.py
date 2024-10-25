# This file is part of the pclp_juliet_a distribution.
# Copyright (c) 2024 Igor Marinescu (igor.marinescu@gmail.com).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#-------------------------------------------------------------------------------
""" Module used to test different color schemes
"""
import math
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle

#------------------------------------------------------------------------------
def plot_colortable():
    """ Display a color-table.
        Code copied from matplotlib examples. 
    """

    cell_width = 212
    cell_height = 22
    swatch_width = 48
    margin = 12
    ncols=1

    # Sort colors by hue, saturation, value and name.
    #names = ["lightcoral", "orange", "mediumaquamarine", "lightsteelblue",\
    #         "sandybrown", "palegreen", "skyblue", "pink",\
    #         "salmon", "gold", "slategray", "lightseagreen",\
    #         "rosybrown", "khaki", "paleturquoise", "palevioletred",\
    #         "burlywood", "darkkhaki", "cadetblue", "thistle",\
    #         "lightgray", "peachpuff", "lightcyan", "plum",\
    #         "tomato", "palegoldenrod", "powderblue", "lavender",\
    #         "navajowhite", "yellowgreen", "beige", "aquamarine"]

    #names = ["rosybrown", "lightcoral", "indianred", "salmon", "tomato",
    #         "bisque", "navajowhite", "peachpuff", "moccasin", "wheat",
    #         "mediumaquamarine", "aquamarine", "turquoise", "mediumturquoise",  "darkturquoise",
    #         "paleturquoise", "powderblue", "lightblue", "skyblue", "lightskyblue",
    #         "darkgray", "darkgrey", "silver", "lightgray", "lightgrey"]

    names = ["red", "firebrick", "maroon", "crimson", "darkred",    # Error
             "lightcoral", "indianred", "salmon", "tomato", "coral",    # Warning
             "coral", "salmon", "darksalmon", "lightsalmon", "sandybrown", # Info
             "bisque", "navajowhite", "peachpuff", "moccasin", "wheat", # Supp
             "paleturquoise", "powderblue", "lightblue", "skyblue", "lightskyblue" # Note
             ]

    n = len(names)
    nrows = math.ceil(n / ncols)

    width = cell_width * ncols + 2 * margin
    height = cell_height * nrows + 2 * margin
    dpi = 72

    fig, ax = plt.subplots(figsize=(width / dpi, height / dpi), dpi=dpi)
    fig.subplots_adjust(margin/width, margin/height,
                        (width-margin)/width, (height-margin)/height)
    ax.set_xlim(0, cell_width * ncols)
    ax.set_ylim(cell_height * (nrows-0.5), -cell_height/2.)
    ax.yaxis.set_visible(False)
    ax.xaxis.set_visible(False)
    ax.set_axis_off()

    for i, name in enumerate(names):
        row = i % nrows
        col = i // nrows
        y = row * cell_height

        swatch_start_x = cell_width * col
        text_pos_x = cell_width * col + swatch_width + 7

        ax.text(text_pos_x, y, str(i + 1) + " - " + name,
                horizontalalignment='left',
                verticalalignment='center')

        ax.add_patch(
            Rectangle(xy=(swatch_start_x, y-9), width=swatch_width,
                      height=18, facecolor=mcolors.CSS4_COLORS[name], edgecolor='0.7')
        )

    return fig

#-------------------------------------------------------------------------------
if __name__ == '__main__':
    #print(mcolors.CSS4_COLORS)
    plot_colortable()
    plt.show()
