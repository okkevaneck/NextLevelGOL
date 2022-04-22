#!/usr/bin/env bash

# Executes the tests for a single version.
run_test() {
    echo "Running tests for ${1:5:-1}"

}


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

    VDIR=$(find . -type d -name "$1*")
    run_test "${VDIR:2}/"
else
    # Run tests for all versions.
    for d in apps/*/; do
        run_test "$d"
    done
fi
