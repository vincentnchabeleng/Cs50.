#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Initialize an integer variable "count" to keep track of the number of coins used.
    int count = 0;
    int quarter = 0;
    int dimes =0;
    int nickels = 0;
    int pannies = 0;
    // Declare a integer variable "change" to store the amount of change entered by the user.
    int change;
    int sum;


    do
    {
        // Prompt the user to enter the amount of change owed.
        change = get_int("Please enter the amount of change owed in cents:");
    }
    // Ensure that the amount entered is greater than or equal to 0.
    while (change < 0);

    //  Loop through each coin denomination starting from the largest (quarters) to the smallest (pennies).
    while (change >= 25)
    {
        // Deduct multiples of 25 from the remaining change and update the count accordingly.
        change -= 25;
        quarter++;

    }
    printf("Number of quater : %i\n", quarter);

    while (change >= 10)
    {
        // Deduct multiples of 10 from the remaining change and update the count accordingly.
        change -= 10;
        dimes++;


    }
    printf("Number of dimes is : %i\n", dimes);

    while (change >= 5)
    {
        // Deduct multiples of 5 from the remaining change and update the count accordingly.
        change -= 5;
        nickels++;

    }
    printf("Number of nickels is : %i\n", nickels);

    while (change >= 1)
    {
        // Deduct multiples of 1 from the remaining change and update the count accordingly.
        change -= 1;
        pannies++;

    }
    printf("Number of pannies is : %i\n", pannies);
    sum = quarter + dimes + nickels + pannies;

    // Print the total count of coins required to make the change.
    printf("Your change is : %i\n", sum);

}
