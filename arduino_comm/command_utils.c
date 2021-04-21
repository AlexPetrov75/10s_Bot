#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "command_utils.h"

void float2Bytes(char bytes[4], float floatVariable)
{
    /* Used to populate byte arrays for testing */
    memcpy(bytes, (unsigned char*) (&floatVariable), 4);
}

Command** makeEmptyCommandArr(char *byteArr, char numCommands)
{
    /* Malloc array of struct pointers with one extra spot for null terminator */
    Command** emptyCommandArr = malloc(sizeof(Command *) * (numCommands + 1));

    /* Malloc each struct in array */
    for (int i = 0; i < numCommands; i++)
        emptyCommandArr[i] = malloc(sizeof(Command));

    /* Add null terminator */
    emptyCommandArr[numCommands] = NULL;

    return emptyCommandArr;
}

float getCommandArg(char *byteArr, char curLetterIdx)
{
    float f;
    char b[] = {byteArr[curLetterIdx + 1],
                byteArr[curLetterIdx + 2],
                byteArr[curLetterIdx + 3],
                byteArr[curLetterIdx + 4]};
    memcpy(&f, &b, sizeof(f));
    return f;
}

Command** parseCommands(char *byteArr)
{
    char numCommands = byteArr[0];

    Command **result = makeEmptyCommandArr(byteArr, numCommands);

    for (char i = 0; i < numCommands; i++)
    {
        Command *cmd = result[i];
        char curLetterIdx = 5 * (i - 1) + 1;
        cmd->command_char = byteArr[curLetterIdx];
        cmd->arg = getCommandArg(byteArr, curLetterIdx);
    }

    return result;
}

