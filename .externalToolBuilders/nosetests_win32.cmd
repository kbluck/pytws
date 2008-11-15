:: Command script to invoke Nose on Win32. Unfortunately necessary due to
:: Eclipse's refusal in external tool builders to just issue a shell
:: command using the sys exe path.
:: $Id$
@echo off
python run-tests.py %1 %2 %3 %4 %5 %6 %7 %8 %9