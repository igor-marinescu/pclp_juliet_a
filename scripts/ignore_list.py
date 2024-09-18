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
""" ignore_list - implements IgnoreModuleList Class
"""
import os

#-------------------------------------------------------------------------------
class IgnoreModuleList:
    """ Class loads (from file) and holds the list of modules to be
        ignored during processing.
    """

    #---------------------------------------------------------------------------
    def __init__(self):
        self.ignore_list = []

    #---------------------------------------------------------------------------
    def add_dir(self, dir_path):
        ''' 
        Walk through all files and subdirectories, find all *.c files and add them 
        to the list of ignored modules.
        '''
        # For each directory in the tree rooted at directory top (including top itself),
        # it yields a 3-tuple (dirpath, dirnames, filenames).
        walk_res = os.walk(dir_path, topdown=False)
        for entry in walk_res:
            # Iterate through all filenames
            for filename in entry[2]:
                if filename.endswith(".c") or filename.endswith(".C"):
                    filename = os.path.join(entry[0], filename)
                    filename = os.path.realpath(filename)
                    if os.path.isfile(filename) and filename not in self.ignore_list:
                        self.ignore_list.append(filename)

    #---------------------------------------------------------------------------
    def add(self, filename, working_dir):
        '''
        Check the filename if is a valid file, convert it to absolute path and
        add to the ignore list.
        '''
        if not filename or filename.startswith("#"):
            return True

        # Relative path? Convert to absolute
        if not os.path.isabs(filename):
            # Relative to the script?
            if os.path.exists(filename):
                pass
            # Relative to the working directory
            else:
                filename = os.path.join(working_dir, filename)
                if not os.path.exists(filename):
                    return False
            filename = os.path.realpath(filename)

        # Line is a directory?
        if os.path.isdir(filename):
            self.add_dir(filename)
            return True

        # Line is file?
        if os.path.isfile(filename) and filename not in self.ignore_list:
            self.ignore_list.append(filename)
            return True

        return False

    #---------------------------------------------------------------------------
    def load(self, filename, working_dir_arg):
        '''
        Load list of modules to be ignored.
        filename - the name of the text file containing all modules to be ignored.
        '''
        if not os.path.isfile(filename):
            return False

        with open(filename, encoding='UTF-8') as file_ignore_list:
            for file_to_ignore in file_ignore_list:
                if not self.add(file_to_ignore.strip(), working_dir_arg):
                    #print("Error: cannot add module to ignore list:", file_to_ignore.strip())
                    pass

        return True
