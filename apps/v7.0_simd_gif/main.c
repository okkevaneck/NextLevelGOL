#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef TIMED
#include <sys/time.h>
#endif

#include <pthread.h>

#include <sys/mman.h>
#include <unistd.h>
#include <fcntl.h>

#include "gif.h"
#include "gol.h"
#include "opts.h"
#include "util.h"

struct gif_thread_args {
    int steps;
    world *cur_world, *next_world;
    uint8_t *buffer;
    pthread_barrier_t *barrier;
};

void *gif_thread(void *args) {
    const int steps            = ((struct gif_thread_args *)args)->steps;
    world *cur_world           = ((struct gif_thread_args *)args)->cur_world;
    world *next_world          = ((struct gif_thread_args *)args)->next_world;
    uint8_t *buffer            = ((struct gif_thread_args *)args)->buffer;
    pthread_barrier_t *barrier = ((struct gif_thread_args *) args)->barrier;

    uint16_t width = cur_world->width;
    uint16_t height = cur_world->height;
    size_t offset = GIF_SIZE_HEADER;

    world *tmp_world;

#ifdef TIMED
    struct timeval tv;
    double time_start, time_end, gif_time = 0;
#endif

    /* Time steps... */
    for (int n = 0; n < steps; n++) {
        tmp_world = cur_world;
        cur_world = next_world;
        next_world = tmp_world;

        /* Wait for main thread to finish. */
        pthread_barrier_wait(barrier);

#ifdef TIMED
        time_start = time_secs(tv);
#endif
        offset = write_gif_frame(width, height, cur_world->cells[0], buffer, offset);
#ifdef TIMED
        time_end = time_secs(tv);
        gif_time += time_end - time_start;
#endif
    }

#ifdef TIMED
    double *elapsed_time = malloc(sizeof(double));  // Free in main!
    *elapsed_time = gif_time;
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

    FILE *input_fp = NULL;
    int output_fd = -1;

    world worlds[2];
    world *cur_world, *next_world;

    options opts;
    parse_opts(argc, argv, &opts);

    pthread_t thread;
    struct gif_thread_args thread_args;
    pthread_barrier_t barrier;

    size_t img_size = GIF_SIZE(opts.width, opts.height, opts.steps);
    size_t offset = 0;
    uint8_t *img = NULL;

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
        output_fd = open(opts.output, O_RDWR | O_CREAT, S_IRUSR | S_IWUSR);
        if (output_fd < 0) {
            fprintf(stderr, "Failed to open output file: '%s'!\n", opts.output);
            exit(1);
        }

        if (ftruncate(output_fd, img_size) < 0) {
            fprintf(stderr, "Failed to stretch output file!\n");
            exit(1);
        }

        img = (uint8_t *) mmap(NULL, img_size, PROT_READ | PROT_WRITE, MAP_SHARED, output_fd, 0);
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

    /* Setup the thread. */
    if (opts.use_output != 0) {
        pthread_barrier_init(&barrier, NULL, 2);
        thread_args.steps = opts.steps;
        thread_args.cur_world = cur_world;
        thread_args.next_world = next_world;
        thread_args.buffer = img;
        thread_args.barrier = &barrier;
        pthread_create(&thread, NULL, gif_thread, &thread_args);
    }

    /* Print the initial world state */
    if (opts.verbose != 0) {
        printf("\ninitial world:\n\n");
        world_print(cur_world);
    }

    /* Write the header part of the gif file */
    if (opts.use_output != 0) {
        offset = write_gif_header(cur_world->width, cur_world->height, img, offset);
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
#endif

        if (opts.verbose != 0) {
            printf("World contains %d live cells after time step %d:\n\n", world_count(cur_world), n);
            world_print(cur_world);
        }

        /* Wait for threads to catch up! */
        if (opts.use_output != 0) {
            pthread_barrier_wait(&barrier);
        }
    }

#ifdef TIMED
    time_start = time_secs(tv);
#endif
    if (opts.use_output != 0) {
        /* Stop the thread */
#ifdef TIMED
        double *thread_time = NULL;
        pthread_join(thread, (void **)&thread_time);
        gif = *thread_time;
        free(thread_time);  // Allocated in thread that no longer exists!
#else
        pthread_join(thread, NULL);
#endif

        /* Close the gif file */
        write_gif_trailer(img, GIF_SIZE(cur_world->width, cur_world->height, opts.steps)-1);

        msync(img, img_size, MS_SYNC);
        munmap(img, img_size);
        close(output_fd);
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
    fprintf(stderr, "  step  : %7.3f seconds (%6.2f%%)\n", step, step/actual*100);
    fprintf(stderr, "  swap  : %7.3f seconds (%6.2f%%)\n", swap, swap/actual*100);
    fprintf(stderr, "  gif   : %7.3f seconds (%6.2f%%)\n", gif, gif/actual*100);
    fprintf(stderr, "  final : %7.3f seconds (%6.2f%%)\n", final, final/actual*100);
    fprintf(stderr, "  -----------------------------------\n");
    fprintf(stderr, "  total : %7.3f seconds (%6.2f%%)\n", total, total/actual*100);
    fprintf(stderr, "  actual: %7.3f seconds (100.00%%)\n\n", actual);

    fprintf(stderr, "Throughput: %.0f pixels/second\n", opts.width * opts.height / total);
#endif

    return 0;
}
