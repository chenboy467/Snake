from tkinter import *
import random
import functools
import Game


class Launcher:
    def __init__(self, window):
        self.window = window
        self.window.geometry('450x300')
        self.window.resizable(False, False)
        self.window.title('Launcher')

        Label(window, text='Snake', font='Arial 48 bold').grid(
            row=0, column=0, columnspan=3)
        for x in range(3):
            Button(window, text=('SLOW', 'MEDIUM', 'LARGE')[
                   x], command=functools.partial(self.start, x)).grid(row=1, column=x)
        self.mode_select = Spinbox(window, values=(
            'Rabbits', 'Borderless', 'Bombs', 'Multifruit', 'Standard'))
        self.mode_select.grid(row=2, column=1)

    def start(self, speed):
        root = Tk()
        game_gui = Game.Game(root, speed, self.mode_select.get())
        root.mainloop()


root = Tk()
Launcher(root)
root.mainloop()
