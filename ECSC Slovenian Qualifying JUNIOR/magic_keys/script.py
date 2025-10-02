#!/usr/bin/env python3
from Crypto.Cipher import AES
from config import key1, key2
import socket
import sys
import _thread

port = 1343

try:
    if len(key1) != 16 or len(key2) != 16:
        print("Configuration error - check key lengths!", file=sys.stderr)
        sys.exit(1)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', port));
    s.listen(5);
    i = 0;

    def main(c):
        while True:
            c.send(b"You have 2 keys to choose from: \n");
            c.send(b"=> ");
            key_opt = c.recv(4096);
            key_opt = str(key_opt.decode())
            key_opt = key_opt.replace("\n", "")
            if key_opt == "1":
                key = key1
            elif key_opt == "2":
                key = key2
            else:
                c.send(b"Only 2 keys available 1 or 2\n")
                continue
                exit()
            while True:
                c.send(b"1) Decrypt content\n")
                c.send(b"2) Choose a different key\n")
                c.send(b"3) Exit\n")
                c.send(b"=> ");
                choice = c.recv(4096);
                choice = str(choice.decode())
                choice = choice.replace("\n", "")
                if choice == "1":
                    decrypt_message(key, key, c)
                elif choice == "2":
                    key = new_key(c)
                else:
                    exit()
        c.close();


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

    def new_key(c):
        c.send(b"Choose between 2 keys\n")
        c.send(b"=> ")
        key_opt = c.recv(4096);
        key_opt = str(key_opt.decode())
        key_opt = key_opt.replace("\n", "")
        if key_opt == "1":
            key = key1
        elif key_opt == "2":
            key = key2

        else:
            c.send(b"Only 2 keys available")
            exit()
        return key

    while True:
        c, addr = s.accept();
        print("Socket Up and running with a connection from",addr);
        _thread.start_new_thread(main,(c,));
        i+=1;

except KeyboardInterrupt:
    print("\nClosing Connection and freeing the port.")
    c.close();
    sys.exit();


if __name__=='__main__':
    main()

