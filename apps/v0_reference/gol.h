#ifndef GOL_H
#define GOL_H

typedef struct {
    int width, height;
    int **cells;
} world;

void world_border_wrap(world *world);
void world_timestep(world *old, world *new);

#endif
