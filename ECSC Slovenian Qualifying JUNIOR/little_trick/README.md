## Challenge Name: Little Trick
Categories: Reverse Engineering, Programming
Difficulty: Easy

## Description: 
Download the executable and find the missing XXXXXXXX and complete the UUID.
(Example UUID: `XXXXXXXX-522f-40fa-90eb-7c42213416e2`)

Artifact Files:
* [littletrick](littletrick)

## Solution

If we run the binary, we can see that it asks for a password:
```
$ ./littletrick
Password? 123
Wrong password, no flag. Sorry
```

If we look at the decompiled source of the main function (using [Ghidra](https://ghidra-sre.org/)), we can see it just compares the password you entered with the actual password (that's created earlier from some other data).

```
iVar1 = memcmp(passwd,buf,0x10);
if (iVar1 == 0) {
    decrypt(v,k);
    for (i = 0; i < 4; i = i + 1) {
        printf("%c%c",(ulong)(v[0] >> ((byte)(i << 3) & 0x1f) & 0xff),
                (ulong)(v[1] >> ((byte)(i << 3) & 0x1f) & 0xff));
    }
}
```

The simplest way to bypass the check is to just change the two instructions after the memcmp to `NOP` (Assembly instruction for no operation). Running this new program just prints the part of the flag, regardless of the password we enter:

```
$ ./patched
Password? test
d16ce710
```

---
[Back to home](../README.md)

