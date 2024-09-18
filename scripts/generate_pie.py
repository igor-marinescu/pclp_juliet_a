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
""" generate_pie - generates pie charts.
"""
import random
import matplotlib.pyplot as plt

#-------------------------------------------------------------------------------
def gen_pie(axes, pie_data, pie_fullness = 0.95):
    """ Generate a pie chart.
        axes - drawing axes
        pie_data a tuple: (pie_title, slices_data_dict, slices_colors_dict)
        Where:
            slices_data_dict - a dictionary containing the names and values for all slices:
                {slice1_name : slice1_val, slice2_name : slice2_val2, ... }
            slices_colors_dict - a dictionary containing the color for every slice:
                {slice1_name : slice1_color, slice2_name : slice2_color, ...}

        pie_fullness - how much of the pie (in percent) occupy the slices 
                    and the rest of the slices (below this percent) will not be
                    displayed, intead one "others" slice used for the remaining slices
    """
    # Calculate the sum of all slices and the count of non-null slices
    sum_vals = 0
    not_null_cnt = 0
    for item in pie_data[1].values():
        if item:
            sum_vals += item
            not_null_cnt += 1

    # Sort the slices dictionary based on values
    slices_sorted_list = sorted(pie_data[1].items(), key=lambda x: x[1], reverse = True)
    # This generates a sorted list of tuples: [(<slice_name>, <slice_val>),...]
    # Example: [("i793", 15), ("w746", 10), ("i2707", 3), ("e838", 3), ... ]

    slices_values = []
    slices_labels = []
    slices_colors = []
    slices_explode = []

    # Iterate through the list of sorted slices and generate the values-, labels-,
    # colors-lists for the pie. At the same time calculate the occupied pie in %
    # and if the pie is > pie_fullness full and there are more than 1 remaining
    # slice to display ignore it - display "others" instead
    pie_full_percent = 0.0
    other_val = 0
    for idx, slice_tuple in enumerate(slices_sorted_list):
        slice_name = slice_tuple[0]
        slice_val = slice_tuple[1]
        if not slice_val:
            # Stop here, no need to continue
            # the rest of slices are also nulls (the slices list is sorted)
            break
        # If the pie is > pie_fullness full and there are more than 1 remaining
        # slice to display add the remaining slices into one "others" slice
        rest_cnt = not_null_cnt - idx
        if other_val or (pie_full_percent > pie_fullness and rest_cnt > 1):
            pie_full_percent += (slice_val / sum_vals)
            other_val += slice_val
            continue
        slices_values.append(slice_val)
        slices_labels.append(slice_name)
        slices_colors.append(pie_data[2][slice_name])
        slices_explode.append(0.1)
        pie_full_percent += (slice_val  / sum_vals)

    # Add the remaining "others" slice
    if other_val > 0:
        slices_values.append(other_val)
        slices_labels.append("others")
        slices_colors.append(pie_data[2]["others"])
        slices_explode.append(0.1)

    # plotting the pie chart
    #plt.clf()
    axes.pie(slices_values,
            labels = slices_labels,
            colors = slices_colors,
            startangle = 90,
            shadow = False,
            explode = tuple(slices_explode),
            radius = 0.8,
            autopct = '%1.0f%%',
            rotatelabels = True
            )
    axes.set_title(pie_data[0])

    #plt.savefig(pie_filename)
    #plt.show()

#-------------------------------------------------------------------------------
def gen_plt(pie_data):
    """ Generate a plot containing a 2D array of pie charts (every on its axes)

        pie_data a 2D-list (lits in list) of pies:

            pie_data = [
                [pie_data00, pie_data01, ... pie_data0M],
                [pie_data10, pie_data11, ... pie_data1M],
                ...
                [pie_dataN0, pie_data11, ... pie_dataNM]
            ]

        Every pie_data is defined as a tuple: 
                (pie_title, slices_data_dict, slices_colors_dict)    
        Where:
            slices_data_dict - a dictionary containing the names and values for all slices:
                {slice1_name : slice1_val, slice2_name : slice2_val2, ... }
            slices_colors_dict - a dictionary containing the color for every slice:
                {slice1_name : slice1_color, slice2_name : slice2_color, ...}

    """

    # Detect the number of rows and columns in pie_data 2D-list
    plt_rows = len(pie_data)
    plt_cols = 0
    for i_row in pie_data:
        plt_cols = max(plt_cols, len(i_row))

    # Create the figure and populate with pies
    fig, axes = plt.subplots(plt_rows, plt_cols, figsize=(10.0, 10.0))
    if plt_rows == 1 and plt_cols == 1:
        gen_pie(axes, pie_data[0][0])
    elif plt_rows == 1:
        for i in range(plt_cols):
            gen_pie(axes[i], pie_data[0][i])
    elif plt_cols == 1:
        for i in range(plt_rows):
            gen_pie(axes[i], pie_data[i][0])
    else:
        for i in range(plt_rows):
            for j in range(plt_cols):
                gen_pie(axes[i][j], pie_data[i][j])

    #plt.savefig(pie_filename)
    plt.show()

#-------------------------------------------------------------------------------
def gen_random_pie_data(title):
    """ Generate data for a random pie.
        title - title of the pie to be generated
        Return: the generated data as a tuple:
            (pie_title, slices_data_dict, slices_colors_dict)
        Where:
            slices_data_dict - a dictionary containing the names and values for all slices:
                {slice1_name : slice1_val, slice2_name : slice2_val2, ... }
            slices_colors_dict - a dictionary containing the color for every slice:
                {slice1_name : slice1_color, slice2_name : slice2_color, ...}
    """

    color_list = ["lightcoral", "plum", "coral", "palegreen", "beige",
                  "powderblue", "sandybrown", "darkkhaki", "lightsteelblue", "lavender"]

    slices_test_data_dict = {}
    slices_test_colors_dict = {}
    slices_test_colors_dict["others"] = "rosybrown"
    for i in range(20):
        slice_name = "s" + str(i)
        slices_test_data_dict[slice_name] = random.randint(1, 800)
        slices_test_colors_dict[slice_name] = random.choice(color_list)

    #sum_val = sum(slices_test_data_dict.values())
    #print("Sum slices: ", sum_val)

    #for sl_name, sl_val in slices_test_data_dict.items():
    #    print(sl_name, ":", sl_val, "\t", int(sl_val * 100 / sum_val), "%")

    return (title, slices_test_data_dict, slices_test_colors_dict)


#-------------------------------------------------------------------------------
if __name__ == '__main__':
    # Generate test pie-image

    NROWS = 2
    NCOLS = 1

    random.seed()

    pies_data = []
    for row in range(NROWS):
        pies_data.append([])
        for col in range(NCOLS):
            pies_data[row].append(gen_random_pie_data("TestPie" + str(row) + str(col)))

    gen_plt(pies_data)
