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
""" generate_tab - generates table.
"""
import random
import matplotlib.pyplot as plt

#-------------------------------------------------------------------------------
if __name__ == '__main__':

    row_labels = ['e131', 'e132', 'e136', 'e138', 'e139', 'e148', 'e157', 'e160', 'e161', 'e175']

    cdata = [
        "too few arguments provided to function-like macro invocation",
        "expected function definition",
        "illegal macro name",
        "cannot create recursive relationship between '__strong-type__' and '__strong-type__'",
        "cannot take sizeof a function",
        "member __name__ previously declared",
        "no data may follow an incomplete array",
        "the sequence ({ is non standard and is taken to introduce a GNU statement expression",
        "repeated use of parameter __symbol__ in parameter list",
        "cannot pass __string__ to variadic __string__; expected type from format string was __type__"
    ]


    cell_text = list()
    for row in cdata:
        row_text = list()
        row_text.append(row)
        cell_text.append(row_text)

    fig, axs = plt.subplots()
    axs.axis('off')
    axs.table(
        cellText=cell_text,
        rowLabels=row_labels,
        cellLoc='left',
        loc='center',
    )

    plt.show()