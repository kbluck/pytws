#! /bin/bash
#
# Shell script to invoke Nose on Linux. Unfortunately necessary due to
# Eclipse's refusal in external tool builders to just issue a shell 
# command using the sys exe path.
#
# $Id$

python run-tests.py $@