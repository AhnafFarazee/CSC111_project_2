"""The main body of the python program.

This module sets up the graphical user interface (GUI) for a music playlist generator.
It uses CustomTkinter for UI components, retrieves song information via an external API,
and organizes songs into a tree-based playlist structure.
"""
from __future__ import annotations
from tkinter import *
import customtkinter as ctk
from itunes import get_track_summary

from datatypes import *
from tracks import *


from io import BytesIO
from PIL import Image
import requests


class MusicFrame(ctk.CTkFrame):
    """
    Frame to handle user choice regarding which songs are accepted and denied

    Attributes:
     - _confirm: boolean to confirm if user accepts or denies the song
    """

    _confirm: Optional[bool]

    def __init__(self, master, **kwargs):
        """
        Initialize the MusicFrame widget and set up its layout.

        Preconditions:
            - master is a valid Tkinter widget.
        """
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
        """
        Confirm the current song selection.
        """
        self.stop_audio()
        self._confirm = True

    def _deny_song(self) -> None:
        """
        Deny the current song selection.
        """
        self.stop_audio()
        self._confirm = False

    def play_pause(self) -> None:
        """ Play or pause the current song"""
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
        """ Update the widget to display information about the new song"""

        self.song_title.configure(text=title)
        self.song_title.grid(row=1, column=0, columnspan=3, sticky="ew")

        self.song_image.configure(image=image)
        self.song_image.grid(row=2, column=1)

        self.song_artist.configure(text=artists)
        self.song_artist.grid(row=3, column=0, columnspan=3, sticky="ew")

        # Reset play/pause button text when displaying a new song
        self.song_link.configure(text="play")

    def user_input(self, title: str, image, artists: str, song_info=None) -> bool:
        """ Return if user likes/dislikes the song"""

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
    """
    Frame to visualize the user's playlist.

    attributes:
     - playlist : PlaylistTree object that holds all the songs in the tree
     - canvas : Displays a visual aid of the playlist
    """
    def __init__(self, master, playlist: PlaylistTree, **kwargs):
        super().__init__(master, **kwargs)
        self.playlist = playlist

        self.canvas = ctk.CTkCanvas(self, bg="gray22", bd = 0)
        self.canvas.pack(fill=ctk.BOTH, expand=True)
        self.bind("<Configure>", self.on_resize)

        # Making the dimensions fit properly
        self.after(100, self.display_graph)

    def on_resize(self, event):
        """ Redraw the tree when the frame is resized. """
        self.display_graph()

    def display_graph(self):
        """ Clear and redraw the tree. """
        self.canvas.delete("all")

        def interpolate_color(depth):
            """ Interpolate between two colors based on depth (gradient). """
            start_color = (255, 0, 0)  # Red
            end_color = (0, 0, 255)    # Blue

            factor = depth / 10
            r = int(start_color[0] * (1 - factor) + end_color[0] * factor)
            g = int(start_color[1] * (1 - factor) + end_color[1] * factor)
            b = int(start_color[2] * (1 - factor) + end_color[2] * factor)

            return f"#{r:02x}{g:02x}{b:02x}"

        def get_circle_radius():
            """ Set a fixed size for all circles. """
            return 10 # makes it standard across the Tree

        def draw_tree(node: PlaylistTree, x: int, y: int, dx: float, depth=0):
            """ Recursively draw the tree with colored circles (gradient). """
            if node.is_empty():
                return

            color = interpolate_color(depth)

            radius = get_circle_radius()

            self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color, outline="black")

            new_y = y + 50 + radius

            num_subtrees = len(node._subtrees)
            if num_subtrees > 0:
                step = dx // num_subtrees if num_subtrees > 1 else dx
                start_x = x - (dx // 2) if num_subtrees > 1 else x

                for i, subtree in enumerate(node._subtrees):
                    new_x = start_x + i * step
                    self.canvas.create_line(x, y + radius, new_x, new_y - radius, fill="black")
                    draw_tree(subtree, new_x, new_y, step // 2, depth + 1)

        width = self.winfo_width() or 400
        draw_tree(self.playlist, width // 2, 50, width // 2)


class PlaylistFrame(ctk.CTkFrame):
    """ Frame to handle displaying the playlist to the user

    attributes:
     - playlist : PlaylistTree object that stores the playlist so far
     - my_list : mutable object to help terminate program properly
     - title : Shows the size of the playlist
     - list : Shows the songs within the playlist

    representation invariants:
     - len(self.my_list) == 1
    """

    def __init__(self, master, playlist: PlaylistTree, my_list: list[bool], **kwargs):
        """
        Initialize the PlaylistFrame.
        """
        super().__init__(master, **kwargs)
        self.playlist = playlist
        self.my_list = my_list

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.rowconfigure(2, weight=1)

        self.title = ctk.CTkLabel(self, text=f"playlist: {len(playlist)}", width = 200)
        self.title.grid(row = 0, column = 0)

        self.list = _ScrollingListFrame(self, self.playlist.get_all_tracks())
        self.list.grid(row = 1, column = 0)

        self.button = ctk.CTkButton(self, text="Stop Generating", bg_color="red", command=self.stop_app)
        self.button.grid(row = 2, column = 0)

    def stop_app(self) -> None:
        """ Function to terminate the program successfully"""
        self.my_list[0] = False

    def update(self) -> None:
        """ Function to update the label and list"""
        self.title.configure(text=f"playlist: {len(self.playlist)}")
        self.title.grid(row =0, column = 0)

        self.list = _ScrollingListFrame(self, self.playlist.get_all_tracks())
        self.list.grid(row = 1, column = 0)


class _ScrollingListFrame(ctk.CTkFrame):
    """ Helper Frame to display the playlist, in a scrollable fashion"""

    def __init__(self, master, items: list[Track], **kwargs):
        super().__init__(master, **kwargs)

        self.canvas = ctk.CTkCanvas(self, bg =  "gray22")
        self.scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=self.canvas.yview)
        self.scrollable_frame = ctk.CTkFrame(self.canvas)  # A frame to hold the list items

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.create_item_list(items)

        self.scrollable_frame.bind(
            "<Configure>", lambda x: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

    def create_item_list(self, items: list[Track]):
        """ Add items to the scrollable frame. """
        i = 0
        for item in items:
            i += 1
            label = ctk.CTkLabel(self.scrollable_frame, text=f"{i} - {item.track_name}", anchor="w")
            label.pack(fill = "both")


class App(ctk.CTk):
    """
    App holds the main body of the program, inherits from customtkinter.CTK

    Attributes:
     - music_frame : Frame to handle user decisions about songs
     - visualizer : Frame to display the tree
     - playlist : Frame to display all the songs added so far

    """
    def __init__(self, playlist: PlaylistTree, my_list: list[bool]):
        """
        Initialize the main application window.
        """
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

        self.visualizer = Visualizer(self, playlist)
        self.visualizer.grid(row=0,column=1,sticky="nsew", padx=5,pady=5)

        self.playlist = PlaylistFrame(self, playlist, my_list)
        self.playlist.grid(row=0, column=2,sticky="ns", padx=5,pady=5)


class PlaylistTree():
    """
    Tree structure to store songs in a playlist.

    Attributes:
        _root: Unique identifier of the root song; if None, the tree is empty.
        _info: The Track object associated with the root.
        _photo: Optional image associated with the root song.
        _subtrees: List of child PlaylistTree nodes.
    Representation Invariants:
        - If _root is None, then _info and _photo must also be None and _subtrees is empty.
        - _subtrees contains only PlaylistTree instances.
    """
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
        """ Return if item is contained within the tree"""
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
        """ Remove node with item from the tree"""
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
        """ Delete self from the tree, and fix tree as appropriate"""
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
        """ Add subtree to self"""
        self._subtrees.extend(subtrees)

    def add_song_to_parent(self, item: str, info: Track, photo: PhotoImage, parent: str) -> None:
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

    def get_all_tracks(self) -> list[Track]:
        """Return a list containing all Track objects in the tree."""
        if self.is_empty():
            return []

        items = [self._info]

        for subtree in self._subtrees:
            items.extend(subtree.get_all_tracks())

        return items


def get_tk_photo(url: str) -> ctk.CTkImage:
    """Fetch an image from a URL and return a CustomTkinter-compatible CTkImage."""
    response = requests.get(url)
    img_data = BytesIO(response.content)
    image = Image.open(img_data)

    ctk_image = ctk.CTkImage(light_image=image, size=(100, 100))
    return ctk_image

if __name__ == "__main__":
    tk = TrackList("dataset.csv")
    pending_songs = []
    filter = set()

    # mutable object To easy quit out of app
    app_ongoing = [True]


    # Initialization, done in terminal
    first_id = input("Enter the starting track id: ")
    first_track = tk.get_track(first_id)
    playlist = PlaylistTree(first_track.track_id, first_track, None)
    temp_list = tk.find_multiple_similar(first_track.track_id, 5)
    for item in temp_list:
        pending_songs.append((first_track, item))
        filter.add(item.track_name)

    app = App(playlist, app_ongoing)
    app.update()

    while app_ongoing[0]:
        root_song, curr_song = pending_songs.pop(0)

        song_info = get_track_summary(curr_song.artists, curr_song.track_name)

        while song_info == {}:         #recommend new song if itunes cannot find this one

            root_song, curr_song = pending_songs.pop(0)
            song_info = get_track_summary(curr_song.artists, curr_song.track_name)

        song_photo = get_tk_photo(song_info["artwork"])

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

        app.update()

        if len(pending_songs) < 3:
            app_ongoing[0] = False

    print("-" * 120)
    print("Final Playlist: ")
    i = 0
    for track in playlist.get_all_tracks():
        i += 1
        print(f"{i} - {track.track_name}")

