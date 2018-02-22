#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void print_flag(void)
{
    char buf[128];
    int fd;
    int len = 0;
    fd = open("flag.txt", 0);
    len = read(fd, buf, 128);
    write(1, buf, len);
}

int main(int argc, char* argv[])
{
    char overflowme[128];
    printf("buffer address: %p\n", overflowme);
    printf("overflowme: ");
    gets(overflowme);
    printf("your input: %s\n", overflowme);

    int fail = 0;
    if(fail)
    {
        print_flag();
    }
    return 0;
}

