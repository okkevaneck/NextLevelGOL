/***********************

Conway's Game of Life

Based on https://web.cs.dal.ca/~arc/teaching/CS4125/2014winter/Assignment2/Assignment2.html

************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>

typedef struct {
   int height, width;
   int **cells;
} world;

static world worlds[2];
static world *cur_world, *next_world;

static int print_cells = 0;
static int print_world = 0;

// use fixed world or random world?
#ifdef FIXED_WORLD
static int random_world = 0;
#else
static int random_world = 1;
#endif

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

static void
world_init_fixed(world *world)
{
    int **cells = world->cells;
    int i, j;

    /* use predefined start_world */

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

static void
world_init_random(world *world)
{
    int **cells = world->cells;
    int i, j;

    // Note that rand() implementation is platform dependent.
    // At least make it reprodible on this platform by means of srand()
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

static void
world_print(world *world)
{
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

static int
world_count(world *world)
{
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
static void
world_border_wrap(world *world)
{
    int **cells = world->cells;
    int i, j;

    /* left-right boundary conditions */
    for (i = 1; i <= world->height; i++) {
        cells[i][0] = cells[i][world->width];
        cells[i][world->width + 1] = cells[i][1];
    }

    /* top-bottom boundary conditions */
    for (j = 0; j <= world->width + 1; j++) {
        cells[0][j] = cells[world->height][j];
        cells[world->height + 1][j] = cells[1][j];
    }
}

static int
world_cell_newstate(world *world, int row, int col)
{
    int **cells = world->cells;
    int row_m, row_p, col_m, col_p, nsum;
    int newval;

    // sum surrounding cells
    row_m = row - 1;
    row_p = row + 1;
    col_m = col - 1;
    col_p = col + 1;

    nsum = cells[row_p][col_m] + cells[row_p][col] + cells[row_p][col_p]
         + cells[row  ][col_m]                     + cells[row  ][col_p]
         + cells[row_m][col_m] + cells[row_m][col] + cells[row_m][col_p];

    switch (nsum) {
    case 3:
        // a new cell is born
        newval = 1;
        break;
    case 2:
        // nothing happens
        newval = cells[row][col];
        break;
    default:
        // the cell, if any, dies
        newval = 0;
    }

    return newval;
}


// update board for next timestep
// height/width params are the base height/width
// excluding the surrounding 1-cell wraparound border
static void
world_timestep(world *old, world *new)
{
    int i, j;

    // update board
    for (i = 1; i <= new->height; i++) {
        for (j = 1; j <= new->width; j++) {
            new->cells[i][j] = world_cell_newstate(old, i, j);
        }
    }
}

static int **
alloc_2d_int_array(int nrows, int ncolumns)
{
    int **array;
    int i;

    /* version that keeps the 2d data contiguous, can help caching and slicing across dimensions */
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

static double
time_secs(void)
{
    struct timeval tv;

    if (gettimeofday(&tv, 0) != 0) {
        fprintf(stderr, "could not do timing\n");
        exit(1);
    }

    return tv.tv_sec + (tv.tv_usec / 1000000.0);
}

int
main(int argc, char *argv[])
{
    int n, nsteps;
    double start_time, end_time, elapsed_time;
    int bwidth, bheight;

    /* Get Parameters */
    if (argc != 6) {
        fprintf(stderr, "Usage: %s width height steps print_world print_cells\n", argv[0]);
        exit(1);
    }
    bwidth = atoi(argv[1]);
    bheight = atoi(argv[2]);
    nsteps = atoi(argv[3]);
    print_world = atoi(argv[4]);
    print_cells = atoi(argv[5]);

    /* initialize worlds, when allocating arrays, add 2 for ghost cells in both directorions */
    worlds[0].height = bheight;
    worlds[0].width = bwidth;
    worlds[0].cells = alloc_2d_int_array(bheight + 2, bwidth + 2);

    worlds[1].height = bheight;
    worlds[1].width = bwidth;
    worlds[1].cells = alloc_2d_int_array(bheight + 2, bwidth + 2);

    cur_world = &worlds[0];
    next_world = &worlds[1];

    /*  initialize board */
    if (random_world) {
        world_init_random(cur_world);
    } else {
        world_init_fixed(cur_world);
    }

    if (print_world > 0) {
        printf("\ninitial world:\n\n");
        world_print(cur_world);
    }

    start_time = time_secs();

    /*  time steps */
    for (n = 0; n < nsteps; n++) {
        world *tmp_world;

        world_border_wrap(cur_world);
        world_timestep(cur_world, next_world);

        // swap old and new worlds
        tmp_world = cur_world;
        cur_world = next_world;
        next_world = tmp_world;

        if (print_cells > 0 && (n % print_cells) == (print_cells - 1)) {
            printf("%d: %d live cells\n", n, world_count(cur_world));
        }

        if (print_world > 0 && (n % print_world) == (print_world - 1)) {
            printf("\nafter time step %d:\n\n", n);
            world_print(cur_world);
        }
    }

    end_time = time_secs();
    elapsed_time = end_time - start_time;

    /*  Iterations are done; sum the number of live cells */
    printf("Number of live cells = %d\n", world_count(cur_world));
    fprintf(stderr, "Game of Life took %10.3f seconds\n", elapsed_time);

    return 0;
}
