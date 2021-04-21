#include <stdlib.h>
#include <stdio.h>
#include "command_utils.h"

Command** parseCommands(char *byteArr)
{
    Command **result = malloc(sizeof(Command *)*50);
    for (int i = 0; i < 50; i++)
        result[i] = malloc(sizeof(Command));

    printf("Making array of structs\n");

    return result;
}

