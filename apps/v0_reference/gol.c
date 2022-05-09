#include "gol.h"

/* Take world wrap-around into account: */
void world_border_wrap(world *world) {
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
void world_timestep(world *old, world *new) {
    int i, j;

    /* Update board. */
    for (i = 1; i <= new->height; i++) {
        for (j = 1; j <= new->width; j++) {
            new->cells[i][j] = world_cell_newstate(old, i, j);
        }
    }
}
