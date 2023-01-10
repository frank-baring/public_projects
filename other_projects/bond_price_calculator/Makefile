CC = gcc
CFLAGS = -g -Wall

price: price.o

price.o: price.c

.PHONY: clean
clean:
	rm -f *.o price

.PHONY: all
all: clean price

.PHONY: run
run: price
	./price
