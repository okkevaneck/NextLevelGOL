#include "gol.h"

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
}

static pixel_t world_cell_newstate(world *world, int row, int col) {
    pixel_t **cells = world->cells;
    int row_m, row_p, col_m, col_p, nsum;
    pixel_t newval;

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
    int width  = old->width;
    int height = old->height;

    /* Update board. */
    for (i = 1; i < height-1; i++) {
        for (j = 1; j < width-1; j++) {
            new->cells[i][j] = world_cell_newstate(old, i, j);
        }
    }
}
