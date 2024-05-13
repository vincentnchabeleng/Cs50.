#include <cs50.h>  //Header file for cs50 library
#include <stdio.h> //Header file for standard library

int main(void)
{
    string name = get_string("Please enter your name:"); // Declaring a string variable and a prompt.

    printf("Hello %s!\n", name); // Output to be diplayed on screen.
}
