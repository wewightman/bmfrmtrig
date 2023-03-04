#!/bin/bash
gcc test_engines.c -o test -lm
./test
rm test
