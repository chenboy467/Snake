from tkinter import *
import random
import functools
import Game


class Launcher:
    def __init__(self, window):
        self.window = window
        self.window.title('Launcher')
        self.window.geometry('450x250')
        self.window.resizable(False, False)

        self.title = Label(window, text='Snake', font='Arial 48 bold')
        self.title.grid(row=0, columnspan=4, pady=10)

        for x in range(3):
            Button(window, text=('SLOW', 'MEDIUM', 'FAST')[
                   x], font='Ariel 18 bold', command=functools.partial(self.start, x), width=8).grid(row=1, column=x, columnspan=1, padx=10, pady=3)
        self.mode_select = Spinbox(window, values=(
            'Rabbits', 'Borderless', 'Bombs', 'Multifruit', 'Standard'), width=8)
        self.mode_select.grid(row=2, column=1, columnspan=1, pady=20)

    def start(self, speed):
        root = Tk()
        game_gui = Game.Game(root, speed, self.mode_select.get())
        root.mainloop()


root = Tk()
Launcher(root)
root.mainloop()
