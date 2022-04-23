#!/usr/bin/env bash

run_tests() {
    cd $1
    make gol-fixed 1> /dev/null

    if ! ./gol-fixed 42 22 500 1 1 2> /dev/null | diff /dev/stdin ../../reference_output/fixed-42-22-500.ref ; then
        echo "Error: $1 does not comply with reference_output! (42 22 500)"
        exit -1
    fi

    if ! ./gol-fixed 100 100 1200 1 1 2> /dev/null | diff /dev/stdin ../../reference_output/fixed-100-100-1200.ref ; then
        echo "Error: $1 does not comply with reference_output! (100 100 1200)"
        exit -1
    fi
}

VERSIONS=$(find apps/* -type d)
for V in $VERSIONS; do
  run_tests $V
done
