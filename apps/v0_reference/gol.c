/***********************

Conway's Game of Life

Based on the PPP assignment for the Computer Science master.
Based on https://web.cs.dal.ca/~arc/teaching/CS4125/2014winter/Assignment2/Assignment2.html

************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>

#ifdef VIDEO
#include <inttypes.h>
#include "gif.h"
#endif

typedef struct {
    int height, width;
    int **cells;
} world;

static world worlds[2];
static world *cur_world, *next_world;

static int print_cells = 0;
static int print_world = 0;

#ifdef FIXED_WORLD
static char *start_world[] = {
    /* Gosper glider gun */
    /* example from https://bitstorm.org/gameoflife/ */
    "..........................................",
    "..........................................",
    "..........................................",
    "..........................................",
    "..........................................",
    "..........................................",
    "........................OO.........OO.....",
    ".......................O.O.........OO.....",
    ".OO.......OO...........OO.................",
    ".OO......O.O..............................",
    ".........OO......OO.......................",
    ".................O.O......................",
    ".................O........................",
    "....................................OO....",
    "....................................O.O...",
    "....................................O.....",
    "..........................................",
    "..........................................",
    ".........................OOO..............",
    ".........................O................",
    "..........................O...............",
    "..........................................",
};

static void world_init(world *world) {
    int **cells = world->cells;
    int i, j;

    /* Use predefined start_world. */
    for (i = 1; i <= world->height; i++) {
        for (j = 1; j <= world->width; j++) {
            if ((i <= sizeof(start_world) / sizeof(char *)) &&
                (j <= strlen(start_world[i - 1]))) {
                cells[i][j] = (start_world[i - 1][j - 1] != '.');
            } else {
                cells[i][j] = 0;
            }
        }
    }
}
#endif

#ifndef FIXED_WORLD
static void world_init(world *world) {
    int **cells = world->cells;
    int i, j;

    /* Using srand() instead of rand() as it is reproducible on the designated
     * platform.
     */
    srand(1);

    for (i = 1; i <= world->height; i++) {
        for (j = 1; j <= world->width; j++) {
            float x = rand() / ((float)RAND_MAX + 1);
            if (x < 0.5) {
                cells[i][j] = 0;
            } else {
                cells[i][j] = 1;
            }
        }
    }
}
#endif

#ifdef VIDEO
static void world_print(world *world) {
    int **cells = world->cells;
    int i, j;
    int ci = 0;
    uint8_t *canvas = malloc(world->width * world->height);

    for (i = 1; i <= world->height; i++) {
        for (j = 1; j <= world->width; j++) {
            /* Fill the canvas */
            canvas[ci++] = cells[i][j];
        }
    }

    /* Write canvas to GIF file */
    write_gif_frame(world->width, world->height, canvas, stdout);

    free(canvas);
}
#endif

#ifndef VIDEO
static void world_print(world *world) {
    int **cells = world->cells;
    int i, j;

    for (i = 1; i <= world->height; i++) {
        for (j = 1; j <= world->width; j++) {
            if (cells[i][j]) {
                printf("O");
            } else {
                printf(" ");
            }
        }
        printf("\n");
    }
}
#endif

static int world_count(world *world) {
    int **cells = world->cells;
    int isum;
    int i, j;

    isum = 0;
    for (i = 1; i <= world->height; i++) {
        for (j = 1; j <= world->width; j++) {
            isum = isum + cells[i][j];
        }
    }

    return isum;
}

/* Take world wrap-around into account: */
static void world_border_wrap(world *world) {
    int **cells = world->cells;
    int i, j;

    /* left-right boundary conditions. */
    for (i = 1; i <= world->height; i++) {
        cells[i][0] = cells[i][world->width];
        cells[i][world->width + 1] = cells[i][1];
    }

    /* top-bottom boundary conditions. */
    for (j = 0; j <= world->width + 1; j++) {
        cells[0][j] = cells[world->height][j];
        cells[world->height + 1][j] = cells[1][j];
    }
}

static int world_cell_newstate(world *world, int row, int col) {
    int **cells = world->cells;
    int row_m, row_p, col_m, col_p, nsum;
    int newval;

    /* Sum surrounding cells. */
    row_m = row - 1;
    row_p = row + 1;
    col_m = col - 1;
    col_p = col + 1;

    nsum = cells[row_p][col_m] + cells[row_p][col] + cells[row_p][col_p]
           + cells[row  ][col_m]                     + cells[row  ][col_p]
           + cells[row_m][col_m] + cells[row_m][col] + cells[row_m][col_p];

    switch (nsum) {
        case 3:
            /* A new cell is born. */
            newval = 1;
            break;
        case 2:
            /* Nothing happens. */
            newval = cells[row][col];
            break;
        default:
            /* If there is a cell, it dies. */
            newval = 0;
    }

    return newval;
}

/* Update board for next time step.
 * Height/width params are the base height/width.
 * Excluding the surrounding 1-cell wraparound border.
 */
static void world_timestep(world *old, world *new) {
    int i, j;

    /* Update board. */
    for (i = 1; i <= new->height; i++) {
        for (j = 1; j <= new->width; j++) {
            new->cells[i][j] = world_cell_newstate(old, i, j);
        }
    }
}

static int **alloc_2d_int_array(int nrows, int ncolumns) {
    int **array;
    int i;

    /* Version that keeps the 2d data contiguous, can help caching and slicing
     * across dimensions.
     */
    array = malloc(nrows * sizeof(int *));
    if (array == NULL) {
        fprintf(stderr, "out of memory\n");
        exit(1);
    }

    array[0] = malloc(nrows * ncolumns * sizeof(int));
    if (array[0] == NULL) {
        fprintf(stderr, "out of memory\n");
        exit(1);
    }

    for (i = 1; i < nrows; i++) {
        array[i] = array[0] + i * ncolumns;
    }

    return array;
}

static inline double time_secs(struct timeval tv) {
    gettimeofday(&tv, 0);
    return tv.tv_sec + (tv.tv_usec / 1000000.0);
}

int main(int argc, char *argv[]) {
    int n, nsteps;
    int bwidth, bheight;

    struct timeval tv;
    double time_start, time_end, total;
    double wrap = 0.0;
    double step = 0.0;
    double swap = 0.0;
    double gif  = 0.0;

    /* Get parameters. */
    if (argc != 6) {
        fprintf(stderr, "Usage: %s width height steps print_world "
                        "print_cells\n", argv[0]);
        exit(1);
    }

    bwidth = atoi(argv[1]);
    bheight = atoi(argv[2]);
    nsteps = atoi(argv[3]);
    print_world = atoi(argv[4]);
    print_cells = atoi(argv[5]);

    /* Initialize worlds. When allocating arrays, add 2 for ghost cells in both
     * directions.
     */
    worlds[0].height = bheight;
    worlds[0].width = bwidth;
    worlds[0].cells = alloc_2d_int_array(bheight + 2,
                                         bwidth + 2);

    worlds[1].height = bheight;
    worlds[1].width = bwidth;
    worlds[1].cells = alloc_2d_int_array(bheight + 2,
                                         bwidth + 2);

    cur_world = &worlds[0];
    next_world = &worlds[1];

    /* Initialize board. */
    world_init(cur_world);

    if (print_world > 0) {
#ifndef VIDEO
        fprintf(stderr, "\ninitial world:\n\n");
#endif
#ifdef VIDEO
        write_gif_header(cur_world->width, cur_world->height, stdout);
#endif
        world_print(cur_world);
    }

    /* Time steps. */
    for (n = 0; n < nsteps; n++) {
        world *tmp_world;

        time_start = time_secs(tv);
        world_border_wrap(cur_world);
        time_end = time_secs(tv);
        wrap += time_end - time_start;

        time_start = time_secs(tv);
        world_timestep(cur_world, next_world);
        time_end = time_secs(tv);
        step += time_end - time_start;

        /* Swap old and new worlds. */
        time_start = time_secs(tv);
        tmp_world = cur_world;
        cur_world = next_world;
        next_world = tmp_world;
        time_end = time_secs(tv);
        swap += time_end - time_start;

        time_start = time_secs(tv);
        if (print_cells > 0 && (n % print_cells) == (print_cells - 1)) {
            fprintf(stderr, "%d: %d live cells\n", n, world_count(cur_world));
        }

        if (print_world > 0 && (n % print_world) == (print_world - 1)) {
#ifndef VIDEO
            fprintf(stderr, "\nafter time step %d:\n\n", n);
#endif
            world_print(cur_world);
        }
        time_end = time_secs(tv);
        gif += time_end - time_start;
    }

    /* Iterations are done: sum the number of live cells. */
    fprintf(stderr,"Number of live cells = %d\n\n", world_count(cur_world));

    /* Print timing data. */
    total = wrap + step + swap + gif;
    fprintf(stderr, "Total time spend in each part:\n");
    fprintf(stderr, "  wrap : %7.3f seconds (%6.2f%%)\n", wrap, wrap/total*100);
    fprintf(stderr, "  step : %7.3f seconds (%6.2f%%)\n", step, step/total*100);
    fprintf(stderr, "  swap : %7.3f seconds (%6.2f%%)\n", swap, swap/total*100);
    fprintf(stderr, "  gif  : %7.3f seconds (%6.2f%%)\n", gif, gif/total*100);
    fprintf(stderr, "  -----------------------------------\n");
    fprintf(stderr, "  total: %7.3f seconds (100.00%%)\n\n", total);

    fprintf(stderr, "Throughput: %.0f pixels/second\n", bwidth * bheight / total);

#ifdef VIDEO
    write_gif_trailer(stdout);
#endif
    return 0;
}
