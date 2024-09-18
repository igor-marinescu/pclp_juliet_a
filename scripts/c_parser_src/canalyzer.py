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
""" canalyzer - definition of main CAnallyzer class and extra AnalyzerException
    and CFunction classes.
"""
from .block_def import BlockDef
from .statements import StatementList
from .statements import StatementType

#-------------------------------------------------------------------------------
class AnalyzerException(Exception):
    """ Exception raised for errors in analyzing 
    """
    def __init__(self, line, col, text):
        self.line = line
        self.col = col
        self.text = "{" + str(line) + ", " + str(col) + "} " + text
        super().__init__(self.text)

#------------------------------------------------------------------------------
class CFunction:
    """ Class stores information about a Function: 
        name : function name
        pos_start : function's start position (line, column)
        pos_end : function's end position (line, column) 
    """

    def __init__(self, pos_start, pos_end, name):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.name = ""
        # if the name contains more than one word, use the last word
        words = name.split()
        if words:
            self.name = words[-1]

    def __str__(self):
        """ String representation of a Statement record 
        """
        txt = f'({self.pos_start[0]:3},{self.pos_start[1]:3}),'
        txt += f'({self.pos_end[0]:3},{self.pos_end[1]:3}),'
        txt += ' ' + self.name
        return txt

#------------------------------------------------------------------------------
class CAnalyzer:
    """ Class analyzes a C-file """

    def __init__(self):
        self.block_def = BlockDef()
        self.statements = StatementList(self.block_def)

    def analyze(self, file_name):
        """ Analyze a C-file and generate the list of statements 
        """
        line_idx = 0

        in_code = 0
        in_comment = 1
        in_text = 2
        in_define = 3
        in_where = in_code

        self.block_def.clear()
        self.statements.clear()

        with open(file_name, encoding='UTF-8') as file:
            for line in file:
                line_idx += 1
                line = line.rstrip()
                len_line = len(line)
                col_idx = 0

                # Remove whitespaces at the begining
                while col_idx < len_line:
                    ch = line[col_idx]
                    if ch in (' ', '\t'):
                        col_idx += 1
                    else:
                        break

                while col_idx < len_line:

                    ch = line[col_idx]
                    ch_next = None
                    col_idx += 1
                    if col_idx < len_line:
                        ch_next = line[col_idx]
                    pos = (line_idx, col_idx)

                    if in_where == in_comment:
                        if ch == '*' and ch_next == '/':
                            in_where = in_code
                            col_idx += 1

                    elif in_where == in_text:
                        if ch == '"':
                            in_where = in_code

                    elif in_where == in_define:
                        self.statements.add_ch(ch, pos)

                    elif in_where == in_code:

                        if ch == '"':
                            in_where = in_text

                        elif self.block_def.check_block_open(ch):
                            self.statements.end()
                            self.block_def.block_open(ch, pos)
                            self.statements.add_block_open(ch, pos)

                        elif self.block_def.check_block_close(ch):
                            self.statements.end()
                            if self.block_def.block_close(ch):
                                self.statements.add_block_close(ch, pos)
                            else:
                                raise AnalyzerException(line_idx, col_idx, "block open/close error")

                        elif ch == '/' and ch_next == '*':
                            in_where = in_comment
                            col_idx += 1

                        elif ch == '/' and ch_next == '/':
                            # The rest of the line is comment, ignore it
                            break

                        elif ch == '#':
                            self.statements.end()
                            in_where = in_define
                            self.statements.add_ch(ch, pos)

                        elif ch == ';':
                            self.statements.end()

                        else:
                            self.statements.add_ch(ch, pos)

                else:
                    # End of line
                    if in_where == in_define:
                        if ch != '\\':
                            self.statements.end()
                            in_where = in_code

        # End of file (there must be no opened blocks left)
        if self.block_def.stack:
            raise AnalyzerException(line_idx, col_idx, "block open/close error")

    def dump_statements(self, file_name, level):
        """ Write the list of detected statements to file """
        with open(file_name, 'w', encoding='UTF-8') as file:
            for rec in self.statements.list:
                if rec.level <= level:
                    file.write(str(rec) + "\n")

    def extract_functions(self):
        """ Extract functions info from the list of statements.
            The C functions are allway defined at level 0.
            A C function has always the format: Function(...){...} """
        func_list = []
        list_level = self.statements.get_list_level(0)
        list_len = len(list_level)
        list_idx = 0
        while list_idx < list_len:
            rec = list_level[list_idx]
            if rec.stype != StatementType.code:
                list_idx += 1
                continue
            if (list_idx + 4) > list_len:
                break
            list_idx += 1
            rec1 = list_level[list_idx]
            if not rec1 or \
                rec1.stype != StatementType.block_open or rec1.text != '(':
                continue
            list_idx += 1
            rec2 = list_level[list_idx]
            if not rec2 or \
                rec2.stype != StatementType.block_close or rec2.text != ')':
                continue
            list_idx += 1
            rec3 = list_level[list_idx]
            if not rec3 or \
                rec3.stype != StatementType.block_open or rec3.text != '{':
                continue
            list_idx += 1
            rec4 = list_level[list_idx]
            if not rec4 or \
                rec4.stype != StatementType.block_close or rec4.text != '}':
                continue
            func_list.append(CFunction(rec.pos_start, rec4.pos_end, rec.text))
            list_idx += 1
        return func_list
