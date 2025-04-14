import requests

# Define the target URL
url = "http://192.168.15.10:4343/"

chrome = [
    "01",
    "02",
    "03",
    "04",
    "05",
    "06",
    "07",
    "08",
    "09",
    "11",
    "13",
    "16",
    "20",
    "21",
    "23",
    "24",
    "25"
]

appleWebKit = [
    "01",
    "02",
    "03",
    "04",
    "05",
    "06",
    "07",
    "08",
    "09"
]

for awk in appleWebKit:
    for ch in chrome:
        headers = {
            'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/53{awk}.36 (KHTML, like Gecko) Chrome/1{ch}.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Priority': 'u=0, i'
        }

        # Define the SOCKS5 proxy (change the IP and port to your actual SOCKS5 proxy details)
        proxies = {
            'http': 'socks5://192.168.174.128:55555',
            'https': 'socks5://192.168.174.128:55555',  # If you want the proxy to be used for HTTPS as well
        }

        # Send the GET request with the custom headers and via the SOCKS5 proxy
        response = requests.get(url, headers=headers, proxies=proxies)

        # Print the response content
        if response.status_code == 200:
            print("Response received successfully:")
            print(response.text)  # Print the HTML content or response body
        else:
            print(f"Request failed with status code: {response.status_code}")
