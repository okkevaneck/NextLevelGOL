CC      = gcc
FLAGS   = -Wall -O3 -g -std=gnu99 -lpthread

TARGET  = gol
SRC     = $(wildcard *.c)
OBJ     = $(patsubst %.c,%.o,$(SRC))

.PHONY: all
all: $(TARGET)

$(TARGET): $(OBJ)
	$(CC) $(FLAGS) $(OBJ) -o $@

%.o: %.c
	$(CC) $(FLAGS) -c $< -o $@

.PHONY: clean
clean:
	rm -f $(TARGET) $(OBJ)
