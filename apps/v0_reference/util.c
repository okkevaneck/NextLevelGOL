#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <inttypes.h>

#include "gif.h"
#include "gol.h"
#include "util.h"

int **alloc_2d_int_array(int nrows, int ncolumns) {
    int **array;
    int i;

    /* Version that keeps the 2d data contiguous, can help caching and slicing
     * across dimensions. */
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

void free_2d_int_array(int **array) {
    free(array[0]);
    free(array);
}

void world_load(world *world, FILE* world_fp) {
    int **cells = world->cells;
    int i, j, k;
    char c = fgetc(world_fp);

    /* Load world from given file.
     * Fill blanks with 0 and skip extra characters per row.
     */
    for (i = 1; i <= world->height; i++) {
        for (j = 1; j <= world->width; j++) {
            /* If newline is found, fill in remaining row with 0. */
            if (j != world->width && (c == '\n' || c == EOF)) {
                for (k = j; k <= world->width; k++) {
                    cells[i][k] = 0;
                }

                break;
            }

            /* Otherwise parse character. EOF will be parsed as 0. */
            cells[i][j] = (c == 'O');

            /* Fetch next character. Keep EOF if found already. */
            if (c != EOF) {
                c = fgetc(world_fp);

                /* Skip newline char if end of row is reached as well. */
                if (c == '\n' && j == world->width) {
                    c = fgetc(world_fp);
                }
            }
        }

        /* Move to next line of input world and fetch new character. */
        while (c != EOF && c != '\n') {
            c = fgetc(world_fp);
        }
        c = fgetc(world_fp);
    }
}

void world_init_random(world *world, unsigned int seed) {
    int **cells = world->cells;
    int i, j;

    /* Using srand() instead of rand() as it is reproducible on the designated
     * platform. */
    srand(seed);

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

int world_count(world *world) {
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

void world_print(world *world) {
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
    printf("\n");
}

void world_frame(world *world, FILE *output_fp) {
    int **cells = world->cells;
    int i, j;
    int ci = 0;

    struct timeval tv;
    double time_start, time_convert, time_frame, time_free;

    time_start = time_secs(tv);
    uint8_t *canvas = malloc(world->width * world->height);

    for (i = 1; i <= world->height; i++) {
        for (j = 1; j <= world->width; j++) {
            /* Fill the canvas */
            canvas[ci++] = cells[i][j];
        }
    }
    time_convert = time_secs(tv);

    /* Write canvas to GIF file */
    write_gif_frame(world->width, world->height, canvas, output_fp);
    time_frame = time_secs(tv);

    free(canvas);
    time_free = time_secs(tv);

    double time_total = time_free - time_start;
    time_free -= time_frame;
    time_frame -= time_convert;
    time_convert -= time_start;

    printf("convert: %f\n", (time_convert) / time_total);
    printf("frame:   %f\n", time_frame / time_total);
    printf("free:    %f\n\n", (time_free) / time_total);

    printf("T_convert: %f\n", (time_convert + time_free) / time_total);
    printf("T_frame:   %f\n\n\n", (time_frame) / time_total);
}

double time_secs(struct timeval tv) {
    gettimeofday(&tv, 0);
    return tv.tv_sec + (tv.tv_usec / 1000000.0);
}
