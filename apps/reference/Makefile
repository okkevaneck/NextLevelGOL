all: gol-plain


gol-plain: gol.c
	gcc -Wall -O3 -o gol.o gol.c

gol-video: gol.c
	gcc -Wall -O3 -o gol.o gol.c -lm -D VIDEO

clean:
	rm -f *.o gol *~ *core
