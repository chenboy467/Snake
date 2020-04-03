from tkinter import *
import random
import functools
import time


class Game:

    row_length = 15
    col_length = 15

    snake_length = 3
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
    fruit_amount = 5

    game_paused = False

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
        self.spawn_fruit()
        if self.mode == 'Multifruit':
            for x in range(self.fruit_amount - 1):
                self.spawn_fruit()
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
            [0 for x in range(self.row_length)] for y in range(self.col_length)]
        self.tiles = [[0 for x in range(self.row_length)]
                      for y in range(self.col_length)]
        for x in range(self.col_length):
            for y in range(self.row_length):
                self.tiles[x][y] = Frame(
                    self.canvas, bg=('gray85', 'white')[(x+y) % 2], height=40, width=40)
                self.tiles[x][y].grid(
                    row=x, column=y, sticky='ew')

    def move(self):
        if self.game_paused:
            return

        self.prev_direction = self.direction

        # change snake position
        if self.mode == 'Borderless':
            self.snake_pos = [(self.snake_pos[0] + self.directions[self.direction][1]) % self.row_length,
                              (self.snake_pos[1] + self.directions[self.direction][0]) % self.col_length]
        else:
            self.snake_pos = [self.snake_pos[0] + self.directions[self.direction]
                              [1], self.snake_pos[1] + self.directions[self.direction][0]]

            if (self.snake_pos[0] < 0) or (self.snake_pos[0] >= self.row_length) or (self.snake_pos[1] < 0) or (self.snake_pos[1] >= self.col_length):
                self.game_paused = True
                return

        # running into itself
        if self.tile_values[self.snake_pos[0]][self.snake_pos[1]] > 0:
            self.game_paused = True
            return

        # eating fruit
        if self.tile_values[self.snake_pos[0]][self.snake_pos[1]] < 0:
            self.snake_length += 1
            if (self.row_length*self.col_length - self.snake_length) >= self.fruit_amount:
                self.spawn_fruit()
            for x in range(self.col_length):
                for y in range(self.row_length):
                    if self.tile_values[x][y] > 0:
                        self.tile_values[x][y] += 1

        # snake body update
        for x in range(self.col_length):
            for y in range(self.row_length):
                # self.tiles[x][y].configure(bg='green')
                self.tile_values[x][y] -= (self.tile_values[x][y] > 0)
                if self.tile_values[x][y] > 0:
                    self.tiles[x][y].configure(bg='green3')
                elif self.tile_values[x][y] == 0:
                    self.tiles[x][y].configure(
                        bg=('gray85', 'white')[(x+y) % 2])
                # else:
                    # self.tiles[x][y].configure(bg='red')

        self.tile_values[self.snake_pos[0]
                         ][self.snake_pos[1]] = self.snake_length
        self.tiles[self.snake_pos[0]][self.snake_pos[1]].configure(bg='green4')
        self.window.after(400 - self.speed*100, self.move)

    def turn(self, direction, event):
        if (self.prev_direction == 'n' and direction == 's') or (self.prev_direction == 'e' and direction == 'w') or (self.prev_direction == 's' and direction == 'n') or (self.prev_direction == 'w' and direction == 'e'):
            return
        self.direction = direction

    def spawn_fruit(self):
        fruit_pos = [random.randint(
            0, self.row_length - 1), random.randint(0, self.col_length - 1)]
        while self.tile_values[fruit_pos[0]][fruit_pos[1]]:
            fruit_pos = [random.randint(
                0, self.row_length - 1), random.randint(0, self.col_length - 1)]
        self.tile_values[fruit_pos[0]][fruit_pos[1]] = -1
        self.tiles[fruit_pos[0]][fruit_pos[1]].configure(bg='red')
