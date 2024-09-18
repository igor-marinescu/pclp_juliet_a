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
""" statements - definition of classes uses to detect statements inside of a
    C-file.
"""

#------------------------------------------------------------------------------
class StatementType:
    """ Statement type 
    """
    none = 0
    code = 1
    define = 2
    block_open = 3
    block_close = 4

#------------------------------------------------------------------------------
class StatementRec:
    """ Class implements a Statemenet record: contains information about a statement:
        stype : statemenet type (stype_...)
        level : statement incapsulation/block level
        pos_start : statement's start position (line, column) 
        pos_end : statement's end position (line, column) 
        text : statement's text 
    """

    def __init__(self, ch, pos_start, pos_end):
        self.stype = StatementType.none
        self.level = 0
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.text = ch

    def __str__(self):
        """ String representation of a Statement record 
        """
        txt = f'{self.stype:1},{self.level:1},'
        txt += f'({self.pos_start[0]:3},{self.pos_start[1]:3}),'
        txt += f'({self.pos_end[0]:3},{self.pos_end[1]:3}),'
        txt += ' ' * (4 * self.level)
        txt += self.text
        return txt

#------------------------------------------------------------------------------
class StatementList:
    """ Class implements a list of statements 
    """

    def __init__(self, block_def):
        self.list = []
        self.block = block_def
        self.rec = None

    def clear(self):
        """ Clear the list of statements
        """
        self.list.clear()
        self.rec = None

    def add_ch(self, ch, pos):
        """ Add ch symbol to the current statement
        """
        if not self.rec:
            if ch not in (' ', '\t'):
                self.rec = StatementRec(ch, pos, pos)
        else:
            self.rec.text += ch
            self.rec.pos_end = pos

    def end(self):
        """ End of statement: add current statement (if not empty) to list
        """
        if self.rec and self.rec.text:
            self.rec.level = self.block.get_level()
            if self.rec.text[0] == '#':
                self.rec.stype = StatementType.define
            else:
                self.rec.stype = StatementType.code
            self.list.append(self.rec)
        self.rec = None

    def add_block_open(self, ch, pos_start):
        """ Add a block-open statement to the list of statements
        """
        if self.rec:
            self.end()
        block_st = StatementRec(ch, pos_start, pos_start)
        block_st.level = self.block.get_level() - 1
        block_st.stype = StatementType.block_open
        self.list.append(block_st)

    def add_block_close(self, ch, pos_end):
        """ Add a block-close statement to the list of statements
        """
        if self.rec:
            self.end()
        block_st = StatementRec(ch, pos_end, pos_end)
        block_st.level = self.block.get_level()
        block_st.stype = StatementType.block_close
        self.list.append(block_st)

    def get_list_level(self, level):
        """ Get a list of statements which are <= level
        """
        list_level = []
        for rec in self.list:
            if rec.level <= level:
                list_level.append(rec)
        return list_level
