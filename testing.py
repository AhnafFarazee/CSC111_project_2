import customtkinter as ctk

import tkinter as tk

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Different Column Sizes per Row")

        # Row 1: Column weights (e.g., row 0)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)

        # Row 2: Column weights (e.g., row 1)
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        # Row 3: Column weights (e.g., row 2)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=2)

        # Create buttons for Row 1
        self.button1 = tk.Button(self, text="Button 1", bg="lightblue")
        self.button1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.button2 = tk.Button(self, text="Button 2", bg="lightgreen")
        self.button2.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        self.button3 = tk.Button(self, text="Button 3", bg="lightcoral")
        self.button3.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)

        # Create buttons for Row 2
        self.button4 = tk.Button(self, text="Button 4", bg="lightyellow")
        self.button4.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        self.button5 = tk.Button(self, text="Button 5", bg="lightpink")
        self.button5.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        self.button6 = tk.Button(self, text="Button 6", bg="lightgray")
        self.button6.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)

        # Create buttons for Row 3
        self.button7 = tk.Button(self, text="Button 7", bg="lightblue")
        self.button7.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        self.button8 = tk.Button(self, text="Button 8", bg="lightgreen")
        self.button8.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)

        self.button9 = tk.Button(self, text="Button 9", bg="lightcoral")
        self.button9.grid(row=2, column=2, sticky="nsew", padx=5, pady=5)

        # Adjust row/column configuration for dynamic resizing
        self.grid_rowconfigure(0, weight=1)  # Row 0 expands
        self.grid_rowconfigure(1, weight=1)  # Row 1 expands
        self.grid_rowconfigure(2, weight=1)  # Row 2 expands


if __name__ == "__main__":
    app = MyApp()
    app.geometry("600x400")  # Initial window size
    app.mainloop()

