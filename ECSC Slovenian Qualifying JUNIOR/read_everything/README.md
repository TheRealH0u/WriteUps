## Challenge Name: Read Everything
Categories: Reverse Engineering, Exploitation, Crypto
Difficulty: Easy

## Description: 

Start the service from `RESOURCES`. The docker is offering two ports (web and socket port).
- port 80
- port 1342

Exploit port `1342`.

Flag Format: `UUID`

### Hint

The password is not the flag.


## Solution

This executable asks for the length of a password that we then enter. If we enter something else than a number, it just prints out the flag :/. That's it.

---
[Back to home](../README.md)
