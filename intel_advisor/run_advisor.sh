#!/usr/bin/env bash
# Collect data from version in current directory.
prun -np 1 advisor --collect=roofline --project-dir=. -- ./gol 1000 1000 1000 -o /dev/null

# Generate report from collected data in current directory.
prun -np 1 advisor --report=roofline --with-stack --project-dir=. --report-output=./roofline-withstack.html
