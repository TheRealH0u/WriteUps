import requests
import base64
import json

def split_into_chunks(string, chunk_size=16):
    return [string[i:i+chunk_size] for i in range(0, len(string), chunk_size)]

user = "admin"

target_string = "9610b99c-bf65-4860-ad94-5112b007fa3a"+ \
        "::" + user + \
        "::" + "guest"
#target_string = "9610b99c-bf65-4860-ad94-5112b007fa3a::0000000000admin000000000::guest00000000000"
chunks = split_into_chunks(target_string)
print("Split Chunks:", chunks)


# url = "https://unchained.insomnihack.ch/login"
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#     "Accept-Language": "en-US,en;q=0.5",
#     "Accept-Encoding": "gzip, deflate, br",
#     "Content-Type": "application/x-www-form-urlencoded",
#     "Origin": "https://unchained.insomnihack.ch",
#     "Dnt": "1",
#     "Sec-Gpc": "1",
#     "Referer": "https://unchained.insomnihack.ch/login",
#     "Upgrade-Insecure-Requests": "1",
#     "Sec-Fetch-Dest": "document",
#     "Sec-Fetch-Mode": "navigate",
#     "Sec-Fetch-Site": "same-origin",
#     "Sec-Fetch-User": "?1",
#     "Priority": "u=0, i",
#     "Te": "trailers"
# }
# data = {"username": "0000000000admin000000000"}

# session = requests.Session()
# response = session.post(url, headers=headers, data=data)

# # Extract session cookie from response
# cookies = session.cookies.get_dict()
# session_cookie = cookies.get("session")
# if not session_cookie:
#     exit(0)

# try:
#         unsigned_cookie = ".".join(session_cookie.split(".")[:-1])
        
#         # Decode the base64-encoded session cookie payload
#         payload = unsigned_cookie.split(".")[0]
#         padding = "=" * (-len(payload) % 4)  # Fix padding if necessary
#         decoded_data = base64.urlsafe_b64decode(payload + padding).decode("utf-8")
#         data = json.loads(decoded_data)
#         cookie = data["status"]
#         cookie = base64.b64decode(cookie)
#         print(cookie)
# except Exception as e:
#     print("Error processing cookie:", e)
