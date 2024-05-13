#include <stdio.h>
#include <cs50.h>

int main(void)
{
    long credit_card;
    int sum = 0, count = 0, digit,total=0;

    // Prompt the user for credit card number
    do
    {
        credit_card = get_long("Enter your credit card number: ");
    }
    while (credit_card <= 0);

    // Calculate the checksum (sum of every other digit starting from the rightmost)
    for (long i = credit_card; i > 0; i /= 10)
    {
        digit = i % 10;
        if (count % 2 == 0)
        {
            sum += digit;
        }
        else
        {
            digit *= 2;
            sum += digit % 10 + digit / 10;
        }
        count++;
    }

    // Check if the checksum is valid and determine the card type
    if (sum % 10 == 0)
    {
        // Check the length and prefixes of the credit card number to determine the type
        if (count == 15 && (credit_card / 10000000000000 == 34 || credit_card / 10000000000000 == 37))
        {
            printf("AMEX\n");
        }
        else if (count == 16 && (credit_card / 100000000000000 >= 51 && credit_card / 100000000000000 <= 55))
        {
            printf("MASTERCARD\n");
        }
        else if ((count == 13 || count == 16) && (credit_card/1000000000000000 == 4))
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");

        }
    }
    else
    {
        printf("INVALID\n");
    }

}
