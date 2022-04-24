#!/usr/bin/env bash

# Execute unit world tests.
run_unit_tests() {
    echo -e "\n\tRunning unit worlds.."

    # Fetch worlds from folder and test each individually.
    worlds=$(find tests/test_worlds/* -type f)

    for w in $worlds; do
        # Parse bwidth, bheight, and nsteps from filename.
        world_name=$(basename "$w")
        split_=(${world_name//_/ })
        params=(${split_[0]//x/ })

        # Store STDOUT for reference and version code while running in parallel.
        "./apps/v0_reference/gol-plain" "${params[0]}" "${params[1]}" "${params[2]}" 1 1 "$w" 2> /dev/null > ref.out &
        "./$1gol-plain" "${params[0]}" "${params[1]}" "${params[2]}" 1 1 "$w" 2> /dev/null > ver.out &
        wait

        # Compare output and log result.
        if ! diff ref.out ver.out; then
            echo -e "\t\tError: Unit failed - $world_name"
        else
            echo -e "\t\tSuccess: Unit passed - $world_name"
        fi

        # Delete intermediate files.
        rm ref.out ver.out
    done
}

# Execute configuration tests.
run_conf_tests() {
    echo -e "\tRunning configurations.."

    # Configurations to test.
    bwidths=( 42 100 )
    bheights=( 22 100 )
    nsteps=( 500 1200 )
    printworlds=( 1 1 )
    printcells=( 1 1 )

    # Test every configuration.
    for i in "${!bwidths[@]}"; do
        # Store STDOUT for reference and version code while running in parallel.
        "./apps/v0_reference/gol-plain" "${bwidths[i]}" "${bheights[i]}" "${nsteps[i]}" "${printworlds[i]}" "${printcells[i]}" 2> /dev/null > ref.out &
        "./$1gol-plain" "${bwidths[i]}" "${bheights[i]}" "${nsteps[i]}" "${printworlds[i]}" "${printcells[i]}" 2> /dev/null > ver.out &
        wait

        # Compare output and log result.
        if ! diff ref.out ver.out; then
            echo -e "\t\tError: Config failed - (${bwidths[i]} ${bheights[i]} ${nsteps[i]} ${printworlds[i]} ${printcells[i]})"
        else
            echo -e "\t\tSuccess: Config passed - (${bwidths[i]} ${bheights[i]} ${nsteps[i]} ${printworlds[i]} ${printcells[i]})"
        fi

        # Delete intermediate files.
        rm ref.out ver.out
    done
}

# Executes the tests for a single version, given as first argument.
run_test() {
    echo "Running tests for ${1:5:-1}"

    # Compile reference code.
    cd "apps/v0_reference" || exit 2
    make clean > /dev/null
    make gol-plain > /dev/null
    cd ../..

    # Compile the to be tested code with plain for configurations.
    cd "$1" || exit 4
    make clean > /dev/null
    make gol-plain > /dev/null
    cd ../..

    # Test different configurations.
    run_conf_tests "$@"

    # Compile the to be tested code with load for unit worlds.
    cd "$1" || exit 4
    make clean > /dev/null
    make gol-load > /dev/null
    cd ../..

    # Test unit worlds.
    run_unit_tests "$@"
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
            exit 3
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
