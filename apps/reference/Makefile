all: gol


gol: gol.c
	gcc -Wall -O3 -o gol.o gol.c gif.c -lm -D VIDEO

clean:
	rm -f *.o gol *~ *core
