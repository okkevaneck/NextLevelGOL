#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "opts.h"

void init_opts(options *opts) {
    opts->verbose = 0;
    opts->time_code = 0;
    opts->seed = time(NULL);
    opts->use_input = 0;
    opts->input = NULL;
    opts->use_output = 0;
    opts->output = NULL;
}

void print_opts(options *opts) {
    printf(
            "Width     : %4d\n"
            "Height    : %4d\n"
            "Steps     : %4d\n"
            "Verbose   : %4d\n"
            "Time code : %4d\n"
            "Seed      : %4d\n"
            "Use Input : %4d (%s)\n"
            "Use Output: %4d (%s)\n",
            opts->width, opts->height, opts->steps,
            opts->verbose,
            opts->time_code,
            opts->seed,
            opts->use_input, opts->input,
            opts->use_output, opts->output
    );
}

void print_usage(char *name) {
    printf(
            "usage: %s width height steps [-v] [-t] [-s seed] [-i file] [-o file]\n\n"
            "Conway's Game of Life simulator by Okke van Eck & Kevin Nobel\n\n"
            "positional arguments:\n"
            "\twidth\t\tCanvas width (of input file, if used)\n"
            "\theight\t\tCanvas height (of input file, if used)\n"
            "\tsteps\t\tNumber of steps that should be simulated\n\n"
            "options:\n"
            "\t-h, --help\tShow this help message and exit\n"
            "\t-v, --verbose\tPrint world state to stdout\n"
            "\t-t, --time\tUse time code for performance metrics\n"
            "\t-s, --seed\tSeed to use for random world initialization\n"
            "\t-i, --input\tInput file to use as initial state\n"
            "\t-o, --output\tOutput file to use (will generate gif animation)\n",
            name
    );
}

void parse_opts(int argc, char *argv[], options *opts) {
    init_opts(opts);

    if (argc == 2 && (!strcmp(argv[1], "-h") || !strcmp(argv[1], "--help"))) {
        print_usage(argv[0]);
        exit(0);
    } else if (argc < 4) {
        print_usage(argv[0]);
        exit(1);
    }

    opts->width  = atoi(argv[1]);
    opts->height = atoi(argv[2]);
    opts->steps  = atoi(argv[3]);

    int i = 4;
    while (i < argc) {
        if (!strcmp(argv[i], "-h") || !strcmp(argv[i], "--help")) {
            print_usage(argv[0]);
            exit(0);
        } else if (!strcmp(argv[i], "-v") || !strcmp(argv[i], "--verbose")) {
            opts->verbose = 1;
        } else if (!strcmp(argv[i], "-t") || !strcmp(argv[i], "--time")) {
            opts->time_code = 1;
        } else if (i+1 < argc && (!strcmp(argv[i], "-s") || !strcmp(argv[i], "--seed"))) {
            opts->seed = atoi(argv[++i]);
        } else if (i+1 < argc && (!strcmp(argv[i], "-i") || !strcmp(argv[i], "--input"))) {
            opts->use_input = 1;
            opts->input = argv[++i];
        } else if (i+1 < argc && (!strcmp(argv[i], "-o") || !strcmp(argv[i], "--output"))) {
            opts->use_output = 1;
            opts->output = argv[++i];
        } else {
            print_usage(argv[0]);
            exit(1);
        }
        i++;
    }
}
