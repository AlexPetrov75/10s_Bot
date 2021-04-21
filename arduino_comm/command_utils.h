#ifndef COMMAND_UTILS_H
#define COMMAND_UTILS_H
#include "command.h"
#define MAX_CMDS_PER_ARR 5

Command** parseCommands(char *byteArr);
float getCommandArg(char *byteArr, char curLetterIdx);
void float2Bytes(char bytes[4], float floatVariable);

#endif



