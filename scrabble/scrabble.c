#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int points[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
// char letters[] = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
//                   'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'};

string convert_upper(string word);
int compute_score(string upper_word);
void print_winner(int score1, int score2);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Convert to uppercase
    string upper_word1 = convert_upper(word1);
    string upper_word2 = convert_upper(word2);

    // Calculate scores
    int score1 = compute_score(upper_word1);
    int score2 = compute_score(upper_word2);

    // Print the winner
    print_winner(score1, score2);
}

string convert_upper(string word)
{
    // Convert to uppercase
    int length = strlen(word);
    for (int i = 0; i < length; i++)
    {
        word[i] = toupper(word[i]);
    }

    return word;
}

int compute_score(string upper_word)
{
    // Add score for each letter, skipping non-alphabetic characters
    int score = 0;
    for (int i = 0; i < strlen(upper_word); i++)
    {
        if (isalpha(upper_word[i]))
        {
            score += points[upper_word[i] - 'A'];
        }
    }
    return score;
}

void print_winner(int score1, int score2)
{
    // Check for tie
    if (score1 == score2)
    {
        printf("Tie! \n");
    }
    else
    {
        // Print result based on the scores
        if (score1 > score2)
        {
            printf("Player 1 wins \n");
        }
        else
        {
            printf("Player 2 wins \n");
        }
    }
}
