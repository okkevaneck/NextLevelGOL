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
#include <string.h>

#include "gif.h"

/* Function to write little endian. */
size_t le_set(uint16_t *value, uint8_t *buffer, size_t offset) {
    memcpy(&buffer[offset++], (uint8_t *) value, 1);
    memcpy(&buffer[offset++], (uint8_t *) value + 1, 1);
    return offset;
}

size_t write_gif_header(uint16_t width, uint16_t height, uint8_t *buffer, size_t offset) {
    /* Header Block: 3-byte signature ("GIF") + 3-byte version ("87a" or "89a") */
    strcpy((char *)&buffer[offset], "GIF89a");
    offset += 6;

    /* Logical Screen Descriptor:
     * 2-byte canvas width + 2-byte height +
     * 1-byte packed field + 1-byte BG color + 1-byte pixel aspect ratio */
    le_set(&width, buffer, offset);
    le_set(&height, buffer, offset+2);
    offset += 4;
    buffer[offset++] = 0x80;  // 1 000 0 000
    buffer[offset++] = 0x00;
    buffer[offset++] = 0x00;

    /* Global Color Table: 2 x 3-byte RGB color mappings.
     * This table contains the colors:
     *   0: #FFFFFF
     *   1: #000000 */
    buffer[offset++] = 0xFF;
    buffer[offset++] = 0xFF;
    buffer[offset++] = 0xFF;
    buffer[offset++] = 0x00;
    buffer[offset++] = 0x00;
    buffer[offset++] = 0x00;

    /* Graphics Control Extension: NETSCAPE 2.0 (looping animation) */
    buffer[offset++] = 0x21;  // GIF Extension code
    buffer[offset++] = 0xFF;  // Application Extension Label
    buffer[offset++] = 0x0B;  // Application block length
    strcpy((char *)&buffer[offset], "NETSCAPE2.0");
    offset += 11;
    buffer[offset++] = 0x03;  // Sub-block data length
    buffer[offset++] = 0x01;  // Sub-block ID
    buffer[offset++] = 0x00;  // Loop count (low  byte)
    buffer[offset++] = 0x00;  // Loop count (high byte)
    buffer[offset++] = 0x00;  // Sub-block terminator

    return offset;
}

size_t write_gif_frame(uint16_t width, uint16_t height, uint8_t *image, uint8_t *buffer, size_t offset) {
    /* Graphics Control Extension: Animation speed */
    buffer[offset++] = 0x21;  // GIF Extension code
    buffer[offset++] = 0xF9;  // Application Extension Label
    buffer[offset++] = 0x04;  // Sub-block data length
    buffer[offset++] = 0x08;  // 000 010 0 0
    buffer[offset++] = 0x04;  // Animation speed (low  byte)
    buffer[offset++] = 0x00;  // Animation speed (high byte)
    buffer[offset++] = 0x00;  // Transparent color index
    buffer[offset++] = 0x00;  // Sub-block terminator

    /* Image Descriptor:
     * 1-byte separator, 4-byte position, 4-byte dimensions, 1-byte option field */
    buffer[offset++] = 0x2C;
    buffer[offset++] = 0x00;  // 4-byte position
    buffer[offset++] = 0x00;
    buffer[offset++] = 0x00;
    buffer[offset++] = 0x00;
    le_set(&width, buffer, offset);
    le_set(&height, buffer, offset+2);
    offset += 4;
    buffer[offset++] = 0x00;

    /* Local Color Table: Not needed, we only use the global color table! */

    /* Image Data: Without LZW compression!
     * TODO: Compress 4 pixels into one byte.
     * TODO: Actually use LZW compression. */
    buffer[offset++] = 0x07;  // 7-bit symbols (8-bit codes)
    size_t remaining = width * height;
    uint8_t size = 0;
    uint8_t *ptr = image;
    while(remaining > 0) {
        size = MIN(remaining, BYTES_PER_BLOCK);
        remaining -= size;

        buffer[offset++] = size + 1;  // How many bytes will follow.
        buffer[offset++] = 0x80;      // Clear code (1000 0000)
        memcpy(&buffer[offset], ptr, size);
        ptr    += size;
        offset += size;
    }
    buffer[offset++] = 0x1;   // One byte will follow.
    buffer[offset++] = 0x81;  // End of Information code (1000 0001)
    buffer[offset++] = 0x00;  // Block terminator

    return offset;
}

size_t write_gif_trailer(uint8_t *buffer, size_t offset) {
    /* Trailer: 1-byte to mark the end of the file */
    buffer[offset++] = 0x3B;
    return offset;
}
