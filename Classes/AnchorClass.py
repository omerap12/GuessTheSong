# Anchor class, fields: player
from tkinter import messagebox


class Anchor:
    # constructor.
    def __init__(self, gamePlayer):
        self.player = gamePlayer

    # wining message
    def winMessage(self):
        messagebox.showinfo("Win!", "Score: " + str(self.player.getScore()))


    # wining message
    def loseMessage(self):
        messagebox.showinfo("Lost!", "Score: " + str(self.player.getScore()))

