#include <stdio.h>
#include <math.h>

int main()
{
    // Declare Variables	
    double price = 0.0;
    double coupon;
    double timeToMaturity;
    double YTM;
    double par;

    // Retrieve bond features from user
    printf("\nEnter years to maturity: ");
    scanf("%lf", &timeToMaturity);
    
    printf("\nEnter coupon rate: ");
    scanf("%lf", &coupon);
    
    printf("\nEnter face value: ");
    scanf("%lf", &par);
    
    printf("\nEnter yield to maturity: ");
    scanf("%lf", &YTM);
    
    // Compute price of bond
    YTM = YTM/100;
    coupon = (coupon/100)*par;

    	// ** Coupons **
    int i;
    for (i = 1; i <= timeToMaturity; i++){
    	price = price + (coupon / pow(1+YTM, i));  
    }

        // ** Principle **
    price = price + (par / pow(1+YTM, i-1));

    // Print price
    printf("Price: $%.2lf\n", price);
    
    return 0;
}
