#!/usr/bin/env bash

# Executes the profiler for a single version, given as first argument.
run_profiler() {
    echo -e "\nRunning tests for ${1:5:-1}.."

    # Compile the to be tested code.
    cd "$1" || exit 4
    make clean > /dev/null
    make gol > /dev/null 2> /dev/null
    cd ../..

    # Include number of threads to arguments if main version is 6 or higher, but not 7.0.
    (( mainVersion = ${1:6:1} ))

    if [ "${1:6:3}" != "7.0" ] && [ "$mainVersion" -ge 6 ]; then
        threadArgs="-t 8"
    else
        threadArgs=""
    fi

    # Perform one dry run.
    echo -en "\tExecuting dry run.."

    if [ "$3" = "das" ]; then
        rm -f "/var/scratch/$USER/profiler.gif"
        prun -reserve "$4" -np 1 "./$1gol" 1000 1000 1000 -s 42 -o "/var/scratch/$USER/profiler.gif" $threadArgs &> /dev/null
    else
        rm -f profiler.gif
        "./$1gol" 1000 1000 1000 -s 42 -o profiler.gif $threadArgs &> /dev/null
    fi

    echo -e "\tDone."

    # Perform 5 tests for each version.
    for t in {1..5}; do
        echo -en "\tExecuting run $t.."

        # Remove old result files, if there are any. Then run the code and store
        # output in results folder.
        if [ "$3" = "das" ]; then
            rm -f "/var/scratch/$USER/profiler.gif"
            prun -reserve "$4" -np 1 "./$1gol" 1000 1000 1000 -s 42 -o "/var/scratch/$USER/profiler.gif" $threadArgs 2> "$2/${1:5:-1}_t$t.out" > /dev/null
        else
            rm -f profiler.gif
            "./$1gol" 1000 1000 1000 -s 42 -o profiler.gif $threadArgs 2> "$2/${1:5:-1}_t$t.out" > /dev/null
        fi

        echo -e "\tDone."
    done
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

    # Unset the number of OpenMP threads as we test purely the code.
    unset OMP_NUM_THREADS

    # When on the DAS, reserve node to perform all experiments on.
    if [ "$2" = "das" ]; then
        reservation=$(preserve -# 1 -t 15:00)
        resid=${reservation:19:7}

        # Sleep 3 seconds for the cluster to activate our reservation.
        sleep 3
        echo -e "Reserved a node with id $resid\n"
    else
        # Set $resid to 0 if running locally.
        (( resid=0 ))
    fi

    # Run specific version, if specified.
    if [ ! "$1" = "all" ]; then
        # Check if folder with version number does exist.
        if ! compgen -G "apps/$1_*" > /dev/null; then
            echo "Version '$1' does not exist"
            exit 3
        fi

        vdir=$(find . -type d -name "$1*")
        run_profiler "${vdir:2}/" "$results" "$2" "$resid"
    else
        # Run tests for all versions.
        for d in apps/*/; do
            run_profiler "$d" "$results" "$2" "$resid"
        done
    fi

    # When on the DAS, cancel the reservation of the node.
    if [ "$2" = "das" ]; then
        preserve -c "$resid"
    fi
}

main "$@"
