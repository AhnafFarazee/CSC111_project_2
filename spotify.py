"""Library for use of Spotify API"""

# I can't get the API to work and I have no idea why

import requests
from datatypes import Track

class Spotify:
    """
    Class for funtions related to spotify API
    """
    spotify_id: str
    base: str

    def __init__(self, spotify_id:str):
        self.id = id
        self.base = "https://api.spotify.com/v1"

    def get_track(self, track_id:str) -> Track:
        response = requests.get(self.base + "/tracks/" + track_id)
        print(response.status_code)
        data = response.json()
        
        print(data["name"])


if __name__ == "__main__":
    sp = Spotify("a")
    bruh = sp.get_track("3VdooJLOy4tLxKpnn46SMP")