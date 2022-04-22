#!/usr/bin/env bash

# Check if arguments are passed.
if [ $# -eq 0 ]; then
    echo "Usage: $0 <version_number> <make_type>"
    exit 1
fi

# Check if folder with version number does exist.
if ! compgen -G "apps/$1*" > /dev/null; then
    echo "Version '$1' does not exist"
    exit 2
else
    VDIR=$(find . -type d -name "$1*")
fi

# Go to right directory and clean folder.
cd "$VDIR" || (echo "Error: cd into VDIR failed.." && exit 3)
make clean
rm -rf annotations.advidb2 config/ e000/ reference.advixeproj report.html

# Compile with right make type.
case "$2" in
    # Compile with video output.
    "video")
        make gol-video
        GOLNAME=gol-video
        ;;
    # Compile without video output by default.
    *)
        make gol-plain
        GOLNAME=gol-plain
        ;;
esac

# Collect data and create report with Intel Advisor.
prun -np 1 advisor --collect=roofline --project-dir=. -- ./$GOLNAME 1920 1080 500 0 0
advisor --report=roofline --data-type=int --project-dir=. --report-output=./report.html
