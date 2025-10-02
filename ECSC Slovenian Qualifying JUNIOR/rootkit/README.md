## Challenge Name: Rootkit
Categories: Malware, Reverse Engineering, Forensic
Difficulty: Medium

## Description: 

Please download and analyze the given [libc_lib.so.6](libc_lib.so.6) rootkit file.

### Security Questions

- which ports are hidden from netstat output? `<port>`
- which files are hidden? `<prefix of file names>`
- in what conditions reverse shell is launched? `<src port number>`

### Flag Format

The flag is the md5sum of the three expected responses (all in lowercase, without wildcards, separated by `:`)

`echo -n "<port>:<prefix of file name>:<src port number>"`


## Solution


---
[Back to home](../README.md)
