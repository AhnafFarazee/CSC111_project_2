"""The main body of the python program"""
from tkinter import *
import customtkinter as ctk
import random

from datatypes import *

class MusicFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

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
        self.song_title = ctk.CTkLabel(self, text="Power")
        self.song_title.grid(row=1, column = 1)

        # row 2
        song_image = PhotoImage(file="test.png")
        self.song_image = ctk.CTkLabel(self, image=song_image, text = "")
        self.song_image.grid(row=2, column = 1)

        # row 3
        self.song_artist = ctk.CTkLabel(self, text="Kanye West")
        self.song_artist.grid(row=3, column =1)

        # row 4
        self.button3 = ctk.CTkButton(self, text="play/pause", command = self.play_pause)
        self.button3.grid(row=4, column = 1)

        self.button1 = ctk.CTkButton(self,fg_color="red", text="no", command=self.deny_song, width=50)
        self.button1.grid(row=4,column=0,sticky="nsew", padx=5,pady=5)

        self.button2 = ctk.CTkButton(self, fg_color="green", text="yes", command=self.confirm_song, width=50)
        self.button2.grid(row=4,column=2,sticky="nsew", padx=5,pady=5)

    def play_pause(self) -> None:
        print("play", "pause")

    def confirm_song(self) -> None:
        print("add song")

    def deny_song(self) -> None:
        print("remove song")

class Visualizer(ctk.CTkFrame):

    def __init__(self, master, graph: Graph):
        super().__init__(master, graph)

        # stored in id:track pairs
        self.graph = graph

        self.canvas = ctk.CTkCanvas(self, width=400, height=600, bg="white")
        self.canvas.pack()

        self.node_positions = {}
        self.draw_graph()
    
    def draw_graph():
        pass
        




class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.minsize(height=400,width=600)
        self.title("PlayList Generator")

        self.columnconfigure(0,weight=1)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=1)

        self.left_frame = MusicFrame(self)
        self.left_frame.grid(row=0,column=0,sticky="nsew", padx=5,pady=5)

        self.right_frame = ctk.CTkFrame(self, fg_color="lightcoral", border_width=2)
        self.right_frame.grid(row=0,column=1,sticky="nsew", padx=5,pady=5)

    def decide_song(item: list[Track]) -> list[Track]:
        pass


# runs app dont touch
app = App()
app.mainloop()

