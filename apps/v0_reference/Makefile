all: gol-plain gol-video

gol-plain: gol.c
	gcc -Wall -O3 -o gol-plain gol.c

gol-fixed: gol.c
	gcc -Wall -O3 -o gol-fixed gol.c -lm -D FIXED_WORLD

gol-video: gol.c
	gcc -Wall -O3 -o gol-video gol.c gif.c -lm -D VIDEO

clean:
	rm -f *.o gol-plain gol-fixed gol-video *~ *core
