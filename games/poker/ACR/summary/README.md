Program name: summ.c
Programmer: Frank Baring
Description: Program to summarize an ACR session.

Overview:
This program reads through .txt files that ACR distributes to users after a session on its platform.
First, the session file is opened with an error check in case file does not exist. Then variables are
declared. These are mostly checking varaibles (i.e. 0's to be turned to ++'d when certain criteria are met)
and char * pointers. Username dependent variable are declared last. These are strings that are concatenated
from the macro USERNAME. The program then reads the first line to extract the stakes of the session. Next the
entire session is read to extract the number of hands, the user's VPIP (voluntary put in pot), the number of 
hands the user wins, and the profit/loss for the session. After reading, the program runs another 
error check on the file, and closes it. Finally, the session summary is printed and all allocated memory is freed.

Functions:
mycat - Helper function to concatenate strings into a new string on allocated memory using malloc().

Usage reminders:
1) Program users must edit summ.c to ensure their username is set as the USERNAME macro.
2) Session file must be located in the same directory as summ.c when it is compiled, so that
executable can be run as follows: ./a.out session.txt (in our case: ./summ session.txt).

Thank you for reading.    

