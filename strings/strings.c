#include <cs50.h>
#include <stdio.h>
#include <string.h>

int main (void)
{
  string strings [] = {"Battleship" , "Boot" , "Iron" , "Cannon" ,"Thimble"};
  string s = get_string("String: ");
  for(int i=0; i < 6; i++)
 {
    if(strings [i] == s)
    {
        printf("Found\n");
        return 0;
    }
 }
    printf("Not found\n");
    return 1;
}
