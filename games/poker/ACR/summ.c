/*
* Program name: summ.c
* Programmer: Frank Baring
* Description: Program to summarize an ACR session.
*/
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <assert.h>
#include "summ.h"

#define USERNAME "MezcalMule"

int main(int argc, char **argv)
{

//DECLARE VARIABLES
int vpip_check;
int file_check = 0;
int pnl_check = 0;
int lineno = 0;
int win_count = 0;
float vpip_count = 0;
float hands = 0;
double sitstack = 0;
double pnl_flt = 0;
char *newHand,*stakes,*pnl_str,*session_num_pt;
char *first_line = NULL;
char *line = NULL;
char session_num[strlen(argv[1])+1];
size_t len = 0;
ssize_t nread;

//CHECK FOR CORRECT PROGAM USAGE
if (argc != 2) {
        fprintf(stderr, "%s\n", "ERROR, usage: summ <file_name>");
        exit(1);
}
if(!(strstr(argv[1],"session_")) || !(strstr(argv[1],".txt"))){
	fprintf(stderr, "%s\n", "ERROR, usage: summ session_[number].txt");
	exit(1);
}

//EXTRACT SESSION NUMBER
strcpy(session_num,argv[1]);
strcpy(session_num,strstr(session_num,"_"));
session_num_pt = strtok(session_num,".");

//CHECK IF RAW DATA FILE EXISTS
if(access("session_summaries_raw.csv", F_OK) == 0) {
	file_check++;
}

//OPEN SESSION FILE
char *filename = argv[1];
FILE *fp = fopen(filename, "r");//session file (read)
FILE *fp2 = fopen("session_summaries.csv","a");//output file (append)
FILE *fp3 = fopen("session_summaries_raw.csv", "a+");//output file (append and read)
if (fp == NULL) {//check fp exists
        perror(filename);
        exit(1);
}

//USERNAME-DEPENDENT VARIABLES
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

//PRINT SUMMARY TO FILE
fprintf(fp2,"Session: %s\n",session_num_pt+1);
fprintf(fp2,"Stakes: %s\n",stakes);
fprintf(fp2,"Hands played: %.0f\n",hands);
fprintf(fp2,"VPIP: %.2f%%\n",(vpip_count/hands)*100);
fprintf(fp2,"Pots won: %d\n",win_count);
fprintf(fp2,"Profit/Loss: $%.2f\n",pnl_flt); 
fprintf(fp2,"*********************************\n");

//PRINT COLUMN NAMES IF FIRST ENTRY
if (file_check == 0) {
	fprintf(fp3, "session, stakes, hands_played, vpip, pots_won, pnl\n");
}

//PRINT RAW DATA TO FILE
fprintf(fp3, "%s, %s, %.0f, %.2f, %d, %.2f\n",
	session_num_pt+1,stakes,hands,(vpip_count/hands)*100,win_count,pnl_flt);

//CLOSE FILE
fclose(fp);
fclose(fp2);
fclose(fp3);

//FREE POINTERS
free(raise_check);
free(call_check);
free(startstack);

return 0;
}
