#include "gol.h"

#include "stdio.h"//TODO: Remove me!

static pixel_t get_newval(world *world, int lft, int h_mid, int rgt, int top, int v_mid, int bot) {
    pixel_t **cells = world->cells;
    int nsum;

    nsum =     cells[  top][lft] + cells[top][h_mid] + cells[  top][rgt]
             + cells[v_mid][lft]                     + cells[v_mid][rgt]
             + cells[  bot][lft] + cells[bot][h_mid] + cells[  bot][rgt];

    switch (nsum) {
        case 3:
            /* A new cell is born. */
            return 1;
        case 2:
            /* Nothing happens. */
            return cells[v_mid][h_mid];
        default:
            /* If there is a cell, it dies. */
            return 0;
    }
}

/* Take world wrap-around into account: */
void world_border_timestep(world *old, world *new) {
    int i;
    int width  = old->width;
    int height = old->height;

    /* Corners */
    new->cells[0][0]              = get_newval(old, width-1, 0, 1, height-1, 0, 1);
    new->cells[0][width-1]        = get_newval(old, width-2, width-1, 0, height-1, 0, 1);
    new->cells[height-1][0]       = get_newval(old, width-1, 0, 1, height-2, height-1, 0);
    new->cells[height-1][width-1] = get_newval(old, width-2, width-1, 0, height-2, height-1, 0);

    /* Top and bottom rows */
    for (i = 1; i < width-1; i++) {
        new->cells[0][i]        = get_newval(old, i-1, i, i+1, height-1, 0, 1);
        new->cells[height-1][i] = get_newval(old, i-1, i, i+1, height-2, height-1, 0);
    }

    /* Left and right column */
    for (i = 1; i < height-1; i++) {
        new->cells[i][0]       = get_newval(old, width-1, 0, 1, i-1, i, i+1);
        new->cells[i][width-1] = get_newval(old, width-2, width-1, 0, i-1, i, i+1);
    }

//    int i;
//    int width  = old->width;
//    int height = old->height;
//
//    /* ID 0 processes top half, ID 1 bottom half.
//     * First process corners, then process the top and bottom rows.
//     */
//    if (id == 0) {
//        /* Update top corners. */
//        new->cells[0][0]              = get_newval(old, width-1, 0, 1, height-1, 0, 1);
//        new->cells[0][width-1]        = get_newval(old, width-2, width-1, 0, height-1, 0, 1);
//
//        printf("Barrier wait for id 0\n");
//        pthread_barrier_wait(border_barrier);
//        printf("Barrier wait after id 0\n");
//
//        /* Update top row. */
//        for (i = 1; i < width - 1; i++) {
//            new->cells[0][i] = get_newval(old, i - 1, i, i + 1, height - 1, 0, 1);
//        }
//
//        /* Update top half of the columns. */
//        for (i = 1; i < (height - 1) / 2; i++) {
//            new->cells[i][0]       = get_newval(old, width-1, 0, 1, i-1, i, i+1);
//            new->cells[i][width-1] = get_newval(old, width-2, width-1, 0, i-1, i, i+1);
//        }
//    } else {
//        /* Update bottom corners. */
//        new->cells[height-1][0]       = get_newval(old, width-1, 0, 1, height-2, height-1, 0);
//        new->cells[height-1][width-1] = get_newval(old, width-2, width-1, 0, height-2, height-1, 0);
//
//        printf("Barrier wait for id 1\n");
//        pthread_barrier_wait(border_barrier);
//        printf("Barrier wait after id 1\n");
//
//        /* Update bottom row. */
//        for (i = 1; i < width - 1; i++) {
//            new->cells[height-1][i] = get_newval(old, i-1, i, i+1, height-2, height-1, 0);
//        }
//
//        /* Update top half of the columns. */
//        for (i = (height - 1) / 2; i < height - 1; i++) {
//            new->cells[i][0]       = get_newval(old, width-1, 0, 1, i-1, i, i+1);
//            new->cells[i][width-1] = get_newval(old, width-2, width-1, 0, i-1, i, i+1);
//        }
//    }
}

/* Update board for next time step.
 * Height/width params are the base height/width.
 * Excluding the surrounding 1-cell wraparound border.
 */
void world_timestep(world *old, world *new, int start_row, int end_row) {
    pixel_t *cells = *old->cells;
    pixel_t *newcells = *new->cells;
    int row, col, i, nsum;
    int width  = old->width;

    /* Update board. */
    for (row = start_row; row < end_row; row++) {
        i = width * row + 1;
        for (col = 1; col < width-1; col++) {
            /* Calculate sum of local (3x3) neighborhood, excluding the middle cell. */
            nsum = cells[i-width-1] + cells[i-width] + cells[i-width+1]
                 + cells[i      -1]                  + cells[i      +1]
                 + cells[i+width-1] + cells[i+width] + cells[i+width+1];

            /* Make a decision based on local sum. */
            switch (nsum) {
                case 3:
                    /* A new cell is born. */
                    newcells[i] = 1;
                    break;
                case 2:
                    /* Nothing happens. */
                    newcells[i] = cells[i];
                    break;
                default:
                    /* If there is a cell, it dies. */
                    newcells[i] = 0;
            }

            /* Continue to the cell on the right. */
            i++;
        }
    }
}
