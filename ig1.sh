#!/bin/bash

#-------------------------------------------------------------------------------
# Configuration
#-------------------------------------------------------------------------------

# Name of the PClint command
PCLP_NAME="pclp64_linux"

#--- Global for working directory (all makefiles) ------------------------------

# Global results folder
GRES_FOLDER="ig_gl_out"
# Name of generated Compile Configuration
PCLP_CO_NAME="./$GRES_FOLDER/ig_co-gcc"
# File where all found Makefiles are stored
MAKEFILES_NAME="./$GRES_FOLDER/ig_makefiles.txt"
# File where global results (for all makefiles) are stored
GRES_OUT_FILE="./$GRES_FOLDER/ig_global_results.txt"

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
INTR_OUT_FILE="ig_interpret_out.txt"

#-------------------------------------------------------------------------------
# Script name and path
#-------------------------------------------------------------------------------
SCRIPT_NAME=$(realpath "$0")
SCRIPT_PATH=$(dirname "$SCRIPT_NAME")

#-------------------------------------------------------------------------------
# args.lnt exists? (extra options for PCLint)
#-------------------------------------------------------------------------------
if [[ -f "$SCRIPT_PATH/args.lnt" ]]; then
    # If "$SCRIPT_PATH/args.lnt" exists (extra options for PCLint), pass it as argument while invoking PCLint
    echo "[INFO]" PCLint extra options: "$SCRIPT_PATH/args.lnt"
    PCLP_ARGS="$SCRIPT_PATH/args.lnt"
fi

#-------------------------------------------------------------------------------
# Working directory and global results folder
#-------------------------------------------------------------------------------
# Argument 1 (working directory) passed? 
if [[ "$#" -gt 0 ]]; then
    cd "$1"
    if [[ $? -ne 0 ]]; then
        echo "[ERROR] Invalid working directory"
        exit 1
    fi
fi

WORKING_DIR=$(pwd)
echo "[INFO] WORKING_DIR=$WORKING_DIR"

# Delete old global results (if exists)
if [[ -d "$GRES_FOLDER" ]]; then
    rm -rf "$GRES_FOLDER"
fi
mkdir "$GRES_FOLDER"
if [[ $? -ne 0 ]]; then
    echo "[ERROR] Cannot create global output folder: $GRES_FOLDER"
    exit 1
fi

#-------------------------------------------------------------------------------
# Find the gcc Compiler
#-------------------------------------------------------------------------------
GCC_EXE=$(which gcc)
if [[ $? -eq 0 ]]; then
    echo "[INFO] GCC_EXE=$GCC_EXE"
else
    echo "[ERROR] gcc Compiler not found"
    exit 1
fi

#-------------------------------------------------------------------------------
# Find the PCLint-path
#-------------------------------------------------------------------------------
PCLP_EXE=$(which "$PCLP_NAME")
if [[ $? -eq 0 ]]; then
    PCLP_PATH=$(dirname "$PCLP_EXE")
    echo "[INFO] PCLP_PATH=$PCLP_PATH"
else
    echo "[ERROR] PCLint ($PCLP_NAME) not found. Add PCLint to PATH."
    exit 1
fi

#-------------------------------------------------------------------------------
# Check if imposter exists
#-------------------------------------------------------------------------------
export CC="$PCLP_PATH/config/imposter"
export CPP="$PCLP_PATH/config/imposter"

if [[ ! -f "$CC" ]]; then
   echo "[ERROR] Imposter missing ($CC)"
   exit 1
fi

#-------------------------------------------------------------------------------
# Generate Compiler Configuration
#-------------------------------------------------------------------------------
echo "[INFO] Generate compiler configuration"

PCLP_CO_LNT="$WORKING_DIR/$PCLP_CO_NAME.lnt"
PCLP_CO_H="$WORKING_DIR/$PCLP_CO_NAME.h"

python3 "$PCLP_PATH/config/pclp_config.py" \
            --compiler=gcc \
            --compiler-bin="$GCC_EXE" \
            --config-output-lnt-file="$PCLP_CO_LNT" \
            --config-output-header-file="$PCLP_CO_H" \
            --generate-compiler-config

if [[ ! -f "$PCLP_CO_LNT" || ! -f "$PCLP_CO_H" ]]; then
   echo "[ERROR] Error generating compiler configuration"
   exit 1
fi

#-------------------------------------------------------------------------------
# Find all Makefiles in all subdirectories (store in ig_makfiles.txt)
#-------------------------------------------------------------------------------
find "$WORKING_DIR" -name "Makefile" > "$MAKEFILES_NAME"

MAKEFILES_COUNT=$(wc -l < "$MAKEFILES_NAME")
if [[ $MAKEFILES_COUNT -le 0 ]]; then
    echo "[INFO] No Makefiles found, nothing to do"
    exit 0
fi

#-------------------------------------------------------------------------------
# For every directory that contains a Makefile:
#   - build the code (invoke make -e) with imposter
#   - generate project config using data from imposter (invoke pclp_config.py)
#   - analyze the code (invoke $PCLP_EXE)
#-------------------------------------------------------------------------------
MAKEFILE_IDX=0
while read make_file; do

    MAKEFILE_IDX=$((MAKEFILE_IDX + 1))
    printf "[%3d/%-3d] %s\n" $MAKEFILE_IDX $MAKEFILES_COUNT $make_file
    MAKE_DIR=$(dirname "$make_file")
    cd "$MAKE_DIR"

    # Get the relative path between Makefile and working directory
    # and create a respective directory in the results folder (local results folder)
    RELATIVE_PATH=$(realpath -s --relative-to="$WORKING_DIR" . )
    LRES_FOLDER="$WORKING_DIR/$GRES_FOLDER/$RELATIVE_PATH"
    mkdir -p "$LRES_FOLDER"

    if [[ $? -ne 0 ]]; then
        echo "[ERROR] Cannot create local results folder: $LRES_FOLDER"
        exit 1
    fi

    export IMPOSTER_LOG="$LRES_FOLDER/$IMPO_OUT_FILE"
    make -e > "$LRES_FOLDER/$MAKE_OUT_FILE"

    # Generate project configuration
    python3 "$PCLP_PATH/config/pclp_config.py" \
            --compiler=gcc \
            --imposter-file="$LRES_FOLDER/$IMPO_OUT_FILE" \
            --config-output-lnt-file="$LRES_FOLDER/$PCLP_PRJ_FILE" \
            --generate-project-config

    # Analyze project, default options:
    # -b - suppress banner output
    # -"width(256)" - sets the maximum output width and indentation level for continuations
    # -"format=%f, %l, %t, %n" - sets the message format for height 3 or less
    # -h1 - adjusts message height options
    ${PCLP_NAME} -b -"width(256)" -"format=%f, %l, %t, %n" -h1 "$PCLP_ARGS" "$PCLP_CO_LNT" "$LRES_FOLDER/$PCLP_PRJ_FILE" > "$LRES_FOLDER/$PCLP_OUT_FILE"

    if [[ $? -ne 0 ]]; then
        echo "[ERROR] $PCLP_NAME finished with error:"
        cat "$LRES_FOLDER/$PCLP_OUT_FILE"
        exit 1
    fi

    if [[ ! -f "$LRES_FOLDER/$PCLP_OUT_FILE" ]]; then
        echo "[ERROR] Error invoking $PCLP_NAME, the output file not generated"
        exit 1
    fi

    # Interpret the output generated by PC-lint
    #python3 "$SCRIPT_PATH/scripts/processor.py" "$LRES_FOLDER/$PCLP_OUT_FILE" "$MAKE_DIR" "$WORKING_DIR/$GRES_OUT_FILE" "$LRES_FOLDER/$INTR_OUT_FILE"

    #if [[ $? -ne 0 ]]; then
    #    echo "[ERROR] pclp_out_interpret finished with error"
    #    exit 1
    #fi

done < "$WORKING_DIR/$MAKEFILES_NAME"
