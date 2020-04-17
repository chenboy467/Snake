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
    rabbit_amount = 3
    rabbit_pos = []
    bomb_amount = 3

    game_paused = True

    def __init__(self, window, speed, mode, skin):
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
        self.skin = skin

        self.create_tiles()
        if self.mode == 'Rabbits':
            for x in range(self.rabbit_amount):
                self.spawn_item(-2)
        else:
            self.spawn_item(-1)
            if self.mode == 'Multifruit':
                for x in range(self.fruit_amount - 1):
                    self.spawn_item(-1)
            if self.mode == 'Bombs':
                for x in range(self.bomb_amount):
                    self.spawn_item(-3)
        self.window.bind('<Up>', functools.partial(self.turn, 'n'))
        self.window.bind('<Right>', functools.partial(self.turn, 'e'))
        self.window.bind('<Down>', functools.partial(self.turn, 's'))
        self.window.bind('<Left>', functools.partial(self.turn, 'w'))

        self.clock = Label(window, text='00:00', font='Arial 36')
        self.clock.place(relx=0.75, rely=0.1, anchor=NW)
        self.score = Label(window, text='0', font='Arial 36')
        self.score.place(relx=0.75, rely=0.2, anchor=NW)
        self.start_button = Button(window, text='START', font='Arial 18 bold',
                                   command=self.start, width=8)
        self.start_button.place(relx=0.75, rely=0.8, anchor=SW)
        Button(window, text='RESET', font='Arial 18 bold',
               command=self.reset, width=8).place(relx=0.75, rely=0.9, anchor=SW)

        self.tiles[self.snake_pos[0]][self.snake_pos[1]].configure(bg=(
            'red4', 'DarkOrange4', 'yellow4', 'green4', 'DodgerBlue4', 'DarkOrchid4', 'sienna4', 'grey30', 'red', (('gray85', 'white')[(self.snake_pos[0]+self.snake_pos[1]) % 2]))[self.skin])

    def timer(self):
        current_time = time.time()
        delta_time = (current_time - self.start_time)
        minutes = int(delta_time//60)
        seconds = int(delta_time % 60)
        if delta_time < 3600 and not self.game_paused:
            self.clock.config(
                text='{0:02d}:{1:02d}'.format(minutes, seconds))
            self.window.after(100, self.timer)

    def toggle_fullscreen(self, event):
        self.window.attributes(
            '-fullscreen', not self.window.attributes('-fullscreen'))

    def start(self):
        self.start_button.config(state='disabled')
        self.game_paused = False
        self.start_time = time.time()
        self.timer()
        self.move()
        if self.mode == 'Rabbits':
            self.rabbit_move()

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
                for x in range(self.col_length):
                    for y in range(self.row_length):
                        if self.tile_values[x][y] > 0:
                            self.tiles[x][y].configure(bg='snow3')
                        elif self.tile_values[x][y] == 0:
                            self.tiles[x][y].configure(
                                bg=('gray85', 'white')[(x+y) % 2])
                self.tiles[(self.snake_pos[0] - self.directions[self.direction][1]) % self.row_length][
                    (self.snake_pos[1] - self.directions[self.direction][0]) % self.col_length].configure(bg='snow4')
                return

        # running into itself
        if self.tile_values[self.snake_pos[0]][self.snake_pos[1]] > 0:
            self.game_paused = True
            for x in range(self.col_length):
                for y in range(self.row_length):
                    if self.tile_values[x][y] > 0:
                        self.tiles[x][y].configure(bg='snow3')
                    elif self.tile_values[x][y] == 0:
                        self.tiles[x][y].configure(
                            bg=('gray85', 'white')[(x+y) % 2])
            self.tiles[(self.snake_pos[0] - self.directions[self.direction][1]) % self.row_length][
                (self.snake_pos[1] - self.directions[self.direction][0]) % self.col_length].configure(bg='snow4')
            return

        # eating fruit
        if self.tile_values[self.snake_pos[0]][self.snake_pos[1]] == -1 or self.tile_values[self.snake_pos[0]][self.snake_pos[1]] == -2:
            self.snake_length += 1
            if self.mode == 'Rabbits':
                for x in self.rabbit_pos:
                    if x[0] == self.snake_pos[0] and x[1] == self.snake_pos[1]:
                        x[0] = -1
                        x[1] = -1
                if (self.row_length*self.col_length - self.snake_length) >= self.rabbit_amount:
                    self.spawn_item(-2)
            else:
                if (self.row_length*self.col_length - self.snake_length) >= self.fruit_amount:
                    self.spawn_item(-1)
            for x in range(self.col_length):
                for y in range(self.row_length):
                    if self.tile_values[x][y] > 0:
                        self.tile_values[x][y] += 1
            if self.snake_length % 3 == 0 and self.mode == 'Bombs':
                self.spawn_item(-3)

        # eating bomb
        if self.tile_values[self.snake_pos[0]][self.snake_pos[1]] == -3:
            self.game_paused = True
            for x in range(self.col_length):
                for y in range(self.row_length):
                    if self.tile_values[x][y] > 0:
                        self.tiles[x][y].configure(bg='snow3')
                    elif self.tile_values[x][y] == 0:
                        self.tiles[x][y].configure(
                            bg=('gray85', 'white')[(x+y) % 2])
            self.tiles[self.snake_pos[0]
                       ][self.snake_pos[1]].configure(bg='snow4')
            return

        # snake body update
        for x in range(self.col_length):
            for y in range(self.row_length):
                # self.tiles[x][y].configure(bg='green')
                self.tile_values[x][y] -= (self.tile_values[x][y] > 0)
                if self.tile_values[x][y] > 0:
                    self.tiles[x][y].configure(bg='green3')
                    # TODO: MAKE SKINS APPLY FOR WHOLE BODY
                elif self.tile_values[x][y] == 0:
                    self.tiles[x][y].configure(
                        bg=('gray85', 'white')[(x+y) % 2])
                # else:
                    # self.tiles[x][y].configure(bg='red')

        self.tile_values[self.snake_pos[0]
                         ][self.snake_pos[1]] = self.snake_length
        self.tiles[self.snake_pos[0]][self.snake_pos[1]].configure(bg='green4')
        self.window.after(400 - self.speed*100, self.move)

        # updates the score
        self.score.config(text=str(self.snake_length - 3))

        if self.snake_length == self.row_length * self.col_length:
            self.game_paused = True

    def turn(self, direction, event):
        if self.game_paused and (self.snake_length > 3 or not (self.snake_pos[0] == 7 and self.snake_pos[1] == 3)):
            return
        if self.game_paused:
            self.direction = direction
            self.prev_direction = direction
            self.start()
            return
        if (self.prev_direction == 'n' and direction == 's') or (self.prev_direction == 'e' and direction == 'w') or (self.prev_direction == 's' and direction == 'n') or (self.prev_direction == 'w' and direction == 'e'):
            return
        self.direction = direction

    def rabbit_move(self):
        if self.game_paused:
            return

        for x in self.rabbit_pos:
            if not x[0] == -1:
                # if abs(x[0] - self.snake_pos[0]) < 4 or abs(x[1] - self.snake_pos[1]) < 4:
                # pass
                # else:
                if True:
                    rabbit_direction = ('n', 'e', 's', 'w')[
                        random.randint(0, 3)]
                    if abs(x[0] - self.snake_pos[0]) < 6 or abs(x[1] - self.snake_pos[1]) < 6:
                        if abs(x[0] - self.snake_pos[0]) > abs(x[1] - self.snake_pos[1]):
                            if x[0] - self.snake_pos[0] < 0:
                                rabbit_direction = 'w'
                            elif x[0] - self.snake_pos[0] > 0:
                                rabbit_direction = 'e'
                        elif abs(x[0] - self.snake_pos[0]) < abs(x[1] - self.snake_pos[1]):
                            if x[1] - self.snake_pos[1] < 0:
                                rabbit_direction = 'n'
                            elif x[1] - self.snake_pos[1] > 0:
                                rabbit_direction = 's'
                        else:
                            if x[0] - self.snake_pos[0] < 0 and x[1] - self.snake_pos[1] < 0:
                                rabbit_direction = ('e', 's')[
                                    random.randint(0, 1)]
                            elif x[0] - self.snake_pos[0] > 0 and x[1] - self.snake_pos[1] < 0:
                                rabbit_direction = ('w', 's')[
                                    random.randint(0, 1)]
                            elif x[0] - self.snake_pos[0] < 0 and x[1] - self.snake_pos[1] > 0:
                                rabbit_direction = ('e', 'n')[
                                    random.randint(0, 1)]
                            elif x[0] - self.snake_pos[0] > 0 and x[1] - self.snake_pos[1] > 0:
                                rabbit_direction = ('w', 'n')[
                                    random.randint(0, 1)]
                    else:
                        rabbit_direction = ('n', 'e', 's', 'w')[
                            random.randint(0, 3)]
                    path_clear = False
                    while path_clear == False:
                        path_clear = True
                        while (x[0] + self.directions[rabbit_direction][1] < 0) or (x[0] + self.directions[rabbit_direction][1] >= self.row_length) or (x[1] + self.directions[rabbit_direction][0] < 0) or (x[1] + self.directions[rabbit_direction][0] >= self.col_length):
                            rabbit_direction = ('n', 'e', 's', 'w')[
                                random.randint(0, 3)]
                            path_clear = False
                        if (self.tile_values[x[0] + self.directions[rabbit_direction][1]][x[1] + self.directions[rabbit_direction][0]]):
                            rabbit_direction = ('n', 'e', 's', 'w')[
                                random.randint(0, 3)]
                            path_clear = False
                    self.tile_values[x[0]][x[1]] = 0
                    self.tiles[x[0]][x[1]].configure(
                        bg=('gray85', 'white')[(x[0]+x[1]) % 2])
                    x[0] = x[0] + self.directions[rabbit_direction][1]
                    x[1] = x[1] + self.directions[rabbit_direction][0]
                    self.tile_values[x[0]][x[1]] = -2
                    self.tiles[x[0]][x[1]].configure(bg='pink')

        # rabbit body update
        for x in range(self.col_length):
            for y in range(self.row_length):
                if self.tile_values[x][y] == -2:
                    self.tiles[x][y].configure(bg='pink')

        self.window.after((400 - self.speed*100) * 2, self.rabbit_move)

    def spawn_item(self, item_index):
        item_pos = [random.randint(
            0, self.row_length - 1), random.randint(0, self.col_length - 1)]
        if item_index == -3:
            while self.tile_values[item_pos[0]][item_pos[1]] and (abs(item_pos[0] - self.snake_pos[0]) > 2 or abs(item_pos[1] - self.snake_pos[1]) > 2):
                item_pos = [random.randint(
                    0, self.row_length - 1), random.randint(0, self.col_length - 1)]
        else:
            while self.tile_values[item_pos[0]][item_pos[1]]:
                item_pos = [random.randint(
                    0, self.row_length - 1), random.randint(0, self.col_length - 1)]
        self.tile_values[item_pos[0]][item_pos[1]] = item_index
        self.tiles[item_pos[0]][item_pos[1]].configure(
            bg=(None, 'red', 'pink', 'black')[item_index * -1])
        if item_index == -2:
            if len(self.rabbit_pos) < self.rabbit_amount:
                self.rabbit_pos.append([item_pos[0], item_pos[1]])
            else:
                for x in self.rabbit_pos:
                    if x[0] == -1:
                        x[0] = item_pos[0]
                        x[1] = item_pos[1]

    def reset(self):
        self.snake_length = 3
        self.snake_pos = [7, 3]
        self.direction = 'e'
        self.prev_direction = self.direction
        self.tiles = []
        self.game_paused = True
        self.create_tiles()
        self.rabbit_pos = []
        if self.mode == 'Rabbits':
            for x in range(self.rabbit_amount):
                self.spawn_item(-2)
        else:
            self.spawn_item(-1)
            if self.mode == 'Multifruit':
                for x in range(self.fruit_amount - 1):
                    self.spawn_item(-1)
            if self.mode == 'Bombs':
                for x in range(self.bomb_amount):
                    self.spawn_item(-3)
        self.tiles[self.snake_pos[0]][self.snake_pos[1]].configure(bg='green4')
        self.start_time = time.time()
        self.clock.config(text='00:00')
        self.score.config(text='0')
        self.start_button.config(state='active')
