# Import packages
import os
import re

# Compile session reader
os.system("gcc -Wall summ.c summ_func.c -o summ")

# Make session array
session_arr = []

# If file ends in '.txt' it is a session
# Add to session array
for x in os.listdir('../data/input'):
    if x.endswith(".txt"):    
        session_arr.append('../data/input/' + x)    

# Sort session array
session_arr.sort()

# Run session reader for all sessions in order
for x in session_arr:
    arg_string = ["./summ ",x]
    os.system(" ".join(arg_string))

