"""The main body of the python program"""
from __future__ import annotations
from tkinter import *
import customtkinter as ctk
from api_services import itunes
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

        self.rowconfigure(0, weight=1)

        self.rowconfigure(1,weight=1)
        self.rowconfigure(2, weight=5)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)

        self.rowconfigure(6, weight=3)


        self.columnconfigure(0, weight=1)
        self.columnconfigure(1,weight=3)
        self.columnconfigure(2,weight=1)

        # self.label = ctk.CTkLabel(self, fg_color="gray", text = "bruh")
        # self.label.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # row 1
        self.song_title = ctk.CTkLabel(self, text="Power", font=("Helvetica", 30))
        self.song_title.grid(row=1, column = 0, columnspan=3, sticky="ew")

        # row 2
        song_image = None
        self.song_image = ctk.CTkLabel(self, image=song_image, text = "")
        self.song_image.grid(row=2, column = 1)

        # row 3
        self.song_artist = ctk.CTkLabel(self, text="Kanye West")
        self.song_artist.grid(row=3, column =0, columnspan = 3, sticky = "")

        # row 4
        self.song_link = ctk.CTkButton(self, text="play/pause", command = self.play_pause)
        self.song_link.grid(row=4, column = 1)

        self.deny_button = ctk.CTkButton(self,fg_color="red", text="no", command= self._deny_song, width=50)
        self.deny_button.grid(row=4,column=0,sticky="nsew", padx=5,pady=5)

        self.confirm_button = ctk.CTkButton(self, fg_color="green", text="yes", command= self._confirm_song, width=50)
        self.confirm_button.grid(row=4,column=2,sticky="nsew", padx=5,pady=5)

    def _confirm_song(self) -> None:
        self._confirm = True
    
    def _deny_song(self) -> None:
        self._confirm = False

    def play_pause(self) -> None:
        print("play", "pause")

    def _update_current_song(self, title: str, image: PhotoImage, artists: str) -> None:
        self.song_title.configure(text = title)
        self.song_title.grid(row=1, column=0, columnspan=3, sticky="ew")

        self.song_image.configure(image = image)
        self.song_image.grid(row=2, column=1)

        self.song_artist.configure(text = artists)
        self.song_artist.grid(row=3, column = 0, columnspan = 3, sticky = "ew")

    def user_input(self, title: str, image: PhotoImage, artists:str) -> bool:

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

    def __init__(self, master, graph: Graph, **kwargs):
        super().__init__(master, **kwargs)

        # stored in id:track pairs
        self.graph = graph

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.display_graph()
    
    def display_graph(self):
        """Display the PlaylistGraph on a Tkinter canvas"""
        canvas = ctk.CTkCanvas(self, bg="white", height=400, width=400)
        canvas.grid(row=0, column=0, sticky="nsew")

        # Retrieve song IDs and connections (edges)
        song_ids = self.graph.get_song_ids()
        edges = self.graph.get_connections()

        # Calculate positions for the nodes (simple circular layout)
        num_nodes = len(song_ids)
        angle_step = 360 / num_nodes
        positions = {}

        for i, song_id in enumerate(song_ids):
            angle = i * angle_step
            x = 200 + 100 * math.cos(math.radians(angle))
            y = 200 + 100 * math.sin(math.radians(angle))
            positions[song_id] = (x, y)
            canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="lightblue")
            canvas.create_text(x, y, text=tk.get_track(song_id).track_name)

        # Draw the edges (connections)
        for edge in edges:
            song_1, song_2 = edge
            x1, y1 = positions[song_1]
            x2, y2 = positions[song_2]
            canvas.create_line(x1, y1, x2, y2)

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
    # song_info = itunes.get_track_summary(track.artists, track.album_name)
    # song_photo = itunes.load_image_from_url(song_info["artwork"])

    # replace None with song_photo
    confirmation = app.music_frame.user_input(curr_song.track_name, None, curr_song.artists)
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

