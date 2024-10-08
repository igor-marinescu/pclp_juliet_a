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
def gen_pie(pie_data, filename, pie_fullness = 0.95):
    """ Generate a pie chart.
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
        slices_explode.append(0.05)
        pie_full_percent += (slice_val  / sum_vals)

    # Add the remaining "others" slice
    if other_val > 0:
        slices_values.append(other_val)
        slices_labels.append("others")
        slices_colors.append(pie_data[2]["others"])
        slices_explode.append(0.05)

    fig, axes = plt.subplots(figsize=(10.0, 8.0))

    # plotting the pie chart
    wedges, texts = axes.pie(slices_values,
            #labels = slices_labels,
            colors = slices_colors,
            startangle = 90,
            shadow = False,
            #explode = tuple(slices_explode),
            #radius = 0.9,
            #autopct = '%1.0f%%',
            #textprops={'fontsize': 8},
            rotatelabels = True
            )

    #---------------------------------------------------------------------------
    kwargs = dict(arrowprops=dict(arrowstyle="-"), zorder=0, va="center")

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
        axes.annotate(slice_text, xy=(x_pos, y_pos), xytext=(x_text, y_text),
            horizontalalignment=horizontalalignment, fontsize=12.0, **kwargs)

        #if np.sign(x) < 0:
        #    axes.annotate(str(theta_diff), xy=(x_pos, y_pos), xytext=(x_text, y_text),
        #        horizontalalignment=horizontalalignment, rotation=ang+180, **kwargs)
        #else:
        #    axes.annotate(str(theta_diff), xy=(x_pos, y_pos), xytext=(x_text, y_text),
        #        horizontalalignment=horizontalalignment, rotation=ang, **kwargs)

    # Unkomment the following lines for a donut
    hole = plt.Circle((0, 0), 0.7, facecolor='white')
    axes.add_artist(hole)
    axes.text(0.0, 0.0, pie_data[0], horizontalalignment = "center",\
              verticalalignment = "center", fontsize = 30.0)

    #---------------------------------------------------------------------------

    #axes.set_title(pie_data[0])
    #axes.legend(wedges, slices_labels, title="Categories", loc="center left",\
    #   bbox_to_anchor=(1, 0, 0.5, 1))

    if filename:
        plt.savefig(filename)
    else:
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

    BIG_VAL_CNT, BIG_VAL_MAX = 15, 100
    SMALL_VAL_CNT, SMALL_VAL_MAX = 30, 10

    # Add big balues
    for i in range(BIG_VAL_CNT):
        slice_name = "s" + str(i)
        slices_test_data_dict[slice_name] = random.randint(SMALL_VAL_MAX, BIG_VAL_MAX)
        slices_test_colors_dict[slice_name] = random.choice(color_list)

    # Add small values
    for i in range(SMALL_VAL_CNT):
        slice_name = "s" + str(BIG_VAL_CNT + i)
        slices_test_data_dict[slice_name] = random.randint(1, SMALL_VAL_MAX)
        slices_test_colors_dict[slice_name] = random.choice(color_list)

    sum_val = sum(slices_test_data_dict.values())
    print("Sum slices: ", sum_val)

    for sl_name, sl_val in slices_test_data_dict.items():
        print(sl_name, ":", sl_val, "\t", int(sl_val * 100 / sum_val), "%")

    return (title, slices_test_data_dict, slices_test_colors_dict)


#-------------------------------------------------------------------------------
if __name__ == '__main__':
    # Generate test pie-image

    random.seed()

    pd = gen_random_pie_data("TestPie:\nR=0 C=2")

    gen_pie(pd, None)
