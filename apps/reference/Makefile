all: gol-plain gol-video giftest

gol-plain: gol.c
	gcc -Wall -O3 -o gol-plain gol.c

gol-video: gol.c
	gcc -Wall -O3 -o gol-video gol.c gif.c -lm -D VIDEO

giftest: giftest.c
	gcc -Wall -O3 -o giftest giftest.c gif.c

clean:
	rm -f *.o gol-plain gol-video giftest giftest *~ *core
