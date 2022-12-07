lCC = gcc
CFLAGS = -Wall -g
LDFLAGS = -g
LDFLAGS = -lm

main: main.o gcd.o prime.o

main.o: main.c prime.h gcd.h

gcd.o: gcd.c gcd.h

prime.o: prime.c prime.h

.PHONY: clean
clean: 
	rm -f *.o main core
	
.PHONY: run 
run: main
	./main

.PHONY: all
all: clean main
