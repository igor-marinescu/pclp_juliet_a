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
""" reduced - module loads the list of all makefiles and invokes the processor
    for every makefile. Can be invoked separatelly from the bash script.
"""
import os
import sys

import processor
import ignore_list
import pclp_messages
import generate_pie
import generate_bars

# Global results folder
GRES_FOLDER = "ig_gl_out"
# File where all found Makefiles are stored
MAKEFILES_NAME = "ig_makefiles_win1.txt"
# File where global results (for all makefiles) are stored
GRES_OUT_FILE = "ig_global_results.txt"
# PClint output file:
PCLP_OUT_FILE="ig_pclint_out.txt"
# File where output from interpreter is stored
INTR_OUT_FILE="ig_interpret_out.txt"

# False-Positive colors
cfp_list_r = ["lightcoral", "indianred", "salmon", "tomato", "darksalmon", "coral", "orangered", "lightsalmon"]
cfp_list_y = ["sandybrown", "darkorange", "orange", "goldenrod", "gold", "khaki", "navajowhite"]
cfp_list_p = ["plum", "pink", "thistle", "orchid", "hotpink"]

# True-Positive colors
ctp_list_g = ["yellowgreen", "palegreen", "limegreen", "mediumspringgreen"]
ctp_list_t = ["mediumaquamarine", "turquoise", "paleturquoise", "aquamarine"]
ctp_list_b = ["powderblue", "skyblue", "lightsteelblue", "lightskyblue"]

#-------------------------------------------------------------------------------
def error_exit(txt1 = None, txt2 = None):
    """ Display error message and exit """

    if txt1:
        print(txt1, file = sys.stderr)
    if txt2:
        print(txt2, file = sys.stderr)
    sys.exit(1)

#-------------------------------------------------------------------------------
def generate_issues_colors(issues_dict, cl_list):
    """ Create a dictionary with unique colors for issues.
    issues_dict - dictionary containing issue-names (als keys) and issue-count.
            Example: {"w746":10, "i2707":3, "i793":15, "e838":3, ... }
    cl_list - a list of list of colors - every element of cl_list is a list of colors.
            Example: [  ["sandybrown", "darkorange", "orange", ...],
                        ["plum", "pink", "thistle", "orchid", ...],
                        ["powderblue", "skyblue", "lightsteelblue", ...]
                        ...
                     ]
    The function sorts all issues by the values - issues with bigger count are first,
    issues with smaller count are last. Every issue is assigned a unique color.
    The colors a selected one by one from every list: 
            cl_list[0][0], cl_list[1][0], cl_list[2][0], ..., cl_list[N][0],
            cl_list[0][1], cl_list[1][1], cl_list[2][1], ..., cl_list[N][1]
            ...
    The results are stored in a dictionary. 
            Example: { "i793":"sandybrown", "w746":"plum", "i2707":"powderblue", ...}
    """

    cl_list_cnt = len(cl_list)
    cl_list_idx = [0] * cl_list_cnt
    cl_list_act = 0

    issues_colors = {}

    # Sort the slices dictionary based on values
    issues_sorted_list = sorted(issues_dict.items(), key=lambda x: x[1], reverse = True)
    # This generates a sorted list of tuples: [(<slice_name>, <slice_val>),...]
    # Example: [("i793", 15), ("w746", 10), ("i2707", 3), ("e838", 3), ... ]

    for issue_t in issues_sorted_list:
        col = None
        col = cl_list[cl_list_act][cl_list_idx[cl_list_act]]
        cl_list_idx[cl_list_act] += 1
        if cl_list_idx[cl_list_act] >= len(cl_list[cl_list_act]):
            cl_list_idx[cl_list_act] = 0
        cl_list_act += 1
        if cl_list_act >= cl_list_cnt:
            cl_list_act = 0

        issues_colors[issue_t[0]] = col

    return issues_colors

#-------------------------------------------------------------------------------
def process_makefile_line(proc, gres_path_arg, working_dir_arg, makefile, module_ignore_list):
    """ Process one line (one makefile) from the file containing a list of makefiles
    """
    if not makefile:
        return

    # Path of the current analyzed Makefile, example:
    # C:\projects\pclp_juliet_a\test\testcases\CWE561_Dead_Code\
    #|<----- working directory ---->|<-- make relative path -->|
    #|<----------------- makefile path ----------------------->|
    makefile_path = os.path.dirname(makefile)
    print("make_path:", makefile_path)
    if not os.path.isdir(makefile_path):
        error_exit("Error: make_path not found:", makefile_path)

    # Local results path, example:
    # C:\projects\pclp_juliet_a\test\ig_gl_out\testcases\CWE561_Dead_Code\
    #|<-------------- gres_path ------------->|<-- make relative path -->|
    lres_path = os.path.relpath(makefile_path, working_dir_arg)
    lres_path = os.path.join(gres_path_arg, lres_path)
    print("lres_path:", lres_path)
    if not os.path.isdir(lres_path):
        error_exit("Error: local results directory not found:", lres_path)
    pclp_out_filename = os.path.join(lres_path, PCLP_OUT_FILE)

    # Name for the Interpreter results file
    int_filename = os.path.join(lres_path, INTR_OUT_FILE)

    # Check if PClint output file exists in local results directory
    if not os.path.isfile(pclp_out_filename):
        error_exit("Error: PClint output file not found:", pclp_out_filename)

    int_output = sys.stdout
    if int_filename:
        int_output = open(int_filename, "w", encoding='UTF-8')\

    res = proc.interpret(pclp_out_filename, makefile_path, int_output,\
                        module_ignore_list)
    #if not res:
    #    print(pr.results_modules)

    if int_output and int_output != sys.stdout:
        int_output.close()

    if res:
        error_exit("Error in file:" + res[0], \
                    "Error precessing line " + str(res[1]) + " > " + res[2])

#-------------------------------------------------------------------------------
def generate_plot_data(pclp_m, proc):
    """ Generate pie-charts. Every pie-chart is a tuple:
            (pie_title, slices_data_dict, slices_colors_dict)
        Where:
            slices_data_dict - a dictionary containing the names and values for all slices:
                {slice1_name : slice1_val, slice2_name : slice2_val2, ... }
            slices_colors_dict - a dictionary containing the color for every slice:
                {slice1_name : slice1_color, slice2_name : slice2_color, ...}
    """

    #---------------------------------------------------------------------------
    # Category results
    #---------------------------------------------------------------------------
    #print("bad: ", proc.results_all_bad)
    #print("good: ", proc.results_all_good)
    #print("other: ", proc.results_all_other)

    res_cat_dict = {}
    if proc.results_all_bad:
        res_cat_dict["true-positive"] = proc.results_all_bad
    if proc.results_all_good:
        res_cat_dict["false-positive"] = proc.results_all_good
    if proc.results_all_other:
        res_cat_dict["other-issues"] = proc.results_all_other

    res_cat_colors = {
        "true-positive" : "mediumaquamarine", 
        "false-positive" : "lightcoral", 
        "other-issues" : "sandybrown",
        "others" : "sandybrown"}

    generate_pie.gen_pie(("false-positive\nvs\ntrue-positive", res_cat_dict, res_cat_colors), "out_pie00.jpg")

    #---------------------------------------------------------------------------
    # All issues found
    #---------------------------------------------------------------------------
    issues_dict0 = {}
    for issue_nr, issue_cnt_list in proc.results_issues.items():
        #print(issue_nr, ":", issue_cnt_list)
        issues_dict0[pclp_m.get_message_name(issue_nr)] = issue_cnt_list[3]

    issues_colors0 = generate_issues_colors(issues_dict0, \
        [cfp_list_r, ctp_list_g, cfp_list_y, ctp_list_t, cfp_list_p, ctp_list_b])
    issues_colors0["others"] = "sandybrown"

    generate_pie.gen_pie(("all issues", issues_dict0, issues_colors0), "out_pie01.jpg")

    #---------------------------------------------------------------------------
    # False-positive issues found
    #---------------------------------------------------------------------------
    issues_dict1 = {}
    for issue_nr, issue_cnt_list in proc.results_issues.items():
        issues_dict1[pclp_m.get_message_name(issue_nr)] = issue_cnt_list[1]

    issues_colors1 = generate_issues_colors(issues_dict1, [cfp_list_r, cfp_list_y, cfp_list_p])
    issues_colors1["others"] = "sandybrown"

    generate_pie.gen_pie(("false-positive\nissues", issues_dict1, issues_colors1), "out_pie10.jpg")

    #---------------------------------------------------------------------------
    # True-positive issues found
    #---------------------------------------------------------------------------
    issues_dict2 = {}
    for issue_nr, issue_cnt_list in proc.results_issues.items():
        issues_dict2[pclp_m.get_message_name(issue_nr)] = issue_cnt_list[0]

    issues_colors2 = generate_issues_colors(issues_dict2, [ctp_list_g, ctp_list_t, ctp_list_b])
    issues_colors2["others"] = "sandybrown"

    generate_pie.gen_pie(("true-positive\nissues", issues_dict2, issues_colors2), "out_pie11.jpg")

    #---------------------------------------------------------------------------
    # Generate bars
    #---------------------------------------------------------------------------
    kwargs = dict()
    kwargs["limit_cnt"] = 16

    kwargs["title"] = "true-positive vs false-positive"
    kwargs["filename"] = "out_bar1.jpg"
    kwargs["bar1_color"] = issues_colors1
    kwargs["bar2_color"] = issues_colors2
    generate_bars.gen_bars(issues_dict1, issues_dict2, **kwargs)

    kwargs["title"] = "false-positive vs true-positive"
    kwargs['filename'] = "out_bar2.jpg"
    kwargs["bar1_color"] = issues_colors2
    kwargs["bar2_color"] = issues_colors1
    generate_bars.gen_bars(issues_dict2, issues_dict1, **kwargs)

#-------------------------------------------------------------------------------
if __name__ == '__main__':

    # Expect 1 mandatory argument: working_dir - working directory,
    # and 1 optional: file_ignore_list:
    # <--- 0 --->|<---- 1 ---->|<------ 2 ------->
    # reduced.py  <working_dir> <file_ignore_list>
    #
    # Working directory: directory containing all files/subdirectories to be analyzed:
    #
    # C:/pclp_juliet_a/test/
    # C:/pclp_juliet_a/test/testcases/CWE561_Dead_Code/Makefile
    # C:/pclp_juliet_a/test/testcases/CWE835_Infinite_Loop/Makefile
    #|<-working directory->|
    #
    # Global results: inside of the working directory the "global results" folder
    # is created - folder where all global and local results are stored:
    #
    # C:/pclp_juliet_a/test/ig_gl_out/
    #|<-working directory->|         |
    #|<------ global results ------->|
    #
    # Local results: inside of the "global results" folder, for every analyzed Makefile
    # a "local results" folder is created - folder where results for every Makefile is stored:
    #
    # C:/pclp_juliet_a/test/ig_gl_out/testcases/CWE561_Dead_Code/
    # C:/pclp_juliet_a/test/ig_gl_out/testcases/CWE835_Infinite_Loop/
    #|<-working directory->|         |
    #|<------ global results ------->|
    #|<---------------- local results ----------------------------...
    #
    # File Ignore List:
    # a text file where every line is module (filename and path) that must be ignored
    # by the processor. The filename and path can be absolute or relative to working directory.
    # Example:
    # C:/pclp_juliet_a/test/testcases/CWE561_Dead_Code/CWE561_Dead_Code__return_before_code_01.c
    # ./testcases/CWE561_Dead_Code/CWE561_Dead_Code__return_before_code_01.c

    if len(sys.argv) >= 2:

        script_path = sys.argv[0]
        working_dir = sys.argv[1]

        # Global results path
        gres_path = os.path.join(working_dir, GRES_FOLDER)
        gres_path = os.path.realpath(gres_path)
        print("gres_path:", gres_path)
        if not os.path.isdir(gres_path):
            error_exit("Error: global results directory not found:", gres_path)

        # Delete old global results file if exists
        gres_filename = os.path.join(gres_path, GRES_OUT_FILE)
        if os.path.isfile(gres_filename):
            os.remove(gres_filename)

        # List of makefiles
        makefiles_file = os.path.join(gres_path, MAKEFILES_NAME)
        if not os.path.isfile(makefiles_file):
            error_exit("Error: makefiles list not found:", makefiles_file)

        # Load list of modules to be ignored
        ignore_modules = ignore_list.IgnoreModuleList()
        if len(sys.argv) >= 3:
            if not ignore_modules.load(sys.argv[2], working_dir):
                error_exit("Error: cannot open list of modules to be ignored:", sys.argv[2])

            print("Module ignore list:")
            print("\n".join(ignore_modules.ignore_list))

        pr = processor.Processor()

        # For every makefile in the file containing the names of all found makefiles:
        with open(makefiles_file, encoding='UTF-8') as file:
            for line in file:
                process_makefile_line(pr, gres_path, working_dir, line.strip(),\
                                      ignore_modules.ignore_list)

        res_output = open(gres_filename, "a", encoding='UTF-8') if gres_filename else sys.stdout
        pr.dump_results(res_output)
        if res_output and res_output != sys.stdout:
            res_output.close()

        # Load PClint messages
        pclp_msg = pclp_messages.PclpMessages()
        err_str = pclp_msg.load("pclp_msg_list.txt")
        if err_str:
            error_exit("Error PClint messages", err_str)

        # Generate pie result images
        #print("Generating result charts")
        generate_plot_data(pclp_msg, pr)

    else:
        print("Incorrect invocation.", file = sys.stderr)
        print("Usage: reduced.py <working dir>", file = sys.stderr)
        sys.exit(1)
