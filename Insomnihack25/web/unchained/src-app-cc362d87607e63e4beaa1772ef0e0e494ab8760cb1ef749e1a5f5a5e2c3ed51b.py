from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from random import randint
import uuid
import os
from flask import Flask, request, session, redirect, url_for
import re
from waitress import serve

app = Flask(__name__)
app.secret_key = ''.join(["{}".format(randint(0, 9)) for num in range(0, 6)])

MAIN_KEY = b"FAKE_KEY"

def gen_userid():
    return str(uuid.uuid4())

def encrypt(data,MAIN_KEY):
    cipher = AES.new(MAIN_KEY, AES.MODE_ECB)
    cipher_text_bytes = cipher.encrypt(pad(data, 16,'pkcs7'))
    cipher_text_b64 = b64encode(cipher_text_bytes)
    cipher_text = cipher_text_b64.decode('ascii')
    return cipher_text

def decrypt(MAIN_KEY, cipher_text):
    rem0ve_b64 = b64decode(cipher_text)
    cipher = AES.new(MAIN_KEY, AES.MODE_ECB)
    decrypted_bytes = cipher.decrypt(rem0ve_b64)
    decrypted_data = unpad(decrypted_bytes, 16, 'pkcs7').decode('ascii')
    return decrypted_data

@app.route("/")
def welcome():
    return '''
    <div style="text-align: center;">
        <h1 style="font-size: 3em; color: #333;">UNDER CONSTRUCTION</h1>
        <img src="/static/img/page-under-construction.jpg" alt="Under Construction" style="width:400px; display: block; margin: 0 auto;">

    </div>
    <!-- HACKERS HAVE NO CHANCE THIS TIME!!! -->
    '''


@app.route("/status")
def status():
    if 'status' in session:
        plain_text = decrypt(MAIN_KEY, session["status"])
        return f'Logged in as {plain_text}'
    return 'You are not logged in'

@app.route("/secret")
def get_secret():
    plain_text = decrypt(MAIN_KEY, session["status"])
    role = plain_text.split("::")[2]
    if role == 'admin':
        return  os.environ['INS']
    return f'You are a just a {role}. Only admins can see the secret!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':        
        user_id = gen_userid()

        user = re.sub(r'\W+', '', request.form['username'])

        status_data = user_id + \
        "::" + user + \
        "::" + "guest"

        cipher_text = encrypt(data=status_data.encode('ascii'),MAIN_KEY=MAIN_KEY)
        session['status'] = cipher_text

        return redirect(url_for('status'))
    return '''
            <form method="post">
                <p>
                    <label for="username">Username:</label>
                    <input type="text" id="username" name="username">
                </p>
                <p>
                    <input type="submit" value="Login">
                </p>

                <p> * Note to myself: Password field TBD </p>
            </form>
    '''

@app.route('/logout')
def logout():
    session.pop('status', None)
    return redirect(url_for('status'))

if __name__=="__main__":
    serve(app, host='0.0.0.0', port=80)
