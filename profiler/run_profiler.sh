#!/usr/bin/env bash

# Executes the profiler for a single version, given as first argument.
run_profiler() {
    echo -en "\nRunning tests for ${1:5:-1}.."

    # Compile the to be tested code.
    cd "$1" || exit 4
    make clean > /dev/null
    make gol > /dev/null 2> /dev/null
    cd ../..

    # Run the code and store output in results folder.
    if [ "$3" = "das" ]; then
        prun -np 1 "./$1gol" 1000 1000 1000 -t -s 42 -o /dev/null 2> "$2/${1:5:-1}.out" > /dev/null
    else
        "./$1gol" 1000 1000 1000 -t -s 42 -o /dev/null 2> "$2/${1:5:-1}.out" > /dev/null
    fi

    echo -e "\tDone."
}

# Main entry point of the script.
main() {
    # Check if arguments are passed.
    if [ $# -ne 2 ]; then
        echo "Usage: $0 [all | v<version>] [local | das]"
        exit 1
    fi

    # Move up one dir if profiler are ran from profiler folder.
    if [ "${PWD##*/}" = "profiler" ]; then
        cd ..
    fi

    # Make folder for storing the results.
    results="profiler/results/profiler_$1_$(date +%s)"
    mkdir -p "$results"

    # Run specific version, if specified.
    if [ ! "$1" = "all" ]; then
        # Check if folder with version number does exist.
        if ! compgen -G "apps/$1_*" > /dev/null; then
            echo "Version '$1' does not exist"
            exit 3
        fi

        vdir=$(find . -type d -name "$1*")
        run_profiler "${vdir:2}/" "$results" "$2"
    else
        # Run tests for all versions.
        for d in apps/*/; do
            run_profiler "$d" "$results" "$2"
        done
    fi
}

main "$@"
