# generate shellcode
```
nasm -f elf64 -o pflag.o pflag.asm
for i in $(objdump -d pflag.o | grep "^ " | cut -f2); do echo -n \\x$i; done; echo
```
