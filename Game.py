from tkinter import *
import random
import functools


class Game:
    def __init__(self, window, size, mode):
        self.window = window
        self.window.geometry('450x300')
        self.window.resizable(False, False)
        self.window.title('Snake')
        self.size = size
        self.mode = mode
