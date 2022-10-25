/*
* Program name: summ.c
* Programmer: Frank Baring
* Description: Program to summarize an ACR session.
*/
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <assert.h>
#include "summ.h"

#define USERNAME "MezcalMule"

int main(int argc, char **argv)
{

//CHECK FOR CORRECT PROGAM USAGE
if (argc != 2) {
        fprintf(stderr, "%s\n", "usage: summ <file_name>");
        exit(1);
}

//OPEN SESSION FILE
char *filename = argv[1];
FILE *fp = fopen(filename, "r");
if (fp == NULL) {
        perror(filename);
        exit(1);
}

//DECLARE VARIABLES
int vpip_check;
int pnl_check = 0;
int lineno = 0;
int win_count = 0;
float vpip_count = 0;
float hands = 0;
double sitstack = 0;
double pnl_flt = 0;
char *newHand,*stakes,*pnl_str;
char *first_line = NULL;
char *line = NULL;
size_t len = 0;
ssize_t nread;

//USERNAME DEPENDENT VARIABLES
char *raise_check = my_cat(USERNAME, " raises");
char *call_check = my_cat(USERNAME, " calls");
char *startstack = my_cat(USERNAME, " ($");

//RETURN STAKES
nread = getline(&first_line,&len,fp);
stakes = strtok(strstr(first_line,"$")," ");

//ITERATE THROUGH SESSION
while((nread = getline(&line,&len,fp)) != -1){
	newHand = strstr(line,"Hand #");
        lineno++;
	//HAND COUNT
        if(newHand != NULL){
		hands++;
		vpip_check = 1;
        }
	//VPIP COUNT
	if(strstr(line,"FLOP") || strstr(line,"SUMMARY")){
		vpip_check = 0;
	}

	if((strstr(line,raise_check) || strstr(line,call_check)) && vpip_check > 0){
		vpip_count++;
		vpip_check = 0;
	}
	//HANDS WON COUNT
	if(strstr(line,USERNAME) && strstr(line,"won")){
		win_count++;
	}
	//P/L TALLY
	if(strstr(line,startstack)){
		pnl_str = strtok(strstr(line,startstack),")");
		pnl_str = pnl_str + (strlen(USERNAME)+strlen(" ($"));
		if(pnl_check == 0){
			sitstack = atof(pnl_str);
			pnl_check++;
		}
		if(pnl_check > 0){
		        pnl_flt = atof(pnl_str) - sitstack;
		}
	}
}
//ERROR CHECK
if (ferror(fp)) {
        perror(filename);
        exit(1);
}

//CLOSE FILE
fclose(fp);

//PRINT SUMMARY
printf("*********SESSION SUMMARY*********\n");
printf("Stakes: %s\n",stakes);
printf("Hands played: %.0f\n",hands);
printf("VPIP: %.2f%%\n",(vpip_count/hands)*100);
printf("Pots won: %d\n",win_count);
printf("Profit/Loss: $%.2f\n", pnl_flt); 
printf("*********************************\n");

//FREE POINTERS
free(raise_check);
free(call_check);
free(startstack);

return 0;
}
