import tkinter as tk

class MessageAlert:
    def __init__(self, master, message):
        self.master = master
        self.frame = tk.Frame(self.master)

        self.master.title("")

        self.label = tk.Label(self.frame, text = message)
        self.label.pack()

        self.quitButton = tk.Button(self.frame, text = 'OK', command = master.destroy)
        self.quitButton.pack()

        self.frame.pack()