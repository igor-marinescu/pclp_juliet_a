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
import numpy as np

#-------------------------------------------------------------------------------
def gen_pie(pie_axes, pie_title, data_dict, colors_dict, colors_dict2 = None):
    """ Generate a pie chart.
        pie_axes - axes of the pie
        pie_title - the title to be displayed inside of the pie
        data_dict - a dictionary containing the names and values for all slices:
            {slice1_name : slice1_val, slice2_name : slice2_val2, ... }
        colors_dict - a dictionary containing the color for every slice:
            {slice1_name : slice1_color, slice2_name : slice2_color, ...}
        colors_dict2 - a dictionary containing additional colors for a 
            nested pie (None in case no nested pie to be displayed)
        pie_fullness = 0.95 - how much of the pie (in percent) occupy the slices
                    and the rest of the slices (below this percent) will not be
                    displayed, intead one "others" slice used for the remaining slices
    """
    # Calculate the sum of all slices and the count of non-null slices
    sum_vals = 0
    not_null_cnt = 0
    for item in data_dict.values():
        if item:
            sum_vals += item
            not_null_cnt += 1

    # Sort the slices dictionary based on values
    slices_sorted_list = sorted(data_dict.items(), key=lambda x: x[1], reverse = True)
    # This generates a sorted list of tuples: [(<slice_name>, <slice_val>),...]
    # Example: [("i793", 15), ("w746", 10), ("i2707", 3), ("e838", 3), ... ]

    slices_values = []
    slices_labels = []
    slices_colors = []
    slices_colors2 = []

    # Iterate through the list of sorted slices and generate the values-, labels-,
    # colors-lists for the pie. At the same time calculate the occupied pie in %
    # and if the pie is > pie_fullness (0.95) full and there are more than 1 remaining
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
        # If the pie is > pie_fullness (0.95) full and there are more than 1 remaining
        # slice to display add the remaining slices into one "others" slice
        rest_cnt = not_null_cnt - idx
        if other_val or (pie_full_percent > 0.95 and rest_cnt > 1):
            pie_full_percent += (slice_val / sum_vals)
            other_val += slice_val
            continue
        slices_values.append(slice_val)
        slices_labels.append(slice_name)
        slices_colors.append(colors_dict[slice_name])
        pie_full_percent += (slice_val  / sum_vals)
        if colors_dict2:
            slices_colors2.append(colors_dict2[slice_name])

    # Add the remaining "others" slice
    if other_val > 0:
        slices_values.append(other_val)
        slices_labels.append("others")
        slices_colors.append(colors_dict["others"])
        slices_colors2.append(colors_dict["others"])

    # plotting the pie chart
    wedges, texts = pie_axes.pie(slices_values,
            colors = slices_colors,
            startangle = 90,
            shadow = False,
            #radius = 0.9,
            )

    # plotting nested pie chart?
    if colors_dict2:
        pie_axes.pie(slices_values,
            colors = slices_colors2,
            startangle = 90,
            shadow = False,
            radius = 0.85,
            )

    # add annotations
    kwargs = {"arrowprops":{"arrowstyle":'-'}, "zorder":0, "va":'center'}
    for idx, wedge in enumerate(wedges):
        theta_diff = wedge.theta2 - wedge.theta1
        # If the slice to small (small angle) do not display annotation
        if theta_diff <= 4.0:
            continue

        ang = theta_diff/2.0 + wedge.theta1
        y_pos = np.sin(np.deg2rad(ang))
        x_pos = np.cos(np.deg2rad(ang))

        y_text = 1.2 * y_pos
        x_text = 1.18 * np.sign(x_pos)

        slice_text = slices_labels[idx] + " (" + str(slices_values[idx]) + ")"

        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x_pos))]

        connectionstyle = f"angle,angleA=0,angleB={ang}"
        kwargs["arrowprops"].update({"connectionstyle": connectionstyle})
        pie_axes.annotate(slice_text, xy=(x_pos, y_pos), xytext=(x_text, y_text),
            horizontalalignment=horizontalalignment, fontsize=12.0, **kwargs)

    # add title in the center
    hole = plt.Circle((0, 0), 0.7, facecolor='white')
    pie_axes.add_artist(hole)
    pie_axes.text(0.0, 0.0, pie_title, horizontalalignment = "center",\
              verticalalignment = "center", fontsize = 30.0)

#-------------------------------------------------------------------------------
def gen_random_pie_data(title, big_val_cnt, big_val_max, small_val_cnt, small_val_max):
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

    # Add big balues
    for i in range(big_val_cnt):
        slice_name = "s" + str(i)
        slices_test_data_dict[slice_name] = random.randint(small_val_max, big_val_max)
        slices_test_colors_dict[slice_name] = random.choice(color_list)

    # Add small values
    for i in range(small_val_cnt):
        slice_name = "s" + str(big_val_cnt + i)
        slices_test_data_dict[slice_name] = random.randint(1, small_val_max)
        slices_test_colors_dict[slice_name] = random.choice(color_list)

    sum_val = sum(slices_test_data_dict.values())
    print("Sum slices: ", sum_val)

    for sl_name, sl_val in slices_test_data_dict.items():
        print(sl_name, ":", sl_val, "\t", int(sl_val * 100 / sum_val), "%")

    return (title, slices_test_data_dict, slices_test_colors_dict)

#-------------------------------------------------------------------------------
if __name__ == '__main__':

    # Generate test pie-image using random data
    random.seed()
    fig, paxes = plt.subplots(figsize=(10.0, 10.0))
    pd = gen_random_pie_data("TestPie:\nR=0 C=2", 15, 100, 30, 10)
    gen_pie(paxes, pd[0], pd[1], pd[2])
    paxes.set_title(pd[0])
    #plt.savefig(filename)
    plt.show()
