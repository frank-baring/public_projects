//Function to check if a number is prime.
int prime(int n)
{        
        int i; //Declaration of int i.
        /*
        Int i iterates through from 2 to half of the user input.
        There can be no factors greater than half of the integer.
        */
        for(i=2; i<=n/2; i++){
        	if(n > 3 && (n%i == 0)){
        		return 1; //Returning 1 to the function if the input has a factor in this range.
        	}
        }      
        return 0; //Returning 0 otherwise.
}
