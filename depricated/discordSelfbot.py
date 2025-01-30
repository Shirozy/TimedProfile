import requests
import base64
from tls_client import Session
import os
from dotenv import load_dotenv
from datetime import datetime
import random

sesh = Session(client_identifier="chrome_115", random_tls_extension_order=True)

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

folders = {
    'morning': './images/Morning/',
    'afternoon': './images/Midday/',
    'evening': './images/Evening/',
    'night': './images/Night/'
}

current_time = datetime.now()
if current_time.hour < 8: 
    current_time_of_day = 'morning'
elif current_time.hour < 18:
    current_time_of_day = 'afternoon'
elif current_time.hour < 22:
    current_time_of_day = 'evening'
else:
    current_time_of_day = 'night'

folder_path = folders[current_time_of_day]
image_files = [f for f in os.listdir(folder_path) if f.endswith('.jpg') or f.endswith('.png')]
random_image = random.choice(image_files)
random_image_file = os.path.join(folder_path, random_image)

with open(os.path.join(random_image_file), 'rb') as f:
    image_data = f.read()

base64_image_data = base64.b64encode(image_data).decode()

payload = {
    "avatar": f"data:image/jpeg;base64,{base64_image_data}"
}

headers = {
        "authority": "discord.com",
        "method": "PATCH",
        "scheme": "https",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US",
        "authorization": token,
        "origin": "https://discord.com",
        "sec-ch-ua": '"Not/A)Brand";v="99", "Brave";v="115", "Chromium";v="115"',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9020 Chrome/108.0.5359.215 Electron/22.3.26 Safari/537.36",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "X-Debug-Options": "bugReporterEnabled",
        "X-Discord-Locale": "en-US",
        "X-Discord-Timezone": "Asia/Calcutta",
        "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDIwIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDUiLCJvc19hcmNoIjoieDY0IiwiYXBwX2FyY2giOiJpYTMyIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV09XNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIGRpc2NvcmQvMS4wLjkwMjAgQ2hyb21lLzEwOC4wLjUzNTkuMjE1IEVsZWN0cm9uLzIyLjMuMjYgU2FmYXJpLzUzNy4zNiIsImJyb3dzZXJfdmVyc2lvbiI6IjIyLjMuMjYiLCJjbGllbnRfYnVpbGRfbnVtYmVyIjoyNDAyMzcsIm5hdGl2ZV9idWlsZF9udW1iZXIiOjM4NTE3LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsLCJkZXNpZ25faWQiOjB9"
    }
 
payload = {
    "avatar": f"data:image/jpeg;base64,{base64.b64encode(open(os.path.join(random_image_file), 'rb').read()).decode()}"
}
 
r =sesh.patch("https://discord.com/api/v9/users/@me", json=payload, headers=headers)
if r.status_code == 200:
    print("Profile picture changed successfully")
else:
    print(f"Error: {r.status_code}")
