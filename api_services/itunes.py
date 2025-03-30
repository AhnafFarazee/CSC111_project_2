"""iTunes API"""
import requests

from spotify import Spotify

def id_to_track_summary(track_id: id) -> dict:
    """Return track summary from iTunes track ID"""

    track_data = fetch_itunes_track_data(track_id)

    track_summary = {
        "name": track_data['trackName'],
        "artist": track_data['artistName'],
        "album_name": track_data['collectionName'],
        "audio_url": track_data['previewUrl'],
        "artwork": track_data['artworkUrl100']
    }

    return track_summary


def fetch_itunes_track_data(track_id: int) -> dict:
    """
    Fetch track data from the iTunes API and return it as a dictionary.

    :param track_id: The track ID to look up.
    :return: Dictionary containing track data.
    """
    lookup_base_url = 'https://itunes.apple.com/us/lookup?id='
    track_lookup_url = lookup_base_url + f"{track_id}"

    response = requests.get(track_lookup_url)
    if response.status_code == 200:
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            return data["results"][0]  # Return track details
        else:
            print("Error: No results found.")
            return {}
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return {}



def spotify_id_to_info(track_id: str):
    spotify_obj = Spotify(track_id)
    data = spotify_obj.get_track()
    if data:
        result = get_itunes_id(data)
        return result
    return None


def get_itunes_id(spotify_data):
    artist = spotify_data["artists"][0]["name"]
    title = spotify_data["name"]
    """Returns the first iTunes song link based on title and artist search."""
    query = f"{artist} {title}".replace(" ", "+")
    url = f"https://itunes.apple.com/search?term={query}&entity=song&limit=1"

    response = requests.get(url)
    if response.status_code == 200:
        results = response.json().get("results", [])
        if results:
            track_id = results[0]["trackId"]
            return f"{track_id}"

    return None  # No match found

print(id_to_track_summary(spotify_id_to_info("11dFghVXANMlKmJXsNCbNl")))

