#include <stdio.h>
#include "prime.h"
#include "gcd.h"

int main()
{
        int x, y; //Declaration of variables to be inputted by user.

        // ----------AVERAGE------------

        /* This is the function that returns the average
           of x and y as a floating point number.
        */

        // I had to use floating point variables to prevent my average from rounding.
        float tot;
        float avg; 

        printf("\nPlease enter your first number: ");
        scanf("%d", &x);
        printf("\nPlease enter your second number: ");
        scanf("%d", &y);

        tot = x + y; //tot = total(or sum) of x and y.
        avg = tot/2;

        printf("\nYou typed in %d and %d.\n", x, y);
        printf("\nThe average is: %.1f\n", avg);

        // -----------PRIME------------

        /* This is the print function that uses prime.c
           to check if x or y are prime and prints the 
           answer.
        */

        // If statement for x input. Using returned value from prime.c.
        if(prime(x) == 1){ 
        printf("\nx is not prime.\n");
        } else{
        printf("\nx is prime.\n");
        }

        // If statement for y input. Using returned value from prime.c.
        if(prime(y) == 1){ 
        printf("\ny is not prime.\n");
        } else{
        printf("\ny is prime.\n");
        }   
       
        // ------------GCD--------------

        /* This is the print function that uses gcd.c
           to check if x and y are relatively prime.
           The output depends on the returned value from
           gcd.c.
        */ 
        int comD;
        comD = gcd(x, y);
        
        if (comD == 1){
            printf("\n%d and %d are relatively prime.\n", x, y);
        } else{
            printf("\n%d and %d are NOT relatively prime.\n", x, y);
        }  
        return 0;

}
