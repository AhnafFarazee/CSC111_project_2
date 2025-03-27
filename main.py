"""The main body of the python program"""

import tkinter as tk
from tkinter import ttk

# Create main window
root = tk.Tk()
root.title("Split View App")
root.geometry("600x400")

# Create a PanedWindow (Horizontal Split)
paned_window = tk.PanedWindow(root, orient=tk.HORIZONTAL)
paned_window.pack(fill=tk.BOTH, expand=True)

# Create Left Section (Frame)
left_frame = tk.Frame(paned_window, bg="lightblue", width=100)
paned_window.add(left_frame)

# Create Right Section (Frame)
right_frame = tk.Frame(paned_window, bg="lightgreen", width=100)
paned_window.add(right_frame)

# Add a label to each section
tk.Label(left_frame, text="Song", bg="lightblue", font=("Arial", 14)).pack(pady=20)
tk.Label(right_frame, text="Playlist", bg="lightgreen", font=("Arial", 14)).pack(pady=20)

root.mainloop()
