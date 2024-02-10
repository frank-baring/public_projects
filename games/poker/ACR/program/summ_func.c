#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <assert.h>
#include "summ.h"

char *my_cat(char* str1, char* str2){
    // Allocate memory for new string
	char *newstring = malloc(strlen(str1) + strlen(str2) + 1);
	newstring[0] = '\0';
	// Concatenate
	strcat(newstring, str1);
	strcat(newstring, str2);
	// Return
	return newstring;
}
