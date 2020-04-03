from tkinter import *
import random
import functools
import time


class Game:

    rows = 15
    cols = 15

    snake_length = 4
    snake_pos = [7, 3]
    directions = {
        'n': (0, -1),
        'e': (1, 0),
        's': (0, 1),
        'w': (-1, 0)
    }
    direction = 'e'
    prev_direction = direction

    tiles = []
    apple_locations = set()

    def __init__(self, window, speed, mode):
        self.window = window
        self.window.title('Snake')
        self.window.geometry("1000x666".format(
            self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.window.resizable(False, False)
        self.window.bind('<Escape>', self.toggle_fullscreen)
        self.canvas = Canvas(window)
        self.canvas.place(relx=0.4, rely=0.5, anchor=CENTER)
        self.speed = speed
        self.mode = mode

        self.create_tiles()
        self.move()
        self.window.bind('<Up>', functools.partial(self.turn, 'n'))
        self.window.bind('<Right>', functools.partial(self.turn, 'e'))
        self.window.bind('<Down>', functools.partial(self.turn, 's'))
        self.window.bind('<Left>', functools.partial(self.turn, 'w'))

    def toggle_fullscreen(self, event):
        self.window.attributes(
            '-fullscreen', not self.window.attributes('-fullscreen'))

    def create_tiles(self):
        self.tile_values = [
            [0 for x in range(self.cols)] for y in range(self.rows)]
        self.tiles = [[0 for x in range(self.cols)]
                      for y in range(self.rows)]
        for x in range(self.rows):
            for y in range(self.cols):
                self.tiles[x][y] = Frame(
                    self.canvas, bg=('grey', 'white')[(x+y) % 2], height=40, width=40)
                self.tiles[x][y].grid(
                    row=x, column=y, sticky='ew')

    def move(self):
        self.prev_direction = self.direction
        for x in range(self.rows):
            for y in range(self.cols):
                # self.tiles[x][y].configure(bg='green')
                self.tile_values[x][y] -= (self.tile_values[x][y] > 0)
                if self.tile_values[x][y]:
                    self.tiles[x][y].configure(bg='green3')
                else:
                    self.tiles[x][y].configure(
                        bg=('gray85', 'white')[(x+y) % 2])
        self.snake_pos = [self.snake_pos[0] + self.directions[self.direction][1], self.snake_pos[1] +
                          self.directions[self.direction][0]]

        self.tile_values[self.snake_pos[0]
                         ][self.snake_pos[1]] = self.snake_length
        self.tiles[self.snake_pos[0]][self.snake_pos[1]].configure(bg='green4')
        self.window.after(400 - self.speed*100, self.move)

    def turn(self, direction, event):
        if (self.prev_direction == 'n' and direction == 's') or (self.prev_direction == 'e' and direction == 'w') or (self.prev_direction == 's' and direction == 'n') or (self.prev_direction == 'w' and direction == 'e'):
            return
        self.direction = direction
