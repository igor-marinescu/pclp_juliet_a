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
""" pclp_messages - module loads and holds all messages available in pclint.
"""
import os
import sys

# PClint message types
PCLP_MSG_TYPE_UNKNOWN = 0
PCLP_MSG_TYPE_ERROR = 1
PCLP_MSG_TYPE_WARN = 2
PCLP_MSG_TYPE_INFO = 3
PCLP_MSG_TYPE_SUPP = 4
PCLP_MSG_TYPE_NOTE = 5

PCLP_MSG_TYPE_PREFIX = {PCLP_MSG_TYPE_UNKNOWN : '?', \
                        PCLP_MSG_TYPE_ERROR : 'e', \
                        PCLP_MSG_TYPE_WARN : 'w', \
                        PCLP_MSG_TYPE_INFO : 'i', \
                        PCLP_MSG_TYPE_SUPP : 's', \
                        PCLP_MSG_TYPE_NOTE : 'n' }

# PClint message type colors
PCLP_MSG_ERROR_COLORS = ["red", "firebrick", "maroon", "crimson", "darkred"]
PCLP_MSG_WARN_COLORS = ["lightcoral", "indianred", "salmon", "tomato", "coral"]
PCLP_MSG_INFO_COLORS = ["coral", "salmon", "darksalmon", "lightsalmon", "sandybrown"]
PCLP_MSG_SUPP_COLORS = ["bisque", "navajowhite", "peachpuff", "moccasin", "wheat"]
PCLP_MSG_NOTE_COLORS = ["paleturquoise", "powderblue", "lightblue", "skyblue", "lightskyblue"]

PCLP_MSG_COLOR_MAP = {PCLP_MSG_TYPE_UNKNOWN : ["red"], \
                      PCLP_MSG_TYPE_ERROR : PCLP_MSG_ERROR_COLORS, \
                      PCLP_MSG_TYPE_WARN : PCLP_MSG_WARN_COLORS, \
                      PCLP_MSG_TYPE_INFO : PCLP_MSG_INFO_COLORS, \
                      PCLP_MSG_TYPE_SUPP : PCLP_MSG_SUPP_COLORS, \
                      PCLP_MSG_TYPE_NOTE : PCLP_MSG_NOTE_COLORS }

#-------------------------------------------------------------------------------
class PclpMessages:
    """ PclpMessages - loads and holds all messages available in PClint (and 
        could be generated by PClint). The class loads all the messages from 
        a file which is generated by PClint using the following command:

            pclp64.exe -dump_message_list=pclp_msg_list.txt

        -dump_message_list will case PClint to write out its list of messages 
        to the provided file. For example, -dump_message_list(pclp_msg_list.txt) 
        will write the message information for all messages supported by PClint 
        to a file named pclp_msg_list.txt. This file contains one line per message 
        with three fields, delimited by tabs as shown below:

            25 error character constant too long for its type
            29 error duplicated type-specifier, '__detail__'
            31 error redefinition of symbol __symbol__
            32 error field size (member __symbol__) should not be zero
            ...
    """

    #---------------------------------------------------------------------------
    def __init__(self):
        self.msg_type = {}
        self.msg_text = {}

    #---------------------------------------------------------------------------
    def load(self, filename):
        """ Load the complete list of PClint from a file generated by PClint
            using -dump_message_list command.
            filename - file containing the list of PClint messages (one message per line)
            Returns None in case of success or error string in case of error
        """

        if not os.path.isfile(filename):
            return "Error: file not found: " + filename

        msg_type_dict = {"error" : PCLP_MSG_TYPE_ERROR,\
                         "warning" : PCLP_MSG_TYPE_WARN, \
                         "info" : PCLP_MSG_TYPE_INFO, \
                         "supplemental" : PCLP_MSG_TYPE_SUPP, \
                         "note" : PCLP_MSG_TYPE_NOTE }

        error_str = None

        # For every line from the file containing all the PClint message
        # extract: <message_number>'\t'<message_type>'\t'<message_text>
        with open(filename, encoding='UTF-8') as file:
            line_idx = 0
            for line in file:
                line = line.strip()
                if not line:
                    continue
                values = line.split("\t")
                if len(values) < 3:
                    error_str = "Error line: " + str(line_idx) + " '" + line + "'"
                    break
                try:
                    msg_nr = int(values[0])
                except ValueError:
                    error_str = "Error line: " + str(line_idx) + " '" + line + "'"
                    break
                msg_type = msg_type_dict.get(values[1])
                if not msg_type:
                    error_str = "Error line: " + str(line_idx) + " '" + line + "'"
                    break
                self.msg_type[msg_nr] = msg_type
                self.msg_text[msg_nr] = values[2]
                line_idx += 1
        return error_str

    #---------------------------------------------------------------------------
    def get_message_color(self, msg_nr):
        """
            Return a message color based on message type.
        """
        msg_type = self.msg_type.get(msg_nr)
        if not msg_type:
            return "red"
        color_list = PCLP_MSG_COLOR_MAP[msg_type]
        color_idx = msg_nr % len(color_list)
        return color_list[color_idx]

    #---------------------------------------------------------------------------
    def get_message_name(self, msg_nr):
        """
            Return a message name based on message number and type.
            Example: 
            - msg_nr=25, defined as "25 error character constant...", has name "E25"
            - msg_nr=644, defined as "644 warning potentially...", has name "W644"
        """
        msg_type = self.msg_type.get(msg_nr)
        if not msg_type:
            return None
        return PCLP_MSG_TYPE_PREFIX[msg_type] + str(msg_nr)

#-------------------------------------------------------------------------------
if __name__ == '__main__':

    if len(sys.argv) >= 2:

        script_path = sys.argv[0]
        pclp_msg_file = sys.argv[1]

        pclp_msg = PclpMessages()
        err_str = pclp_msg.load(pclp_msg_file)
        if err_str:
            print(err_str)
        else:
            print("Success:", len(pclp_msg.msg_type), " messages loaded")
    else:
        print("Usage: python pclp_messages.py <pclp_msg_file.txt>")
