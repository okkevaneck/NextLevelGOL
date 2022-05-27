/* Black & white animated GIF encoder.
 *   (c) Kevin Nobel
 *
 * Resources:
 *   GIF87a specs by CompuServe Incorporated, 1987
 *     http://www.w3.org/Graphics/GIF/spec-gif87.txt
 *   What's In A GIF by Mike Flickinger, 2005
 *     http://www.matthewflickinger.com/lab/whatsinagif/
 *     http://giflib.sourceforge.net/whatsinagif (mirror)
 */

#include <inttypes.h>
#include <stdio.h>

#include "gif.h"

/* Macro to write little endian. */
void lwrite(uint16_t *p, FILE *f) {
    fwrite((uint8_t[]) {(*p) & 0xFF, (*p) >> 8}, 2, 1, f);
}

void cwrite(uint8_t c, FILE *f) {
    fwrite(&c, 1, 1, f);
}

void write_gif_header(uint16_t width, uint16_t height, FILE *file) {
    /* Header Block: 3-byte signature ("GIF") + 3-byte version ("87a" or "89a") */
    fwrite("GIF89a", 6, 1, file);

    /* Logical Screen Descriptor:
     * 2-byte canvas width + 2-byte height +
     * 1-byte packed field + 1-byte BG color + 1-byte pixel aspect ratio */
    lwrite(&width, file);
    lwrite(&height, file);
    cwrite(0x80, file);  // 1 000 0 000
    cwrite(0x00, file);
    cwrite(0x00, file);

    /* Global Color Table: 2 x 3-byte RGB color mappings.
     * This table contains the colors:
     *   0: #FFFFFF
     *   1: #000000 */
    const uint8_t ct[6] = {
            0xFF, 0xFF, 0xFF,
            0x00, 0x00, 0x00
    };
    fwrite(ct, 6, 1, file);

    /* Graphics Control Extension: NETSCAPE 2.0 (looping animation) */
    cwrite(0x21, file);  // GIF Extension code
    cwrite(0xFF, file);  // Application Extension Label
    cwrite(0x0B, file);  // Application block length
    fwrite("NETSCAPE2.0", 11, 1, file);
    cwrite(0x03, file);  // Sub-block data length
    cwrite(0x01, file);  // Sub-block ID
    cwrite(0x00, file);  // Loop count (low  byte)
    cwrite(0x00, file);  // Loop count (high byte)
    cwrite(0x00, file);  // Sub-block terminator
}

void write_gif_frame(uint16_t width, uint16_t height, uint8_t *image, FILE *file) {
    /* Graphics Control Extension: Animation speed */
    cwrite(0x21, file);  // GIF Extension code
    cwrite(0xF9, file);  // Application Extension Label
    cwrite(0x04, file);  // Sub-block data length
    cwrite(0x08, file);  // 000 010 0 0
    cwrite(0x04, file);  // Animation speed (low  byte)
    cwrite(0x00, file);  // Animation speed (high byte)
    cwrite(0x00, file);  // Transparent color index
    cwrite(0x00, file);  // Sub-block terminator

    /* Image Descriptor:
     * 1-byte separator, 4-byte position, 4-byte dimensions, 1-byte option field */
    cwrite(0x2C, file);
    cwrite(0x00, file);  // 4-byte position
    cwrite(0x00, file);
    cwrite(0x00, file);
    cwrite(0x00, file);
    lwrite(&width, file);
    lwrite(&height, file);
    cwrite(0x00, file);

    /* Local Color Table: Not needed, we only use the global color table! */

    /* Image Data: Without LZW compression!
     * TODO: Compress 4 pixels into one byte.
     * TODO: Actually use LZW compression. */
    cwrite(0x07, file);  // 7-bit symbols (8-bit codes)
    size_t remaining = width * height;
    uint8_t size = 0;
    uint8_t *ptr = image;
    while(remaining > 0) {
        size = MIN(remaining, BYTES_PER_BLOCK);
        remaining -= size;

        cwrite(size + 1, file);  // How many bytes will follow.
        cwrite(0x80, file);      // Clear code (1000 0000)
        fwrite(ptr, size, 1, file);
        ptr = ptr + size;
    }
    cwrite(0x1, file);   // One byte will follow.
    cwrite(0x81, file);  // End of Information code (1000 0001)
    cwrite(0x00, file);  // Block terminator
}

void write_gif_trailer(FILE *file) {
    /* Trailer: 1-byte to mark the end of the file */
    cwrite(0x3B, file);
}

void write_gif(uint16_t width, uint16_t height, uint8_t *image, FILE *file) {
    write_gif_header(width, height, file);
    write_gif_frame(width, height, image, file);
    write_gif_trailer(file);
}
