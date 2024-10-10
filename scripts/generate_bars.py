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
""" generate_bars - generates bar charts.
"""
import random
import matplotlib.pyplot as plt

#-------------------------------------------------------------------------------
def gen_bars(bar1_dict, bar2_dict, **kwarg):
    """ Generate bar-plot.
        bar1_dict, bar2_dict - dictionaries containing the names and values for
        two sets of bars. Every dictionary (set of bars) has the format:
           {name1 : val1, name2 : val2, name3 : val3 ... }
        Other parameters:
        title - plot title
        bar1_color, bar2_color - color or list of color. The colors of the bar faces
            for both sets of bars.
        limit_cnt - limit every set to a count of bars
        filename - do not display but instead save the plot to a file
    """

    # Combine two bar-dictionaries bar1_dict and bar2_dict into one:
    #   bars_dict - a dictionary containing the names and values for both bars:
    #       {name1 : [bar1_val1, bar2_val1],
    #        name2 : [bar1_val2, bar2_val2],
    #           ...
    #       }
    bars_dict = {b_key:[b_val, 0] for (b_key, b_val) in bar1_dict.items()}

    for b_key, b_val in bar2_dict.items():
        if b_key in bars_dict:
            # If key already exists, just modify the value (element[1])
            bars_dict[b_key][1] = b_val
        else:
            # If key doesn't exist, add it toghether with the value
            # (element[0] in this case is 0)
            bars_dict[b_key] = [0, b_val]

    # Sort dictionary by bar1_val (item[1][0])
    bars_dict_sort = dict(sorted(bars_dict.items(), key=lambda item: item[1][0], reverse=False))
    #print(bars_dict_sort)

    # Generate list of names and values for bars1 and 2
    blist_names = list(bars_dict_sort.keys())
    blist_val1 = [x[0] for x in bars_dict_sort.values()]
    blist_val2 = [x[1] for x in bars_dict_sort.values()]

    # Limit the count of bars?
    if "limit_cnt" in kwarg:
        limit_cnt = kwarg["limit_cnt"]
        if limit_cnt < len(blist_names):
            limit_cnt = len(blist_names) - limit_cnt
            del blist_names[:limit_cnt]
            del blist_val1[:limit_cnt]
            del blist_val2[:limit_cnt]

    # Generate list of colors 
    bar1_color_dict = kwarg.get("bar1_color")
    blist_col1 = None
    if bar1_color_dict:
        blist_col1 = list()
        for issue_name in blist_names:
            blist_col1.append(bar1_color_dict[issue_name])

    bar2_color_dict = kwarg.get("bar2_color")
    blist_col2 = None
    if bar1_color_dict:
        blist_col2 = list()
        for issue_name in blist_names:
            blist_col2.append(bar2_color_dict[issue_name])

    #plt.clf()
    fig, axes = plt.subplots(figsize=(10.0, 10.0))
    x_offset = [0] * len(blist_names)

    width = 0.8

    axes.barh(blist_names, blist_val1, width, left=x_offset,\
            align='center', color=blist_col1)
    x_offset = [sum(x) for x in zip(blist_val1, x_offset)]
    axes.barh(blist_names, blist_val2, width, left=x_offset,\
            align='center', color=blist_col2)

    # Do not display the labels for the bars with 0 value
    for container in axes.containers:
        labels = [v if v > 0 else "" for v in container.datavalues]
        axes.bar_label(container, label_type='center', labels=labels)

    if "title" in kwarg:
        axes.set_title(kwarg["title"])

    if "filename" in kwarg:
        plt.savefig(kwarg["filename"])
    else:
        plt.show()

#-------------------------------------------------------------------------------
def gen_random_bars_data(big_cnt, big_max, small_cnt, small_max, start_idx = 0):
    """ Generate data for a random bar:
        Param:
            big_cnt - count of big values
            big_max - maximal value for big values
            small_cnt - count of small values
            small_max - maximal value for small values
            start_idx - index where elements starts
        Return: the generated data as dictionary:
            bars_data_dict - a dictionary containing the names and values for all bars:
                {bar1_name : bar1_val, bar2_name : bar2_val2, ... }
    """

    bars_test_data_dict = {}

    # Add big balues
    for i in range(big_cnt):
        slice_name = "s" + str(start_idx + i)
        bars_test_data_dict[slice_name] = random.randint(small_max, big_max)

    # Add small values
    for i in range(small_cnt):
        slice_name = "s" + str(start_idx + big_cnt + i)
        bars_test_data_dict[slice_name] = random.randint(1, small_max)

    #sum_val = sum(bars_test_data_dict.values())
    #print("Sum bars: ", sum_val)

    #for b_name, b_val in bars_test_data_dict.items():
    #    print(b_name, ":", b_val, "\t", int(b_val * 100 / sum_val), "%")

    return bars_test_data_dict

#-------------------------------------------------------------------------------
if __name__ == '__main__':

    # Generate random data for two bar-dictionaries:
    b1_dict = gen_random_bars_data(15, 100, 30, 10, 3)
    b2_dict = gen_random_bars_data(10, 100, 20, 10)

    kwargs = dict()
    kwargs["limit_cnt"] = 16

    kwargs["title"] = "true-positive vs false-positive"
    kwargs["filename"] = "out_b1.jpg"
    gen_bars(b1_dict, b2_dict, **kwargs)

    kwargs["title"] = "false-positive vs true-positive"
    kwargs['filename'] = "out_b2.jpg"
    gen_bars(b2_dict, b1_dict, **kwargs)
