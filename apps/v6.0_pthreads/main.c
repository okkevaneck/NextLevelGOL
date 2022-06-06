#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef TIMED
#include <sys/time.h>
#endif

#include <pthread.h>

#include "gif.h"
#include "gol.h"
#include "opts.h"
#include "util.h"

#define MAX(a, b) ((a) > (b) ? (a) : (b))

struct world_step_args {
    int start_row, end_row, steps;
    world *cur_world, *next_world;
    pthread_barrier_t *barrier;
};

void *world_step_thread(void *args) {
    const int start_row        = ((struct world_step_args *)args)->start_row;
    const int end_row          = ((struct world_step_args *)args)->end_row;
    const int steps            = ((struct world_step_args *)args)->steps;
    world *cur_world           = ((struct world_step_args *)args)->cur_world;
    world *next_world          = ((struct world_step_args *)args)->next_world;
    pthread_barrier_t *barrier = ((struct world_step_args *)args)->barrier;

#ifdef TIMED
    struct timeval tv;
    double time_start, time_end, step_time = 0;
#endif

    /* Time steps... */
    world *tmp_world;
    for(int n = 0; n < steps; n++) {
#ifdef TIMED
        time_start = time_secs(tv);
#endif
        world_timestep(cur_world, next_world, start_row, end_row);
#ifdef TIMED
        time_end = time_secs(tv);
        step_time += time_end - time_start;
#endif

        /* Swap old and new worlds. */
        tmp_world = cur_world;
        cur_world = next_world;
        next_world = tmp_world;

        pthread_barrier_wait(barrier);
    }

#ifdef TIMED
    double *elapsed_time = malloc(sizeof(double));  // Free in main!
    *elapsed_time = step_time;
    pthread_exit(elapsed_time);
#else
    pthread_exit(NULL);
#endif
}

int main(int argc, char *argv[]) {
#ifdef TIMED
    struct timeval tv;
    double time_start, time_end;
    double total, actual, init, wrap = 0, step = 0, swap = 0, gif = 0, final;

    time_start = time_secs(tv);  // Initialization
    actual = time_start;
#endif

    FILE *input_fp = NULL, *output_fp = NULL;

    world worlds[2];
    world *cur_world, *next_world, *tmp_world;

    options opts;
    parse_opts(argc, argv, &opts);

    pthread_t *thread = malloc(opts.threads * sizeof(pthread_t));
    struct world_step_args *thread_args = malloc(opts.threads * sizeof(struct world_step_args));
    pthread_barrier_t barrier;

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

    /* Setup the threads */
    pthread_barrier_init(&barrier, NULL, opts.threads + 1);
    int rows_per_thread = (opts.height - 2) / opts.threads + ((opts.height - 2) % opts.threads > 0);
    for (int i = 0; i < opts.threads; i++) {
        if (i == 0) {
            thread_args[i].start_row = 1;
        } else {
            thread_args[i].start_row = thread_args[i-1].end_row;
        }
        thread_args[i].end_row    = MIN(thread_args[i].start_row + rows_per_thread, opts.height - 1);
        thread_args[i].steps      = opts.steps;
        thread_args[i].cur_world  = cur_world;
        thread_args[i].next_world = next_world;
        thread_args[i].barrier    = &barrier;

        pthread_create(&thread[i], NULL, world_step_thread, &thread_args[i]);
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
    for (int n = 0; n < opts.steps; n++) {
#ifdef TIMED
        time_start = time_secs(tv);
#endif
        world_border_timestep(cur_world, next_world);
#ifdef TIMED
        time_end = time_secs(tv);
        wrap += time_end - time_start;
#endif

        /* Swap old and new worlds. */
#ifdef TIMED
        time_start = time_secs(tv);
#endif
        tmp_world = cur_world;
        cur_world = next_world;
        next_world = tmp_world;
#ifdef TIMED
        time_end = time_secs(tv);
        swap += time_end - time_start;
#endif

        /* Wait for threads to catch up! */
        pthread_barrier_wait(&barrier);

#ifdef TIMED
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
    /* Stop the threads */
    for (int i = 0; i < opts.threads; i++) {
#ifdef TIMED
        double *thread_time = NULL;
        pthread_join(thread[i], (void **)&thread_time);
        step = MAX(step, *thread_time);
        free(thread_time);  // Allocated in thread that no longer exists!
#else
        pthread_join(thread[i], NULL);
#endif
    }
    free(thread);
    free(thread_args);

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
    actual = time_end - actual;
    fprintf(stderr, "Total time spent in each part:\n");
    fprintf(stderr, "  init  : %7.3f seconds (%6.2f%%)\n", init, init/actual*100);
    fprintf(stderr, "  wrap  : %7.3f seconds (%6.2f%%)\n", wrap, wrap/actual*100);
    fprintf(stderr, "  step  : %7.3f seconds (%6.2f%%) (max of %d threads)\n", step, step/actual*100, opts.threads);
    fprintf(stderr, "  swap  : %7.3f seconds (%6.2f%%)\n", swap, swap/actual*100);
    fprintf(stderr, "  gif   : %7.3f seconds (%6.2f%%)\n", gif, gif/actual*100);
    fprintf(stderr, "  final : %7.3f seconds (%6.2f%%)\n", final, final/actual*100);
    fprintf(stderr, "  -----------------------------------\n");
    fprintf(stderr, "  total : %7.3f seconds (%6.2f%%)\n", total, total/actual*100);
    fprintf(stderr, "  actual: %7.3f seconds (100.00%%)\n\n", actual);

    fprintf(stderr, "Throughput: %.0f pixels/second\n", opts.steps * opts.width * opts.height / actual);
#endif

    return 0;
}
