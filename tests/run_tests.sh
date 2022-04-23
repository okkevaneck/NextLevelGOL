#!/usr/bin/env bash

# Executes the tests for a single version, given as first argument.
run_test() {
    echo "Running tests for ${1:5:-1}"

    # Compile right version of code.
    cd "$1" || exit 3
    make clean
    make gol-fixed

    # Run code with FIXED_WORLD for 10 cycles. STDOUT and STDERR are captured
    # separately, and NULL bytes are parsed properly to avoid breaking.
    # From: https://stackoverflow.com/questions/11027679/capture-stdout-and-stderr-into-different-variables
    bwidth=$(( 42 ))
    bheight=$(( 22 ))
    nsteps=$(( 10 ))

    {
        IFS=$'\n' read -r -d '' out;
        IFS=$'\n' read -r -d '' err;
    } < <((printf '\0%s\0' "$( (./gol-fixed $bwidth $bheight $nsteps 1 1 | tr -d '\0') 3>&1- 1>&2- 2>&3- | tr -d '\0')" 1>&2 ) 2>&1)

    # Loop over STDERR lines and perform checks.
    for (( i=0; i<nsteps; i++)); do
        frame=${out:i*(bwidth+1)*bheight:bwidth*bheight}

        # Compare the current frame with the stored reference.

    done

    # Check for differences in frames.

    # Report difference of sum of alive cells on error.

}

# Main entry point of the script.
main() {
    # Check if arguments are passed.
    if [ $# -eq 0 ]; then
        echo "Usage: $0 [ all | v<version> ]"
        exit 1
    fi

    # Move up one dir if tests are ran from tests folder.
    if [ "${PWD##*/}" = "tests" ]; then
        cd ..
    fi

    # Run specific version, if specified.
    if [ ! "$1" = "all" ]; then
        # Check if folder with version number does exist.
        if ! compgen -G "apps/$1_*" > /dev/null; then
            echo "Version '$1' does not exist"
            exit 2
        fi

        vdir=$(find . -type d -name "$1*")
        run_test "${vdir:2}/"
    else
        # Run tests for all versions.
        for d in apps/*/; do
            run_test "$d"
        done
    fi
}

main "$@"
