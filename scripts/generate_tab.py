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
import matplotlib.pyplot as plt

#-------------------------------------------------------------------------------
def gen_tab(tab_axes, data_dict, location = 'top'):
    """ Generate a table with issues names and their description.
        tab_axes - axes of the table
        data_dict - a dictionary containing the issue name and its description:
            {issue1_name : issue1_descr, issue2_name : issue2_descr, ... }
    """

    row_labels = list(data_dict.keys())

    cell_text = []
    for row in data_dict.values():
        row_text = []
        row_text.append(row)
        cell_text.append(row_text)

    tab_axes.axis('off')
    tab_axes.table(
        cellText=cell_text,
        rowLabels=row_labels,
        cellLoc='left',
        loc = location
    )

#-------------------------------------------------------------------------------
def gen_test_tab_data():
    """ Generate and return a dictionary containing test data for a table 
    """

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
        "cannot pass __string__ to variadic __string__; expected type from format string",
    ]

    return dict(zip(row_labels, cdata))

#-------------------------------------------------------------------------------
if __name__ == '__main__':

    # Generate test table using test data
    tab_test_dict = gen_test_tab_data()
    fig, taxes = plt.subplots()
    gen_tab(taxes, tab_test_dict, None)
    plt.show()
