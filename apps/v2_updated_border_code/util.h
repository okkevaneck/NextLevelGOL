#ifndef UTIL_H
#define UTIL_H

#include "gol.h"

pixel_t **alloc_2d_int_array(int nrows, int ncolumns);

void world_load(world *world, FILE* world_fp);
void world_init_random(world *world, unsigned int seed);

int world_count(world *world);
void world_print(world *world);

double time_secs(struct timeval tv);


#endif
