"""iTunes API"""
import requests
from tkinter import PhotoImage
from io import BytesIO


def get_track_summary(artist: str, title: str) -> dict:
    """Returns a dictionary with song details based on title and artist search.
    Returns an empty dictionary if there is an error finding the song."""

    keys = ["trackName", "artistName", "collectionName", "previewUrl", "artworkUrl100"]

    query = f"{artist} {title}".replace(" ", "+")
    url = f"https://itunes.apple.com/search?term={query}&entity=song&limit=1"

    response = requests.get(url)
    if response.status_code == 200:
        results = response.json().get("results", [])
        if results:
            track_data = results[0]
            if all(key in track_data for key in keys):
                return {
                    "name": track_data['trackName'],
                    "artist": track_data['artistName'],
                    "album_name": track_data['collectionName'],
                    "audio_url": track_data['previewUrl'],
                    "artwork": track_data['artworkUrl100']
                }

    return {}

# def load_image_from_url(url: str) -> PhotoImage:
#     """Return a photoimage from specified url
#     Return nothing if image was not found
#     """
#     response = requests.get(url)
#     if response.status_code == 200:
#         img_data = Image.open(BytesIO(response.content))
#
#         photo = PhotoImage(img_data)
#         return photo
#     else:
#         return None
#
#
# query = get_track_summary("Kanye West", "My beautiful dark twisted fantasy")
# print(query)
#
