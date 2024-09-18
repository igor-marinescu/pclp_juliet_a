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
""" cparser - definition of CParser class
"""
import os
from .canalyzer import CAnalyzer

#-------------------------------------------------------------------------------
class CParser:
    """ Main class for parsing a C-file or many C-files inside of a directory.
        CAnalyzer is invoked for every C-file to be parsed. 
    """

    def __init__(self):
        self.c_analyzed_dict = {}

    def clear(self):
        """ Clear all previous analyzed data, results 
        """
        self.c_analyzed_dict.clear()

    def analyze(self, filename):
        """ Analize a given C file and extract the list of functions.
            filename - the name of the C file to analyze (without path)
            path - full path to the file filename 
        """
        # If file already processed, don't process it again
        if filename in self.c_analyzed_dict:
            return
        # if not, process it now
        analyzer = CAnalyzer()
        analyzer.analyze(filename)
        #analyzer.dump_statements(filename + "_out.txt", 0)
        func_list = analyzer.extract_functions()
        # Add analzed results to dictionary
        if func_list:
            self.c_analyzed_dict[filename] = func_list

    def show_results(self, filename, output):
        """ Display (or write to file) the results of parsing the C-files:
            filename - if not None: display only for a specific file
            output - sys.stdout for display (or a file descriptor)
        """
        # Display results for a specific filename
        if filename:
            if filename in self.c_analyzed_dict:
                print(filename, file = output)
                func_list = self.c_analyzed_dict[filename]
                for func in func_list:
                    print(func, file = output)
        # Display results for all filenames
        else:
            for f_name, func_list in self.c_analyzed_dict.items():
                print(f_name, file = output)
                for func in func_list:
                    print(func, file = output)

    def process_file(self, filename):
        """ Processor main function. 
            filename - file to be analyzed 
        """
        if filename.endswith(".c") or filename.endswith(".C"):
            self.analyze(filename)

    def process_path(self, path):
        """ Processor main function. 
            path - path to the files to be analyzed 
        """
        # For each directory in the tree rooted at directory top (including top itself),
        # it yields a 3-tuple (dirpath, dirnames, filenames).
        walk_res = os.walk(path, topdown=False)
        for entry in walk_res:
            # Iterate through all filenames
            for filename in entry[2]:
                if filename.endswith(".c") or filename.endswith(".C"):
                    filename = os.path.join(entry[0], filename)
                    filename = os.path.realpath(filename)
                    self.analyze(filename)

    def check_file_line(self, filename, line_idx):
        """ Return the function name at line_idx 
            or None in case there is no function at that location 
        """
        if filename not in self.c_analyzed_dict:
            return None
        func_list = self.c_analyzed_dict[filename]
        if func_list:
            for func in func_list:
                if (line_idx >= func.pos_start[0]) and (line_idx <= func.pos_end[0]):
                    return func.name
        return None
