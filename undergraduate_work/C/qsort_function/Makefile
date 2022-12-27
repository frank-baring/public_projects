CC = gcc
CFLAGS = -g -Wall

isort: isort.o

isort.o: isort.c

.PHONY: clean
clean:
	rm -f *.o isort

.PHONY: all
all: clean isort

.PHONY: run
run: isort
	./isort

.PHONY: vg
vg: isort
	valgrind --leak-check=yes ./isort
