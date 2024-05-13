#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int main(int argc, string argv[])
{
    // Check if the correct number of command-line arguments is provided
    if (argc != 2)
    {
        printf("Usage: %s key\n", argv[0]);
        return 1;
    }

    // Check if the key is valid
    string key = argv[1];
    int key_length = strlen(key);
    if (key_length != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    // Check if the key contains only alphabetic characters and each letter exactly once
    int freq[26] = {0};
    for (int i = 0; i < key_length; i++)
    {
        if (!isalpha(key[i]))
        {
            printf("Key must contain only alphabetic characters.\n");
            return 1;
        }

        int index = tolower(key[i]) - 'a';
        if (freq[index] == 1)
        {
            printf("Key must not contain duplicate characters.\n");
            return 1;
        }

        freq[index]++;
    }

    // Prompt user for plaintext
    string plaintext = get_string("plaintext: ");

    // Encrypt plaintext
    printf("ciphertext: ");
    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        char c = plaintext[i];
        if (isalpha(c))
        {
            // Preserve case of the character
            char base = islower(c) ? 'a' : 'A';
            // Calculate index of character in the key
            int index = tolower(c) - 'a';
            // Encrypt character using the key and preseve case
            char encrypted_char = islower(c) ? tolower(key[index]) : toupper(key[index]);
            // print encrypted character
            printf("%c", encrypted_char);
        }
        else
        {
            // Non-alphabetical characters remain unchanged
            printf("%c", c);
        }
    }
    printf("\n");

    return 0;
}
