#!/usr/bin/env bash

# Executes scaling experiments for a single version, given as first argument.
run_scaling() {
    echo -e "\nRunning tests for ${1:5:-1}"

    # Compile the to be tested code.
    cd "$1" || exit 4
    make clean > /dev/null
    make gol > /dev/null 2> /dev/null
    cd ../..

    # Run the code with different number of threads through global variable.
    for nthreads in {1,2,4,8,12,15,16,24,32}; do
        export OMP_NUM_THREADS=$nthreads

        # Run the code and store output in results folder.
        "$3./$1gol" 1000 1000 1000 -t -s 42 -o /dev/null 2> "$2/${nthreads}_threads.out" > /dev/null
        echo -e "\tDone."
    done
}

# Main entry point of the script.
main() {
    # Check if arguments are passed.
    if [ $# -eq 0 ]; then
        echo "Usage: $0 v<version> [local | das]"
        exit 1
    fi

    # Move up one dir if profiler are ran from profiler folder.
    if [ "${PWD##*/}" = "profiler" ]; then
        cd ..
    fi

    # Make folder for storing the results.
    results="profiler/results/scaling_$1"
    mkdir -p "$results"

    # Add a prefix for running ./gol if executed on DAS.
    if [ "$2" = "das" ]; then
        cmdPrefix="prun -np 1 "
    else
        cmdPrefix=""
    fi

    # Check if folder with version number does exist.
    if ! compgen -G "apps/$1_*" > /dev/null; then
        echo "Version '$1' does not exist"
        exit 3
    fi

    vdir=$(find . -type d -name "$1*")
    run_scaling "${vdir:2}/" "$results" "$cmdPrefix"
}

main "$@"
