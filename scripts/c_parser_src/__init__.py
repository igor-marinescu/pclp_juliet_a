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
""" c_parser_src - parses C-files and extracts info about defined functions.
    __init__ function
"""
import sys
from .c_parser import CParser

#-------------------------------------------------------------------------------
def main():
    """ Init function called when the module is invoked direct from command line:

        > cd "scripts"
        > python3 -m c_parser_src <path_to_analyse>
    """
    print('c_parser_src::__init__.main()')

    if len(sys.argv) > 1:
        parser = CParser()
        parser.process_path(sys.argv[1])
        parser.show_results(None, sys.stdout)
    else:
        print("Nothing to process.")
        print("Specify as argument the path to files to be analyzed.")

    retcode = 0
    sys.exit(retcode)
