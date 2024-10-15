#!/bin/bash

#-------------------------------------------------------------------------------
# Configuration
#-------------------------------------------------------------------------------

# Name of the PClint command
PCLP_NAME="pclp64_linux"

#--- Global for working directory (all makefiles) ------------------------------

# Global results folder
GRES_FOLDER="pclp_a_out"
# File where all found Makefiles are stored
MAKEFILES_NAME="makefiles_win.txt"
# File where global results (for all makefiles) are stored
GRES_OUT_NAME="global_results.txt"
# Filename of generated infograph
GRES_OUT_GRAPH="infograph_out.jpg"

#--- Local (for every makefile) ------------------------------------------------

# Generated Project Configuration file:
PCLP_PRJ_FILE="ig_project.lnt"
# PClint output file:
PCLP_OUT_FILE="ig_pclint_out.txt"
# Imposter output file:
IMPO_OUT_FILE="ig_imposter_out.txt"
# File where output from make is stored
MAKE_OUT_FILE="ig_make_out.txt"
# File where output from interpreter is stored
INTR_OUT_FILE="interpret_out.txt"
