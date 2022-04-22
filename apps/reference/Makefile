all: gol-plain gol-video

gol-plain: gol.c
	gcc -Wall -O3 -o gol-plain gol.c

gol-video: gol.c
	gcc -Wall -O3 -o gol-video gol.c gif.c -lm -D VIDEO

clean:
	rm -f *.o gol-plain gol-video *~ *core
