#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef TIMED
#include <sys/time.h>
#endif

#include "gif.h"
#include "gol.h"
#include "opts.h"
#include "util.h"

int main(int argc, char *argv[]) {
#ifdef TIMED
    struct timeval tv;
    double time_start, time_end;
    double total, init, wrap = 0, step = 0, swap = 0, gif = 0, final;

    time_start = time_secs(tv);  // Initialization
#endif

    FILE *input_fp = NULL, *output_fp = NULL;

    world worlds[2];
    world *cur_world, *next_world;

    options opts;
    parse_opts(argc, argv, &opts);

    /* Open the input file. */
    if (opts.use_input) {
        input_fp = fopen(opts.input, "r");
        if (input_fp == NULL) {
            fprintf(stderr, "Failed to open input file: '%s'!", opts.input);
            exit(1);
        }
    }

    /* Open the output file. */
    if (opts.use_output) {
        output_fp = fopen(opts.output, "w");
        if (output_fp == NULL) {
            fprintf(stderr, "Failed to open output file: '%s'!", opts.output);
            exit(1);
        }
    }

    /* Initialize worlds. */
    worlds[0].width = opts.width;
    worlds[0].height = opts.height;
    worlds[0].cells = alloc_2d_int_array(opts.height, opts.width);

    worlds[1].width = opts.width;
    worlds[1].height = opts.height;
    worlds[1].cells = alloc_2d_int_array(opts.height, opts.width);

    cur_world = &worlds[0];
    next_world = &worlds[1];

    /* Initialize world */
    if (opts.use_input != 0) {
        world_load(cur_world, input_fp);
        fclose(input_fp);
    } else {
        world_init_random(cur_world, opts.seed);
    }

    /* Print the initial world state */
    if (opts.verbose != 0) {
        printf("\ninitial world:\n\n");
        world_print(cur_world);
    }

    /* Write the header part of the gif file */
    if (opts.use_output != 0) {
        write_gif_header(cur_world->width, cur_world->height, output_fp);
    }

#ifdef TIMED
    time_end = time_secs(tv);
    init = time_end - time_start;
#endif

    /* Time steps... */
    world *tmp_world;
    for (int n = 0; n < opts.steps; n++) {
#ifdef TIMED
        time_start = time_secs(tv);
#endif
        world_border_timestep(cur_world, next_world);
#ifdef TIMED
        time_end = time_secs(tv);
        wrap += time_end - time_start;

        time_start = time_secs(tv);
#endif
        world_timestep(cur_world, next_world);
#ifdef TIMED
        time_end = time_secs(tv);
        step += time_end - time_start;

        /* Swap old and new worlds. */
        time_start = time_secs(tv);
#endif
        tmp_world = cur_world;
        cur_world = next_world;
        next_world = tmp_world;
#ifdef TIMED
        time_end = time_secs(tv);
        swap += time_end - time_start;

        time_start = time_secs(tv);
#endif
        if (opts.verbose != 0) {
            printf("World contains %d live cells after time step %d:\n\n", world_count(cur_world), n);
            world_print(cur_world);
        }

        if (opts.use_output != 0) {
            write_gif_frame(cur_world->width, cur_world->height, cur_world->cells[0], output_fp);
        }
#ifdef TIMED
        time_end = time_secs(tv);
        gif += time_end - time_start;
#endif
    }

#ifdef TIMED
    time_start = time_secs(tv);
#endif
    /* Close the gif file */
    if (opts.use_output != 0) {
        write_gif_trailer(output_fp);
        fclose(output_fp);
    }
    free_2d_int_array(cur_world->cells);
    free_2d_int_array(next_world->cells);
#ifdef TIMED
    time_end = time_secs(tv);
    final = time_end - time_start;

    /* Print timing data */
    total = init + wrap + step + swap + gif + final;
    fprintf(stderr, "Total time spent in each part:\n");
    fprintf(stderr, "  init  : %7.3f seconds (%6.2f%%)\n", init, init/total*100);
    fprintf(stderr, "  wrap  : %7.3f seconds (%6.2f%%)\n", wrap, wrap/total*100);
    fprintf(stderr, "  step  : %7.3f seconds (%6.2f%%)\n", step, step/total*100);
    fprintf(stderr, "  swap  : %7.3f seconds (%6.2f%%)\n", swap, swap/total*100);
    fprintf(stderr, "  gif   : %7.3f seconds (%6.2f%%)\n", gif, gif/total*100);
    fprintf(stderr, "  final : %7.3f seconds (%6.2f%%)\n", final, final/total*100);
    fprintf(stderr, "  -----------------------------------\n");
    fprintf(stderr, "  total: %7.3f seconds (100.00%%)\n\n", total);

    fprintf(stderr, "Throughput: %.0f pixels/second\n", opts.width * opts.height / total);
#endif

    return 0;
}
