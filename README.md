# next_level_GOL
This repository contains a performance engineering overview for a Game of Life implementation, where performance is pushed to the maximum.

# Optimisations
 - Change variable types to be as small as possible -> char to represent 1 cell instead of an int
 - Use each bit of a char to represent 8 cells with 1 variable
   - Do this with inline functions
   - Do this with macro functions
 - Use SIMD operations
 - Optimize column data transfer.
 - Detect "dead zones", and only update edges instead of whole area.
 - Detect "stable structures" and only compute edges instead of computing all cells within area. Those can be loaded through pre-defined structures.
 - Avoid excessive looping in gif encoder (see `while` loop in `write_gif_frame`).
 - Pass the same data to gif encoder as used in GOL simulator (aka don't copy everything to a buffer). 
