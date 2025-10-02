## Challenge Name: Magic Keys
Categories: Crypto
Difficulty: Easy

## Description: 
Use the hints below to get KEY1 and KEY2 from the service. The service will also disclose the missing PADDING information.

Please have a closer look at [script.py]()

- Please get `KEY1` (16 chars)
- Please get `KEY2` (16 chars)
- Please read the last piece of information from the service `PADDING` (4 chars)

Please concat `KEY1+KEY2+PADDING` (without entering the `+`) and you will get a valid `UUID`. This is the flag.

Flag Format: `UUID`

Artifact Files:
* [script.py](script.py)


## Solution


If we look at the python code, we can see that this is the function that decrypts the message:
```
def decrypt_message(key, IV, c):
    c.send(b"Hex data for decryption\n")
    c.send(b"=> ");
    ctxt = c.recv(4096);
    ctxt = str(ctxt.replace(b"\n", b"").decode("ascii"))
    ctxt = bytes.fromhex(ctxt)
    if (len(ctxt) % 16) != 0:
        c.send(b"Specify a proper length")
        return
    cipher = AES.new(key, AES.MODE_CBC, IV)
    ptxt = cipher.decrypt(ctxt)
    ptxt = ptxt.hex()
    c.send(bytes(ptxt + "\n\n", "ascii"))
```

If we check where it gets called, we can see that it's always called with the `IV` being set to the same as the `key`.

Looking at

![AES CBC Diagram](diagram.png)

we can see that we could get the `IV` by XOR-ing the output of the decryption with the plaintext that we already know. Getting the IV in this case = getting the key, so that's the solution.

I coded it up [here](solution.py)

---
[Back to home](../README.md)
