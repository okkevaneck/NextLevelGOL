#ifndef GOL_H
#define GOL_H

typedef struct {
    int width, height;
    int **cells;
} world;

world worlds[2];
world *cur_world, *next_world;

void world_border_wrap(world *world);
void world_timestep(world *old, world *new);

#endif
