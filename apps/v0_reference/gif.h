#ifndef GIF_H
#define GIF_H

#include <inttypes.h>

/* Useful size definitions. */
#define BYTES_PER_BLOCK 126

#define MIN(a, b) ((a) < (b) ? (a) : (b))

/* Functions to write a gif, one component at a time. */
void write_gif_header(uint16_t width, uint16_t height, FILE *file);
void write_gif_frame(uint16_t width, uint16_t height, uint8_t *image, FILE *file);
void write_gif_trailer(FILE *file);

/* Function to write a single frame gif at once. */
void write_gif(uint16_t width, uint16_t height, uint8_t *image, FILE *file);

#endif
