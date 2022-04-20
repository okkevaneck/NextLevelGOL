all: gol


gol: gol.c
	gcc -Wall -O3 -o gol gol.c gif.c -lm -D VIDEO

giftest: giftest.c
	gcc -Wall -O3 -o giftest giftest.c gif.c

clean:
	rm -f *.o gol giftest *~ *core
