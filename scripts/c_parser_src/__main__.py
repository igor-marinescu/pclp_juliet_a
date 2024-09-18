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
    __main__ function
"""
import c_parser_src

#-------------------------------------------------------------------------------
if __name__ == '__main__':
    # Main function called when the module is invoked direct from command line:
    #
    #   > cd "scripts"
    #   > python -m pclp_out_interpret_src <pclp_out_file>

    print("__main__")
    c_parser_src.main()
