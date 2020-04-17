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
        # self.mode_select = Spinbox(window, values=(
        #    'Rabbits', 'Borderless', 'Bombs', 'Multifruit', 'Standard'), width=8)
        self.modes = ['Standard', 'Borderless',
                      'Multifruit', 'Bombs', 'Rabbits']
        self.selected_mode = StringVar()
        self.selected_mode.set(self.modes[0])
        self.mode_select = OptionMenu(
            window, self.selected_mode, *self.modes)
        self.mode_select.grid(row=2, column=1, columnspan=1, pady=20)

        self.skins = ['Red', 'Orange', 'Yellow', 'Green', 'Blue',
                      'Purple', 'Brown', 'Gray', 'Rainbow', 'Invisible']
        self.selected_skin = StringVar()
        self.selected_skin.set(self.skins[3])
        self.skin_select = OptionMenu(
            window, self.selected_skin, *self.skins)
        self.skin_select.grid(row=2, column=0, columnspan=1, pady=20)

    def start(self, speed):
        root = Tk()
        game_gui = Game.Game(
            root, speed, self.selected_mode.get(), self.skins.index(self.selected_skin.get()))
        root.mainloop()


root = Tk()
Launcher(root)
root.mainloop()
