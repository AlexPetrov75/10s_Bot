#include <stdio.h>
#include "command.h"
#include "command_utils.h"

int main(int argc, char *argv[])
{
    printf("Main\n");
    Command **cmds = parseCommands("asdf");
    for (int i = 0; i < 50; i++)
    {
        printf("Ptr: %p\n", cmds[i]);
    }
    return 0;
}
