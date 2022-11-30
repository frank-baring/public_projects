Program names: summ.c data_collect.py

Programmer: Frank Baring

Description: Program to extract key metrics from an ACR session.

summ.c:

This program reads through .txt files that ACR distributes to users after a session on its platform.
First, the session file is opened with an error check in case file does not exist. Then variables are
declared. These are mostly checking variables (i.e. 0's to be turned to ++'d when certain criteria are met)
and char * pointers. Username dependent variable are declared last. These are strings that are concatenated
from the macro USERNAME using a helper function called mycat. The program then extracts the session number 
from the file name and reads the first line to extract the stakes of the session. Next the entire session is read to 
extract the number of hands, the user's VPIP (voluntary put in pot), the number of pots the user wins, and the 
profit/loss for the session. After reading, the program runs another error check on the file, and closes it. Finally,
the session summary is printed to a .csv file called session_summaries.csv and the raw data is printed to a .csv 
file called session_summaries_raw.csv. Finally, all allocated memory is freed.

data_collect.py:

This python program first compiles the summ.c program. It then searches for all .txt files in the current directory, 
which will be the session files, and stores the file names in a sorted array named session_arr. It then calls the compiled 
executable on each file by iterating through session_arr and executing an os.system() command.

Functions:

mycat - Helper function to concatenate strings into a new string on allocated memory using malloc().

Usage reminders:
1) Program users must edit summ.c to ensure their username is set as the USERNAME macro.
2) Session files must be located in the same directory as summ.c when it is compiled, so that the
executables can be run as follows: ./a.out session_[session number].txt (in our case: ./summ session_x.txt).
3) Makefile is prepared. To compile program type 'make' in terminal. To run program type 'make run' into terminal.
To clean directory type 'make clean' into terminal.

Thank you for reading.    

