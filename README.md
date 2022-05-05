# Next Level Game of Life
This repository contains a performance engineering overview for a Conway's Game of Life implementation, where performance is pushed to the maximum.

<div align="center">
<img src="34p14.gif">

*[34p14 shuttle](https://conwaylife.com/wiki/34P14_shuttle)*
</div>

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

# Acknowledgements
The inital code was based on the assignment from the
[Parallel Programing Practical course](https://studiegids.vu.nl/en/Master/2020-2021/computer-science-joint-degree/X_400162)
at the Vrije Universiteit in Amsterdam, the Netherlands and the
[CS2110 course](https://web.cs.dal.ca/~arc/teaching/CS4125/2014winter/Assignment2/Assignment2.html) at Dalhousie
University in Halifax, NS, Canada.
