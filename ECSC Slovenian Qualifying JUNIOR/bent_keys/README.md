## Challenge Name: Bent Keys
Categories: Crypto, Web Security
Difficulty: Hard

## Description: 

Please start the vulnerable service from `RESOURCES`. This will start the `SSL/TLS` service on port `8443`. It is possible to get the private key from the server.

Once you have the private key, please run the following command

`openssl pkeyutl -derive -inkey private.key -peerkey public.key | sha1sum`

the `sha1` of the command above is the flag.

## Solution

Didn't solve this challenge.


---
[Back to home](../README.md)
