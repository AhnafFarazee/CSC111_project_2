"""iTunes API"""
import requests

def get_track_summary(artist: str, title: str) -> dict:
    """Returns a dictionary with song details based on title and artist search.
    Returns an empty dictionary if there is an error finding the song."""

    query = f"{artist} {title}".replace(" ", "+")
    url = f"https://itunes.apple.com/search?term={query}&entity=song&limit=1"

    response = requests.get(url)
    if response.status_code == 200:
        results = response.json().get("results", [])
        if results:
            track_data = results[0]
            return {
                "name": track_data['trackName'],
                "artist": track_data['artistName'],
                "album_name": track_data['collectionName'],
                "audio_url": track_data['previewUrl'],
                "artwork": track_data['artworkUrl100']
            }

    return {}

