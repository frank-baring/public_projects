CC = gcc 
CFLAGS = -g -Wall

mylist-test: mylist-test.o libmylist.a 

mylist-test.o: mylist-test.c mylist.c mylist.h

mylist.o: mylist.c mylist.h

libmylist.a: mylist.o
	ar rcs libmylist.a mylist.o

.PHONY: clean
clean:
	rm -f *.o *.a mylist-test

.PHONY: all 
all: clean mylist-test

.PHONY: run 
run: mylist-test
	./mylist-test

.PHONY: vg
vg: mylist-test
	valgrind --leak-check=yes ./mylist-test

