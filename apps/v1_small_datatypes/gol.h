#ifndef GOL_H
#define GOL_H

#include <inttypes.h>

typedef uint8_t pixel_t;

typedef struct {
    int width, height;
    pixel_t **cells;
} world;

void world_border_wrap(world *world);
void world_timestep(world *old, world *new);

#endif
