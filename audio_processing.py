import pyglet
import requests
import io

def play_m4a_with_pyglet(url):
    # Download the M4A file
    response = requests.get(url)
    audio_data = io.BytesIO(response.content)

    # Save to a temporary file
    with open("temp_audio.m4a", "wb") as f:
        f.write(audio_data.getbuffer())

    # Load and play the audio
    player = pyglet.media.Player()
    source = pyglet.media.load("temp_audio.m4a", streaming=False)
    player.queue(source)
    player.play()

    # Run Pyglet event loop
    pyglet.app.run()

# Example Usage
play_m4a_with_pyglet("https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview221/v4/fa/2c/d4/fa2cd4ed-4827-427e-21af-9e9eb4c799e0/mzaf_6203025356450809907.plus.aac.p.m4a")
