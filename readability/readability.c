#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    // Prompt the user for input
    string text = get_string("Text: ");

    // Initilize counters for letters, words, and sentances
    int letters = 0;
    int words = 1;
    int sentences = 0;

    for (int i = 0, n = strlen(text); i < n; i++)
    {
        // Count letters
        if (isalpha(text[i]))
        {
            letters++;
        }
        // Count words by counting spaces
        else if (isspace(text[i]))
        {
            words++;
        }
        // Count sentences by detecting end of sentence puntuation
        else if (text[i] == '.' || text[i] == '?' || text[i] == '!')
        {
            sentences++;
        }
    }
    // Calculate average number of letters per 100 words (L) and average number of sentences per 100 words (S)
    float L = (float) letters / words * 100;
    float S = (float) sentences / words * 100;

    // Calculate the Coleman-Liau index
    int index = round(0.0588 * L - 0.296 * S - 15.8);

    // Determine and print the grade level based on the index
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}
