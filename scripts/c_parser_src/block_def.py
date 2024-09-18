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
""" block_def - definition of the BlockDef class.
"""

#-------------------------------------------------------------------------------
class BlockDef:
    """ Class tracks the opening and closing of blocks. 
        Detects if the blocks are correctly closed. 
        And stores information about encapsulation level and block start position. 
    """

    #---------------------------------------------------------------------------
    def __init__(self):
        self.stack = []
        self.stack_pos = []
        self.ch_open_list = ['{', '(', '[']
        self.ch_close_list = ['}', ')', ']']
        self.in_block = None

    #---------------------------------------------------------------------------
    def clear(self):
        """ Clear all blocks information 
        """
        self.stack.clear()
        self.stack_pos.clear()
        self.in_block = None

    #---------------------------------------------------------------------------
    def check_block_open(self, ch):
        """ Check if ch is a valid block-open symbol 
        """
        return ch in self.ch_open_list

    #---------------------------------------------------------------------------
    def block_open(self, ch, pos):
        """ New block opens, append it to the stack of blocks and remember it in in_block 
        """
        self.stack.append(ch)
        self.stack_pos.append(pos)
        self.in_block = ch

    #---------------------------------------------------------------------------
    def check_block_close(self, ch):
        """ Check if ch is a valid block-close symbol 
        """
        return ch in self.ch_close_list

    #---------------------------------------------------------------------------
    def block_close(self, ch):
        """ Block closes, check the stack if the block was opened 
            with the corresponding ch 
        """
        if self.stack:
            ch_open = self.stack.pop()

            # We leave the old block, refresh the in_block variable to point to
            # most recent block from stack
            if self.stack:
                self.in_block = self.stack[len(self.stack) - 1]
            else:
                self.in_block = None

            # Returns statement index of the corresponding opening block
            # (if the block was opened with the same (coresponding) symbol)
            if self.ch_close_list.index(ch) == self.ch_open_list.index(ch_open):
                return True

        # Error, nothing to close, there are no more opened blocks in stack
        return None

    #---------------------------------------------------------------------------
    def get_opposite_ch(self, ch):
        """ Get block's opposite symbol. For block-close symbol 
            return block_open symbol and viceversa. 
            Example for '{' return '}', for '}' return '{'. 
        """
        if ch in self.ch_open_list:
            idx = self.ch_open_list.index(ch)
            return self.ch_close_list[idx]
        if ch in self.ch_close_list:
            idx = self.ch_close_list.index(ch)
            return self.ch_open_list[idx]
        return None

    #---------------------------------------------------------------------------
    def get_level(self):
        """ Return the (incapsulation) level of the current block
        """
        return len(self.stack)
