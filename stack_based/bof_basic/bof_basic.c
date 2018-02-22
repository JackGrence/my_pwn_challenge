#include <stdio.h>
#include <string.h>
#include <stdlib.h>


int main(int argc, char* argv[])
{
    char overflowme[128];
    printf("buffer address: %p\n", overflowme);
    printf("overflowme: ");
    gets(overflowme);
    printf("your input: %s\n", overflowme);
    
    int fail = 0;
    int fd;
    int len = 0;
    if(!fail)
    {
        fd = open("flag.txt", 0);
        len = read(fd, overflowme, 128);
        write(1, overflowme, len);
    }
    return 0;
}

