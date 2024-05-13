#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

// Function prototype for checking if the key contains only digits
int only_digits(string key);

int main(int argc, string argv[])
{
    // Check if user provided a command-line argument
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // Check if the key contains only digits
    if (only_digits(argv[1]))
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    // Convert command-line argument to integer
    int key = atoi(argv[1]);

    // Prompt user for plaintext
    string plaintext = get_string("plaintext: ");

    // Iterate over each character in the plaintext
    printf("ciphertext: ");
    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        // Check if character is alphabetic
        if (isalpha(plaintext[i]))
        {
            // Convert uppercase characters
            if (isupper(plaintext[i]))
            {
                printf("%c", ((plaintext[i] - 'A' + key) % 26) + 'A');
            }
            // Convert lowercase characters
            else
            {
                printf("%c", ((plaintext[i] - 'a' + key) % 26) + 'a');
            }
        }
        // Print non-alphabetic characters unchanged
        else
        {
            printf("%c", plaintext[i]);
        }
    }

    printf("\n");
}

// Function to check if the key contains only digits
int only_digits(string key)
{
    for(int i = 0; i < strlen(key); i++)
    {
        if(!isdigit(key[i]))
        {
            return 1; // Return 1 if non-digit character found
        }
    }
    return 0; // Return 0 if all characters are digits
}
