#include <stdio.h>
#include <string.h>
#include "command.h"
#include "command_utils.h"

int main(int argc, char *argv[])
{
    Command **cmds = parseCommands("asdf");
    
    float testNum = 123.456;
    printf("testNum: %f\n", testNum);
    char bytes[4];
    float2Bytes(bytes, testNum);

    char bytesToUse[5] = {bytes[0], bytes[0], bytes[1], bytes[2], bytes[3]};
    float testNumCalc = getCommandArg(bytesToUse, 0);

    printf("testNumCalc: %f\n", testNumCalc);

    return 0;
}
