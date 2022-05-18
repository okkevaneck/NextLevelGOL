#ifndef GIF_H
#define GIF_H

#include <inttypes.h>

/* Useful size definitions. */
#define BYTES_PER_BLOCK 126

#define GIF_SIZE_HEADER        38
#define GIF_SIZE_TRAILER        1
#define GIF_SIZE_FRAME_HEADER  19
#define GIF_SIZE_FRAME_TRAILER  3
#define GIF_SIZE_BLOCK_HEADER   2

#define GIF_SIZE_FRAME(w, h) (                                                  \
    GIF_SIZE_FRAME_HEADER + GIF_SIZE_FRAME_TRAILER + w * h +                    \
    ((w * h + (BYTES_PER_BLOCK - 1)) / BYTES_PER_BLOCK) * GIF_SIZE_BLOCK_HEADER \
)

#define GIF_SIZE(w, h, s) \
    (GIF_SIZE_HEADER + s * GIF_SIZE_FRAME(w, h) + GIF_SIZE_TRAILER)

#define MIN(a, b) ((a) < (b) ? (a) : (b))

/* Functions to write a gif, one component at a time. */
void write_gif_header(uint16_t width, uint16_t height, FILE *file);
void write_gif_frame(uint16_t width, uint16_t height, uint8_t *image, FILE *file);
void write_gif_trailer(FILE *file);

/* Function to write a single frame gif at once. */
void write_gif(uint16_t width, uint16_t height, uint8_t *image, FILE *file);

#endif
