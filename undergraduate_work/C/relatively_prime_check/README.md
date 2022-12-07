Program name: main.c

Function names: gcd.c, prime.c

Programmer: Frank Baring

Description: 

GCD.C:

This function returns a 1 or a 0 depending on whether two numbers are
relatively prime. I go on to use these return values in my main.c to print
out the correct result.

PRIME.C:

For my prime checker, I iterate through the lower half of each input,
starting at 2 and ending at the half-way point, to look for factors other
than 1 and the integer itself. If the algorithm is successful at finding a
factor, the inputted integer is a prime number and the function will return
a 1. If not, the function will simply return 0.

MAIN.C:

In this program I, firstly, calculate the average of the inputted variables
from the half value of their sum and print the result.

I then use the return value from prime.c to print out whether or not each
inputted variable is prime, using an if statement to represent that
conditional.

I then use the return value from the gcd.c program to print out whether or
not the two input variables are relatively prime, using another if
statement to represent that conditional.
