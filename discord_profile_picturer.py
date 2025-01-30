import os
from dotenv import load_dotenv
import requests
from tls_client import Session
from base64 import b64encode
from datetime import datetime
import random

load_dotenv()

def get_current_time_of_day():
    """Get the current time of day"""
    current_time = datetime.now()
    if 8 <= current_time.hour < 11:
        return 'morning'
    elif 11 <= current_time.hour < 18:
        return 'afternoon'
    elif 18 <= current_time.hour < 22:
        return 'evening'
    else:
        return 'night'

def get_random_image(folder_path):
    """Get a random image from the specified folder"""
    image_files = [f for f in os.listdir(folder_path) if f.endswith('.jpg') or f.endswith('.png')]
    return random.choice(image_files)

def encode_image_as_base64(image_file):
    """Encode an image as base64"""
    with open(image_file, 'rb') as f:
        return b64encode(f.read()).decode()

class DiscordProfilePicturer:
    def __init__(self):
        self.token = os.getenv("DISCORD_TOKEN")
        self.folders = {
            'morning': './images/Morning/',
            'afternoon': './images/Midday/',
            'evening': './images/Evening/',
            'night': './images/Night/'
        }

    def update_profile_picture(self):
        """Update the Discord profile picture"""
        current_time_of_day = get_current_time_of_day()
        folder_path = self.folders[current_time_of_day]
        image_file = os.path.join(folder_path, get_random_image(folder_path))
        encoded_image = encode_image_as_base64(image_file)
        payload = {
            "avatar": f"data:image/jpeg;base64,{encoded_image}"
        }

        headers = {
            "authority": "discord.com",
            "method": "PATCH",
            "scheme": "https",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US",
            "authorization": self.token,
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

        session = Session(client_identifier="chrome_115", random_tls_extension_order=True)
        response = session.patch("https://discord.com/api/v9/users/@me", json=payload, headers=headers)

        return response.status_code == 200