from flask import Flask, request, redirect, url_for, make_response
from hashlib import sha256
from random import getrandbits
from os import urandom
from binascii import unhexlify, hexlify
from time import time
from struct import pack, unpack
import re

FLAG = 'ZXBpY0ZhaWxOb3RBRmxhZ1lvdVN0aWxsSGF2ZVRvRmluZEl0'
USERS = [ 'billy', 'dutch', 'dillon' ]

secret = (None, 0)

def i2b(i):
    x = hex(i)[2:]
    if len(x) % 2:
        x = '0' + x
    return bytes.fromhex(x)

def b2i(b):
    return int(hexlify(b), 16)

def modexp(base, exp, mod):
    r = 1
    base %= mod
    while exp > 0:
        if exp % 2:
            r = r * base % mod
        exp >>= 1
        base = base * base % mod
    return r

def pkcs1Pad(m, k):
    m = i2b(m)
    l = k - 3 - len(m)
    assert l >= 8
    return b2i(b'\x00\x01' + b'\xff' * l + b'\x00' + m)

def rsaEncrypt(m, e, n):
    k = len(i2b(n))
    return modexp(pkcs1Pad(m, k), e, n)

def rsaVerifySig(s, m, e, n, h = sha256):
    paddedHash = b'\x00' + i2b(modexp(s, e, n))
    mHash = h(i2b(m)).digest()
    return re.match(b'\x00\x01\xff*\x00' + re.escape(mHash), paddedHash) != None

def loadKeys(users):
    keys = {}
    for user in users:
        key = {}
        with open('....../keys/{}'.format(user), 'r') as f:
            e, n = [int(next(f)) for _ in range(2)]
        key['e'] = e
        key['n'] = n
        keys[user] = key
    return keys

def getSecret():
    global secret
    if not secret[0] or secret[1] + 1800 < time():
        secret = (getrandbits(256), time())
    return secret[0]


keys = loadKeys(USERS)
app = Flask(__name__)

indexTemplate = '''
    <!DOCTYPE html>
    <html>
    <head>
...
   
    </body></html>
'''

loginTemplate = '''
    <!DOCTYPE html>
    <html>
    <head>
...
    </body></html>
'''

@app.errorhandler(404)
def errorshit(e):
    return app.send_static_file('error.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            if 'username' not in request.form:
                raise Exception("Username was not provided.")
            username = request.form['username']
            if username not in USERS:
                raise Exception("Username does not exist.")
            return redirect(url_for('login', username=username))
        except Exception as e:
            return indexTemplate.format('<p><font color="red">Error: {}</font></p>'.format(str(e)))
    return indexTemplate.format('')

@app.route('/login/<username>', methods=['GET', 'POST'])
def login(username):
    if username not in USERS:
        return redirect(url_for('index'))
    key = keys[username]
    e, n = key['e'], key['n']
    ct = rsaEncrypt(getSecret(), e, n)
    try:
        if request.method == 'POST':
            if 'signature' not in request.form:
                raise Exception("Signature was not provided.")
            sig = request.form['signature']
            try:
                sig = int(sig)
            except ValueError:
                raise Exception("Signature must be provided as an integer.")
            if not rsaVerifySig(sig, getSecret(), e, n):
                raise Exception("Invalid signature.")
            if username == 'dillon':
                return loginTemplate.format(username, e, n, ct, '<p><font style="font-size:15px; " color="green">Successfully authenticated: {}</font></p>'.format(str(FLAG)))
            return loginTemplate.format(username, e, n, ct, '<p><font color="red">Sorry, only an epic handshake can open this section!</font></p>')
        return loginTemplate.format(username, e, n, ct, '')
    except Exception as ex:
        return loginTemplate.format(username, e, n, ct, '<p><font color="red">Error: {}</font></p>'.format(str(ex)))

if __name__ == '__main__':
    ...
    app.run(host='127.0.2.2', port=12345)
    ...
