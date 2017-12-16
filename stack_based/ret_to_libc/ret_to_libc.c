#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char* argv[])
{
    char overflowme[128];
    printf("buffer address: %p\n", overflowme);

    printf("__libc_start_main address: %p\n", *(size_t *)(overflowme + 128 + 8));
    printf("overflowme: ");
    gets(overflowme);
    printf("your input: %s\n", overflowme);
    return 0;
}

