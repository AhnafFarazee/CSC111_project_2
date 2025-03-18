"""Library for use of Spotify API"""

import requests
from datatypes import Track

class Spotify:
    """
    Class for funtions related to spotify API
    """
    track_id: str
    base = "https://api.spotify.com/v1/tracks/"
    market = "CA"
    token = ('BQB_EYEyqs780VMTMD7atix-n9rdlDVViXv1GKncUCIBu4QpHEwrpkp18n_0Af5t4sJ6IaciuVbb7_s9'
             '-zK16YgJKqNbLqoKY73QGdKrCrA_781uaST6BAVBJ5pTXznTHUDzi0MoxkQ')  # TODO: access from env variable instead
    headers = {
        "Authorization": f"Bearer {token}"
    }
    url: str

    def __init__(self, track_id: str):
        self.url = self.base + track_id + '?market=' + self.market

    def get_track(self):  # returns json
        """Returns track information as JSON"""
        headers = self.headers
        url = self.url
        response = requests.get(url, headers=headers)
        return response.json()

    def parse_json_to_track_obj(self, data) -> Track:
        """Returns json data as Track object"""
        return Track(
            track_id=data["id"],
            artists=[artist["name"] for artist in data["artists"]],
            album_name=data["album"]["name"],
            track_name=data["name"],
            popularity=data["popularity"],
            duration_ms=data["duration_ms"],
            explicit=data["explicit"],
            track_genre="Unknown"  # Genre isn't provided in track data
        )


if __name__ == "__main__":
    example_track = Spotify("11dFghVXANMlKmJXsNCbNl")
    example_data = example_track.get_track()
    print(example_data)
