.PHONY: clean
clean:
	rm -f *.o summ

.PHONY: all
all: clean summ

.PHONY: run
run:
	gcc -Wall summ.c summ_func.c -o summ
	./summ session.txt 

