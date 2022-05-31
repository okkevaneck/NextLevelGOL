#ifndef OPTS_H
#define OPTS_H

typedef struct {
    int width, height;
    int steps;
    int verbose;
    int threads;
    int seed;
    int use_input, use_output;
    char *input, *output;
} options;

void init_opts(options *opts);
void print_opts(options *opts);
void print_usage(char *name);
void parse_opts(int argc, char *argv[], options *opts);

#endif
