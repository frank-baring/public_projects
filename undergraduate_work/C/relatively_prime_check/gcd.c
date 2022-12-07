/*
This algorithm factorizes both numbers and multiplies the 
common factors.
*/
int gcd(int x, int y)
{
        if (y == 0) {
            return x;
        }else {
            return gcd(y, (x % y));
        }
        return 0;
}
