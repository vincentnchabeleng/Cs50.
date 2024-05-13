#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // n is height, h is hash, d is space, and i is row.
    // Get integer between 1 and 8 inclusively.
    int n;
    do
    {
        n = get_int("Please enter the height of the wall: ");
    }
    while (n > 8 || n < 1);

    // Create n rows.
    for (int i = 0; i < n; i++)
    {
        // Print  blank spaces " " (n - 1 - i) times
        for (int d = n - 1; d > i; d--)
        {
            printf(" ");
        }

        // Print right aligned hashes '#' (i + 1) times.
        for (int h = -1; h < i; h++)
        {
            printf("#");
        }

        printf(" ");
        // Print left aligned hashes '#' (i + 1) times.
        for (int h = -1; h < i; h++)
        {
            printf("#");
        }
        printf("\n");
    }
}
