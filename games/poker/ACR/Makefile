.PHONY: clean
clean:
	rm -f *.o summ session_summaries.csv session_summaries_raw.csv

.PHONY: all
all: clean summ

.PHONY: run
run:
	python3 data_collect.py
#	gcc -Wall summ.c summ_func.c -o summ
#	./summ session.txt 

