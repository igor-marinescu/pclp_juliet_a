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
""" Module used to test different types of pies
"""
import matplotlib.pyplot as plt

#-------------------------------------------------------------------------------
slices_text_list = [
        "slice0", "slice4", "slice3", "slice8", "slice1",
        "slice6", "slice2", "slice5", "slice7", "slice9" ]

slices_vals_list1 = [ 100, 67, 45, 34, 23,  12, 20, 10, 5, 4 ]
slices_vals_list2 = [ 200, 17, 35, 14, 23,  12, 10,  6, 5, 4 ]
slices_vals_list3 = [  10, 57,  5, 54, 13, 112, 10,  6, 5, 4 ]
slices_vals_list4 = [  57, 10, 55,154,113,   2,110, 66,14,54 ]

slices_colors_list = [
        "lightcoral", "plum", "coral", "palegreen", "beige", "powderblue",
        "sandybrown", "darkkhaki", "lightsteelblue", "lavender", "rosybrown" ]

slices_explode_list = []
for slice_val in slices_vals_list1:
    slices_explode_list.append(0.1)

#-------------------------------------------------------------------------------
fig, axes = plt.subplots(2, 2, figsize=(10.0, 10.0))

#-------------------------------------------------------------------------------
wedges, texts, autotexts = axes[0][0].pie(slices_vals_list1,
        labels = slices_text_list,
        colors = slices_colors_list,
        startangle = 90,
        shadow = False,
        explode = tuple(slices_explode_list),
        radius = 0.75,
        autopct = '%1.0f%%',
        rotatelabels = True
        )

axes[0][0].set_title("Pie Chart1")
#plt.text(x = 0., y = -1., s = "Pie Chart1")
#plt.xlabel("Pie Chart1", labelpad = -2.)

#-------------------------------------------------------------------------------
axes[0][1].pie(slices_vals_list2,
        labels = slices_text_list,
        colors = slices_colors_list,
        startangle = 90,
        shadow = False,
        explode = tuple(slices_explode_list),
        radius = 1,
        autopct = '%1.0f%%',
        rotatelabels = True
        )


#-------------------------------------------------------------------------------
axes[1][0].pie(slices_vals_list3,
        labels = slices_text_list,
        colors = slices_colors_list,
        startangle = 90,
        shadow = False,
        explode = tuple(slices_explode_list),
        radius = 1,
        autopct = '%1.0f%%',
        rotatelabels = True
        )

#-------------------------------------------------------------------------------
axes[1][1].pie(slices_vals_list4,
        labels = slices_text_list,
        colors = slices_colors_list,
        startangle = 90,
        shadow = False,
        explode = tuple(slices_explode_list),
        radius = 1,
        autopct = '%1.0f%%',
        rotatelabels = True
        )

#-------------------------------------------------------------------------------
#plt.subplots_adjust(wspace=.4, hspace=.4)
#plt.savefig("output2.jpg")
plt.show()
