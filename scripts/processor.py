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
""" processor - module processes one makefile with the results generated
    by pclint.
"""
import os
import sys
from c_parser_src import CParser
from pclp_out_interpret_src import PclpInterpreter

#-------------------------------------------------------------------------------
class Processor:
    """ Processor - invokes the PClint output interpreter and for every
        module check the found issues in the corresponding C-files.
        The generated results are: 
        
        Results per module (results_modules):
        -------------------------------------
        The results are stored in a dictionary, where the key is the module name 
        (full path to the file), and the value is a set of 3 sub-dictionaries:
            sub-dictionary 0 : issue:count found in "bad"-functions (True-Positive Cases)
            sub-dictionary 1 : issue:count found in "good"-functions (False-Positive Cases)
            sub-dictionary 2 : issue:count found in the rest of the functions (neither bad nor good)
        The key in each sub-dictionary is the issue number, the value is the count how many times
        the issue was detected.
            
        { 
            "module_name1" : 
            (
                {issue_nr : count, issue_nr : count, ... }, <-- sub-dict0 = bad functions
                {issue_nr : count, issue_nr : count, ... }, <-- sub-dict1 = good functions
                {issue_nr : count, issue_nr : count, ... }, <-- sub-dict2 = other functions
            ),
            "module_name2" : 
            (
                {issue_nr : count, issue_nr : count, ... }, <-- sub-dict0 = bad functions
                {issue_nr : count, issue_nr : count, ... }, <-- sub-dict1 = good functions
                {issue_nr : count, issue_nr : count, ... }, <-- sub-dict2 = other functions
            ),
            ...
        }

        Results per issue (results_issues):
        -----------------------------------
        The results are stored in a dictionary, where the key is the issue-number, 
        and the value is a list of 3 integers:
            count of issue found in "bad"-functions (True-Positive Cases)
            count of issue found in "good"-functions (False-Positive Cases)
            count of issue found in the rest of the functions (neither bad nor good)
            count of issue found in all functions
        { 
            issue_nr1 : [count_bad, count_good, count_other, count_all],
            issue_nr2 : [count_bad, count_good, count_other, count_all],
            ...
        }

        Results all:
        ------------
        results_all_bad - count of all issues found in bad fucntions (True-Positive Cases)
        results_all_good - count of all issues found in good fucntions (False-Positive Cases)
        results_all_other - count of all issues found in other fucntions (neither bad nor good)
    """

    #---------------------------------------------------------------------------
    def __init__(self):
        self.results_modules = {}
        self.results_issues = {}
        self.results_all_good = 0
        self.results_all_bad = 0
        self.results_all_other = 0

    #---------------------------------------------------------------------------
    def add_issue(self, module_name, issue_number, func_name):
        """ Add an issue to the dictionary results """

        # Check if module not yet in results_modules, and add it
        if module_name not in self.results_modules:
            self.results_modules[module_name] = ({}, {}, {})

        # results_modules: get the list of 3 dictionaries (bad, good, other)
        module_res = self.results_modules[module_name]

        # Check if issue not yet in results_issues, and add it
        issue_res_list = self.results_issues.get(issue_number)
        if not issue_res_list:
            issue_res_list = [0, 0, 0, 0]
            self.results_issues[issue_number] = issue_res_list

        # what type of issue? (bad, good, other)
        func_name_lower = func_name.lower()
        if "bad" in func_name_lower:
            module_res_issues = module_res[0]
            issue_res_list[0] += 1
            self.results_all_bad += 1
        elif "good" in func_name_lower:
            module_res_issues = module_res[1]
            issue_res_list[1] += 1
            self.results_all_good += 1
        else:
            module_res_issues = module_res[2]
            issue_res_list[2] += 1
            self.results_all_other += 1
            
        issue_res_list[3] += 1

        # If issue already in the dictionary - increment its count
        # if not - add it to the dictionary
        if issue_number in module_res_issues:
            module_res_issues[issue_number] += 1
        else:
            module_res_issues[issue_number] = 1

    #---------------------------------------------------------------------------
    def interpret(self, pclint_out_file, makefile_path, output, module_ignore_list = None):
        """ Main processing method - processes a makefile together with generated
            pclint output file.

            pclint_out_file - output file generated by pclint to interpret
            makefile_path - the path to the makefile
            output - output file or stdout where intermediate results are written
            module_ignore_list - list of modules that must be ignored from processing
        """
        # Interpret the results of PClint
        pclp_interp = PclpInterpreter()
        res_error = pclp_interp.process_file(pclint_out_file)
        if res_error:
            return res_error

        # For every module invoke the C-parser
        c_parser = CParser()
        for m in pclp_interp.modules:

            print(80 * "-", file = output)

            # m[0]=module_name, m[1]=module_type, m[2]=module_issues[:]
            # module_issue =
            # (%l=line number, %t=message type (error, info, warning), %n=message number)
            module_name = m[0]
            module_issues = m[2]

            print("[PclpInterpreter]", file = output)
            print(module_name, m[1], file = output)
            for issue in module_issues:
                print(issue, file = output)

            module_name = os.path.join(makefile_path, module_name)
            module_name = os.path.realpath(module_name)

            # Check if module in ignore list
            if module_ignore_list:
                if module_name in module_ignore_list:
                    print("Module in ignore list:", module_name, file = output)
                    continue

            if module_issues:

                print("[CParser]", file = output)
                c_parser.process_file(module_name)
                c_parser.show_results(module_name, output)

                for issue in module_issues:

                    # issue[0]=line number
                    # issue[1]=message type (error, info, warning),
                    # issue[2]=message number
                    line_number = issue[0]
                    msg_number = issue[2]

                    func_name = c_parser.check_file_line(module_name, line_number)
                    if func_name:
                        self.add_issue(module_name, msg_number, func_name)
                        print("line:", line_number, "issue:", msg_number, \
                              "func:", func_name,  file = output)
        return None

    #---------------------------------------------------------------------------
    def dump_results(self, output):
        """ Dump (to a file or stdout) the results from processed files """

        for module_name, issues_list in self.results_modules.items():
            print(module_name, file = output)
            for issues in issues_list:
                print(issues, file = output)

#-------------------------------------------------------------------------------
if __name__ == '__main__':

    # Expect 3 arguments:
    # <-------- 0 -------->|<------ 1 ----->|<----- 2 ---->|<-- 3 -->|<-- 4 -->|
    # pclp_out_interpret.py <pclint_out.txt> <makefile_path> <res_out> <int_out>
    #
    # pclint_out.txt - output file generated by PClint - input file for the interpreter
    # makefile_path - working path, used by c_parser to create a dictionary of analized files
    # res_out - name of the output file, where module results are stored
    #           (if not provided sys.stdout is used)
    # int_out - name of the output file, where module intermediate results are stored
    #           (if not provided sys.stdout is used)

    if len(sys.argv) >= 3:

        path = sys.argv[0]

        pclint_out_file_arg = sys.argv[1]
        makefile_path_arg = sys.argv[2]
        res_output = open(sys.argv[3], "w", encoding='UTF-8') if len(sys.argv) > 3 else sys.stdout
        int_output = open(sys.argv[4], "w", encoding='UTF-8') if len(sys.argv) > 4 else sys.stdout

        processor = Processor()
        res = processor.interpret(pclint_out_file_arg, makefile_path_arg, int_output)
        if not res:
            processor.dump_results(res_output)

        if int_output and int_output != sys.stdout:
            int_output.close()
        if res_output and res_output != sys.stdout:
            res_output.close()

        if res:
            print("Error in file:", res[0], file = sys.stderr)
            print("Error precessing line (", res[1], "):", file = sys.stderr)
            print(res[2], file = sys.stderr)
            sys.exit(1)

    else:
        print("Incorrect interpreter invocation.", file = sys.stderr)
        print("Usage: pclp_out_interpret.py <pclint_out.txt> <makefile_path>", file = sys.stderr)
        sys.exit(1)
