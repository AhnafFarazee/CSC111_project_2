"""The main body of the python program"""
from __future__ import annotations
from tkinter import *
import customtkinter as ctk
from api_services.itunes import get_track_summary
import random

from datatypes import *
from tracks import *


from io import BytesIO
from PIL import Image, ImageTk
# from pillow
import requests
import customtkinter as ctk


class InitialChoice(ctk.CTkFrame):
    _choices: dict[str, bool]

    def __init__(self, master):
        super.__init__(master)

    def confirm(self) -> list[str]:
        pass

class _Individual_Choice(ctk.CTkFrame):
    def __init__(self, master, image: PhotoImage, title:str, command: callable, **kwargs):
        super.__init__(master, **kwargs)

        self.image = ctk.CTkLabel(self, image = image, text="")
        self.image.grid(row=0, column=1)

        self.button = ctk.CTkButton(self, text=title, command=command)
        self.butt.grid(row=1, column = 0)


class MusicFrame(ctk.CTkFrame):
    """
    Frame to handle user choice regarding which songs are acceptable and not acceptable

    Attributes:
    _confirm: boolean to confirm if user accepts or denies the song
    """

    _confirm: Optional[bool]

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_propagate(False)

        self._confirm = None

        # Initialize player attributes
        self.player = None
        self.current_url = None
        self.is_playing = False
        self.player_thread = None
        self.current_song_info = None

        # Rest of your existing initialization code
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=5)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)
        self.rowconfigure(6, weight=3)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=1)

        # Row 1
        self.song_title = ctk.CTkLabel(self, text="Power", font=("Helvetica", 30))
        self.song_title.grid(row=1, column=0, columnspan=3, sticky="ew")

        # Row 2
        song_image = None
        self.song_image = ctk.CTkLabel(self, image=song_image, text="")
        self.song_image.grid(row=2, column=1)

        # Row 3
        self.song_artist = ctk.CTkLabel(self, text="Kanye West")
        self.song_artist.grid(row=3, column=0, columnspan=3, sticky="")

        # Row 4
        self.song_link = ctk.CTkButton(self, text="play/pause", command=self.play_pause)
        self.song_link.grid(row=4, column=1)

        self.deny_button = ctk.CTkButton(self, fg_color="red", text="no", command=self._deny_song, width=50)
        self.deny_button.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)

        self.confirm_button = ctk.CTkButton(self, fg_color="green", text="yes", command=self._confirm_song, width=50)
        self.confirm_button.grid(row=4, column=2, sticky="nsew", padx=5, pady=5)

    def _confirm_song(self) -> None:
        self.stop_audio()
        self._confirm = True

    def _deny_song(self) -> None:
        self.stop_audio()
        self._confirm = False


    def play_pause(self) -> None:
        """Play or pause the current song"""
        # Check if we have song info with an audio URL
        if not hasattr(self,
                       'current_song_info') or not self.current_song_info or "audio_url" not in self.current_song_info:
            print("No audio URL available")
            return

        url = self.current_song_info["audio_url"]

        # Toggle between play and pause states
        if url != self.current_url or self.player is None:
            # New song or first play
            if self.player:
                self.stop_audio()
            self.current_url = url
            self.play_audio(url)
            self.song_link.configure(text="pause")
        elif self.is_playing:
            # Pause current song
            self.player.pause()
            self.is_playing = False
            print("Paused playback")
            self.song_link.configure(text="play")
        else:
            # Resume current song
            self.player.play()
            self.is_playing = True
            print("Resumed playback")
            self.song_link.configure(text="pause")

    def play_audio(self, url):
        """Load and play audio from the given URL"""

        def audio_thread():
            import pyglet
            import requests
            import io

            print(f"Playing audio from: {url}")

            try:
                # Download the M4A file
                response = requests.get(url)
                audio_data = io.BytesIO(response.content)

                # Save to a temporary file
                with open("temp_audio.m4a", "wb") as f:
                    f.write(audio_data.getbuffer())

                # Load and play the audio
                self.player = pyglet.media.Player()
                source = pyglet.media.load("temp_audio.m4a", streaming=False)
                self.player.queue(source)
                self.player.play()
                self.is_playing = True

                # Setup pyglet event handling that doesn't block tkinter
                def update_player():
                    if not self.is_playing:
                        return

                    pyglet.clock.tick()
                    # Schedule the next update using tkinter's after method
                    self.after(33, update_player)  # ~30 fps

                # Start the update cycle
                update_player()
            except Exception as e:
                print(f"Error playing audio: {e}")
                self.is_playing = False

        # Run in a separate thread to avoid blocking the UI
        import threading
        self.player_thread = threading.Thread(target=audio_thread)
        self.player_thread.daemon = True
        self.player_thread.start()

    def stop_audio(self):
        """Stop the current audio playback"""
        if self.player:
            self.player.pause()
            self.player.delete()
            self.player = None
        self.is_playing = False
        print("Stopped playback")
        self.song_link.configure(text="play")

    def _update_current_song(self, title: str, image: PhotoImage, artists: str) -> None:
        self.song_title.configure(text=title)
        self.song_title.grid(row=1, column=0, columnspan=3, sticky="ew")

        self.song_image.configure(image=image)
        self.song_image.grid(row=2, column=1)

        self.song_artist.configure(text=artists)
        self.song_artist.grid(row=3, column=0, columnspan=3, sticky="ew")

        # Reset play/pause button text when displaying a new song
        self.song_link.configure(text="play")

    def user_input(self, title: str, image, artists: str, song_info=None) -> bool:
        # Store the song info for the play button to use
        self.current_song_info = song_info

        # Stop any currently playing audio
        self.stop_audio()

        self._update_current_song(title, image, artists)

        # waiting for user to press button
        while self._confirm is None:
            self.master.update()

        if self._confirm:
            self._confirm = None
            return True
        else:
            self._confirm = None
            return False


class Visualizer(ctk.CTkFrame):
    def __init__(self, master, graph: PlaylistTree, **kwargs):
        super().__init__(master, **kwargs)
        self.graph = graph

        # Create a canvas inside the frame
        self.canvas = ctk.CTkCanvas(self, bg="gray22", bd = 0)
        self.canvas.pack(fill=ctk.BOTH, expand=True)

        # Bind resizing event
        self.bind("<Configure>", self.on_resize)

        # Delay drawing to ensure proper dimensions
        self.after(100, self.display_graph)

    def on_resize(self, event):
        """ Redraw the tree when the frame is resized. """
        self.display_graph()

    def display_graph(self):
        """ Clear and redraw the tree. """
        self.canvas.delete("all")  # Clear previous drawings
        
        def interpolate_color(depth):
            """ Interpolate between two colors based on depth (gradient). """
            # Define the start and end color for the gradient (Hue changes as depth increases)
            start_color = (255, 0, 0)  # Red
            end_color = (0, 0, 255)    # Blue
            
            # Interpolate between start_color and end_color
            factor = depth / 10  # Divide by the max depth you want for color change
            r = int(start_color[0] * (1 - factor) + end_color[0] * factor)
            g = int(start_color[1] * (1 - factor) + end_color[1] * factor)
            b = int(start_color[2] * (1 - factor) + end_color[2] * factor)

            return f"#{r:02x}{g:02x}{b:02x}"

        def get_circle_radius():
            """ Set a fixed size for all circles. """
            return 10  # Fixed radius for all circles

        def draw_tree(node, x, y, dx, depth=0):
            """ Recursively draw the tree with colored circles (gradient). """
            if node.is_empty():
                return
            
            # Get the color for the circle based on the current depth
            color = interpolate_color(depth)
            
            # Get the fixed radius for the circle
            radius = get_circle_radius()
            
            # Create a circle instead of text
            self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color, outline="black")
            
            new_y = y + 50 + radius  # Increase the space between nodes (considering radius)

            num_subtrees = len(node._subtrees)
            if num_subtrees > 0:
                step = dx // num_subtrees if num_subtrees > 1 else dx
                start_x = x - (dx // 2) if num_subtrees > 1 else x

                for i, subtree in enumerate(node._subtrees):
                    new_x = start_x + i * step
                    self.canvas.create_line(x, y + radius, new_x, new_y - radius, fill="black")
                    draw_tree(subtree, new_x, new_y, step // 2, depth + 1)

        width = self.winfo_width() or 400
        draw_tree(self.graph, width // 2, 50, width // 2)

class PlaylistFrame(ctk.CTkFrame):

    def __init__(self, master, playlist: PlaylistTree, **kwargs):
        super().__init__(master, **kwargs)
        self.playlist = playlist

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)

        self.title = ctk.CTkLabel(self, text=f"playlist: {len(playlist)}", width = 200)
        self.title.grid(row = 0, column = 0)

        self.list = _ScrollingListFrame(self, self.playlist.get_all_tracks())
        self.list.grid(row = 1, column = 0)

    def update(self):
        self.title.configure(text=f"playlist: {len(self.playlist)}")
        self.title.grid(row =0, column = 0)

        self.list = _ScrollingListFrame(self, self.playlist.get_all_tracks())
        self.list.grid(row = 1, column = 0)

class _ScrollingListFrame(ctk.CTkFrame):
    def __init__(self, master, items: list, **kwargs):
        super().__init__(master, **kwargs)
        
        # Create a canvas and a scrollbar
        self.canvas = ctk.CTkCanvas(self, bg =  "gray22")
        self.scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=self.canvas.yview)
        self.scrollable_frame = ctk.CTkFrame(self.canvas)  # A frame to hold the list items
        
        # Configuring the canvas and scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack the canvas and scrollbar
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        # Create a window in the canvas to contain the scrollable frame
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Add items to the scrollable frame
        self.create_item_list(items)

        # Update the scroll region to match the content size
        self.scrollable_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

    def create_item_list(self, items: list[Track]):
        """ Add items to the scrollable frame. """
        i = 0
        for item in items:
            i += 1
            label = ctk.CTkLabel(self.scrollable_frame, text=f"{i} - {item.track_name}", anchor="w")
            label.pack(fill = "both")


class App(ctk.CTk):
    def __init__(self, playlist: PlaylistTree):
        super().__init__()
        self.geometry("1200xx900")
        self.minsize(height=400,width=600)
        self.title("PlayList Generator")

        self.columnconfigure(0,weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)
        self.rowconfigure(0, weight=1)

        self.music_frame = MusicFrame(self, width=300)
        self.music_frame.grid(row=0,column=0,sticky="ns", padx=5,pady=5)

        self.visualizer = Visualizer(self, graph=playlist)
        self.visualizer.grid(row=0,column=1,sticky="nsew", padx=5,pady=5)

        self.playlist = PlaylistFrame(self, playlist)
        self.playlist.grid(row=0, column=2,sticky="ns", padx=5,pady=5)


class PlaylistTree():
    """ Object to handle storing storing songs"""
    _root: Optional[str]
    _info: Optional[Track]
    _photo: Optional[PhotoImage]
    _subtrees: list[PlaylistTree]

    def __init__(self, root: Optional[str], info: Optional[Track], photo: Optional[PhotoImage]) -> None:
        self._root = root
        self._info = info
        self._photo = photo
        self._subtrees = []

    def is_empty(self) -> bool:
        """ Return if the tree is empty"""
        return self._root is None
    
    def __len__(self) -> int:
        """ Return the number of songs stored in the tree"""
        if self.is_empty():
            return 0
        else:
            size = 1
            for subtree in self._subtrees:
                size += subtree.__len__()
            return size
        
    def __contains__(self, item: str) -> bool:
        if self.is_empty():
            return False
        elif self._root == item:
            return True
        else:
            for subtree in self._subtrees:
                if subtree.__contains__(item):
                    return True
            return False
        
    def remove(self, item: str) -> bool:
        if self.is_empty():
            return False
        elif self._root == item:
            self._delete_root()
            return True
        else:
            for subtree in self._subtrees:
                deleted = subtree.remove(item)
                
                if deleted and subtree.is_empty():
                    self._subtrees.remove(subtree)
                    return True
                elif deleted:
                    return True
                
    def _delete_root(self) -> None:
        if self._subtrees == []:
            self._root = None
            self._info = None
            self._photo = None
        else:
            last_subtree = self._subtrees.pop()
            self._root = last_subtree._root
            self._info = last_subtree._info
            self._photo = last_subtree._photo
            self._subtrees.extend(last_subtree._subtrees)

    def add_subtrees(self, subtrees: list[PlaylistTree]) -> None:
        self._subtrees.extend(subtrees)

    def add_song_to_parent(self, item: str, info: Track, photo: PhotoImage, parent: str):
        """ Add Subtree with information to the specified parent Tree"""
        if self._root == parent:
            temp_tree = PlaylistTree(item, info, photo)
            self._subtrees.append(temp_tree)
        else:
            for subtree in self._subtrees:
                subtree.add_song_to_parent(item, info, photo, parent)

    def __str__(self, level=0) -> str:
        """Return a string representation of the tree."""
        if self.is_empty():
            return "(empty playlist)"
        
        result = "  " * level + f"- {self._photo}\n"
        for subtree in self._subtrees:
            result += subtree.__str__(level + 1)
        return result
    
    def get_all_tracks(self) -> list[str]:
        """Return a list containing all items (song names/IDs) in the tree."""
        if self.is_empty():
            return []

        # Start with the root item of the current node
        items = [self._info]

        # Recursively collect items from all subtrees
        for subtree in self._subtrees:
            items.extend(subtree.get_all_tracks())  # Extend the list with items from subtrees

        return items

def get_tk_photo(url):
    """Fetch an image from a URL and return a CustomTkinter-compatible CTkImage."""
    response = requests.get(url)
    img_data = BytesIO(response.content)
    image = Image.open(img_data)

    # Resize if needed (width, height)
    ctk_image = ctk.CTkImage(light_image=image, size=(100, 100))
    return ctk_image

tk = TrackList("dataset.csv")
pending_songs = []
filter = set()


# temp
first_track = tk.get_track("22UDw8rSfLbUsaAGTXQ4Z8")
playlist = PlaylistTree(first_track.track_id, first_track, None)
temp_list = tk.find_multiple_similar(first_track.track_id, 5)
for item in temp_list:
    pending_songs.append((first_track, item))
    filter.add(item.track_name)

app = App(playlist)
# app.mainloop()
app.update()

while True:
    root_song, curr_song = pending_songs.pop(0)

    # REMEMVER CALL RAEES TO FIX THIS

    song_info = get_track_summary(curr_song.artists, curr_song.track_name)

    while song_info == {}:         #recommend new song if itunes cannot find this one

        root_song, curr_song = pending_songs.pop(0)
        song_info = get_track_summary(curr_song.artists, curr_song.track_name)

    # regex, list of songs that have been

    song_photo = get_tk_photo(song_info["artwork"])

    # confirmation = app.music_frame.user_input(curr_song.track_name, song_photo, curr_song.artists)
    confirmation = app.music_frame.user_input(curr_song.track_name, song_photo, curr_song.artists, song_info)
    if confirmation:
        playlist.add_song_to_parent(curr_song.track_id, curr_song, song_photo, root_song.track_id)

        new_songs = tk.find_multiple_similar(curr_song.track_id, 7)

        for song in new_songs[:3]:
            if song not in playlist and song.track_name not in filter:
                playlist.add_song_to_parent(song.track_id, song, None, curr_song.track_id)
                filter.add(song.track_name)
                app.playlist.update()

        for song in new_songs[3:]:
            if song not in playlist and song.track_name not in filter:
                pending_songs.append((curr_song, song))
                filter.add(song.track_name)

    app.visualizer.display_graph()

    print(len(playlist))

    app.update()

