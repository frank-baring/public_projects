
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

static int compare_ascending(const void *x, const void *y)
{
    return *(int *)x - *(int *)y;
}

int main()
{
	printf("Please enter the length of your random number array: ");
    int n;
    scanf("%d", &n);
    int *p = malloc(n * sizeof(int));
    
    srandom(time(NULL));

    // fill the array with random integers
    int i;
    for (i = 0; i < n; i++)
        p[i] = random();

    // print the array
    printf("original array:\n");
    for (i = 0; i < n; i++)
        printf("%d ", p[i]);
    printf("\n");

    // sort the array using qsort library function

    qsort(p, n, sizeof(p[0]), &compare_ascending);
    
    // print the sorted array
    printf("sorted array:\n");
    for (i = 0; i < n; i++)
        printf("%d ", p[i]);
    printf("\n");

	// free pointers and return
    free(p);
    return 0;
}

