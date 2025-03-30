import tkinter as tk
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Function to play music
def play_music():
    pygame.mixer.music.load("test.mp3", "mp3")  # Replace with the path to your music file
    pygame.mixer.music.play(loops=0, start=0.0)  # Play the music

# Function to stop music
def stop_music():
    pygame.mixer.music.stop()

# Function to pause music
def pause_music():
    pygame.mixer.music.pause()

# Function to unpause music
def unpause_music():
    pygame.mixer.music.unpause()

# Create Tkinter window
root = tk.Tk()
root.title("Music Player")

# Create play button
play_button = tk.Button(root, text="Play", command=play_music)
play_button.pack(pady=10)

# Create stop button
stop_button = tk.Button(root, text="Stop", command=stop_music)
stop_button.pack(pady=10)

# Create pause button
pause_button = tk.Button(root, text="Pause", command=pause_music)
pause_button.pack(pady=10)

# Create unpause button
unpause_button = tk.Button(root, text="Unpause", command=unpause_music)
unpause_button.pack(pady=10)

# Run Tkinter main loop
root.mainloop()
