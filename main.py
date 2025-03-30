"""The main body of the python program"""
from __future__ import annotations
from tkinter import *
import customtkinter as ctk
from api_services.itunes import get_track_summary
import math


from datatypes import *
from tracks import *

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

    def __init__(self, master, graph: PlaylistGraph, **kwargs):
        super().__init__(master, **kwargs)
        self.graph = graph
        self.canvas = None
        self.node_positions = {}
        self._initialize_layout()
        self.display_graph()

    def _initialize_layout(self):
        """Set up grid and canvas"""
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.canvas = ctk.CTkCanvas(self, bg="white", height=800, width=1200)
        self.canvas.grid(row=0, column=0, sticky="nsew")

    def display_graph(self):
        """Draw the graph using force-directed layout"""
        self.canvas.delete("all")  # Clear previous drawing
        
        # Create NetworkX graph from PlaylistGraph
        G = nx.Graph()
        song_ids = self.graph.get_song_ids()
        edges = self.graph.get_connections()
        
        # Add nodes with metadata
        for song_id in song_ids:
            track = self.graph._verticies[song_id].item
            G.add_node(song_id, 
                      track_name=track.track_name,
                      artist=track.artists)

        # Add edges
        G.add_edges_from(edges)

        # Calculate positions using spring layout
        pos = nx.spring_layout(G, seed=42, k=0.15, iterations=50)
        
        # Scale positions to canvas dimensions
        pos = self._scale_positions(pos, 1200, 800)

        # Draw elements
        self._draw_edges(G, pos)
        self._draw_nodes(G, pos)

    def _scale_positions(self, pos, canvas_width, canvas_height, padding=50):
        """Scale networkx positions to canvas coordinates"""
        x_vals = [x for x, _ in pos.values()]
        y_vals = [y for _, y in pos.values()]
        
        min_x, max_x = min(x_vals), max(x_vals)
        min_y, max_y = min(y_vals), max(y_vals)

        # Avoid division by zero
        x_range = max(max_x - min_x, 1e-9)
        y_range = max(max_y - min_y, 1e-9)

        scaled_pos = {}
        for node, (x, y) in pos.items():
            # Normalize and scale
            scaled_x = padding + (x - min_x) / x_range * (canvas_width - 2*padding)
            scaled_y = padding + (y - min_y) / y_range * (canvas_height - 2*padding)
            scaled_pos[node] = (scaled_x, scaled_y)
            
        return scaled_pos

    def _draw_edges(self, G, pos):
        """Draw connections between songs"""
        for edge in G.edges():
            x1, y1 = pos[edge[0]]
            x2, y2 = pos[edge[1]]
            self.canvas.create_line(x1, y1, x2, y2, 
                                   fill="#808080", width=1)

    def _draw_nodes(self, G, pos):
        """Draw song nodes with labels"""
        for node in G.nodes():
            x, y = pos[node]
            track = self.graph._verticies[node].item
            
            # Node circle
            self.canvas.create_oval(x-20, y-20, x+20, y+20,
                                   fill="#4B8BBE", outline="#306998")
            
            # Track name label
            self.canvas.create_text(x, y-25, 
                                   text=track.track_name[:15] + ("..." if len(track.track_name) > 15 else ""),
                                   fill="black", font=("Arial", 9))
            
            # Artist label
            self.canvas.create_text(x, y+25,
                                   text=track.artists[:15] + ("..." if len(track.artists) > 15 else ""),
                                   fill="#666666", font=("Arial", 8))

class Playlist(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)



class App(ctk.CTk):
    def __init__(self, playlist: PlaylistGraph):
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

        self.playlist = Playlist(self)
        self.playlist.grid(row=0, column=2,sticky="ns", padx=5,pady=5)


class PlaylistGraph():
    """Graph object to store playlist information"""

    _verticies: dict[str, _Vertex]

    def __init__(self):
        self._verticies = {}

    def attempt_add_song(self, song: Track) -> bool:
        """Method to attempt to add a song without User's input"""
        ids_so_far = set()

        for track_id in self._verticies:
            if tk.get_similarity(track_id, song.track_id) < 0.1:
                ids_so_far.add(track_id)

        if len(ids_so_far) >= 3:
            self.add_item(song)
            for track_id in ids_so_far:
                self.add_edge(self._verticies[track_id].item, song)

            return True
        else:
            return False

    def add_item(self, song: Track) -> None:
        if song.track_id not in self._verticies:
            self._verticies[song.track_id] = _Vertex(song)

    def add_edge(self, song_1: Track, song_2: Track):
        if song_1.track_id in self._verticies and song_2.track_id in self._verticies:
            self._verticies[song_1.track_id].neighbours.add(self._verticies[song_2.track_id])
            self._verticies[song_2.track_id].neighbours.add(self._verticies[song_1.track_id])
        else:
            raise NameError

    def __contains__(self, item: Track) -> bool:
        return item.track_id in self._verticies

    def get_song_ids(self) -> list[str]:
        """Return all song IDs in the graph"""
        return list(self._verticies.keys())

    def get_song_names(self) -> list[str]:
        return [x.item.track_name for x in self._verticies.values()]

    def get_connections(self):
        """Return the list of edges (song pairs)"""
        edges = []
        for vertex in self._verticies.values():
            for neighbour in vertex.neighbours:
                edges.append((vertex.item.track_id, neighbour.item.track_id))
        return edges

class _Vertex:
    """Vertex object"""
    item: Track
    neighbours: set[_Vertex]

    def __init__(self, item: Track) -> None:
        self.item = item
        self.neighbours = set()


from io import BytesIO
from PIL import Image, ImageTk
# from pillow
import requests
import customtkinter as ctk

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
playlist = PlaylistGraph()

# temp
first_track = tk.get_track("22UDw8rSfLbUsaAGTXQ4Z8")
playlist.add_item(first_track)
temp_list = tk.find_multiple_similar(first_track.track_id, 5)
for item in temp_list:
    pending_songs.append((first_track, item))

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

    song_photo = get_tk_photo(song_info["artwork"])

    # confirmation = app.music_frame.user_input(curr_song.track_name, song_photo, curr_song.artists)
    confirmation = app.music_frame.user_input(curr_song.track_name, song_photo, curr_song.artists, song_info)
    if confirmation:
        playlist.add_item(curr_song)
        playlist.add_edge(curr_song, root_song)

        new_songs = tk.find_multiple_similar(curr_song.track_id, 10)

        for song in new_songs:
            if song not in playlist:
                if not playlist.attempt_add_song(song):
                    pending_songs.append((curr_song, song))

    pending_songs = [x for x in pending_songs if x[1] not in playlist]

    app.visualizer.display_graph()

    app.update()

