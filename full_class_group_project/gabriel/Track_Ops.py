# functions that I will use to create the track

import pygame


X = 0
Y = 1

LINE_WIDTH = 3
LINE_HEIGHT = 3
BLACK = (0,0,0)

class Track():
    def __init__(self, win):
        self.lines = []   # will store (start, end) tuples
        self.curves = []
        self.win = win 

    def addLine(self, start, end):
        # Store the line as start and end points
        self.lines.append((start, end))

    def track_draw(self):
        for start, end in self.lines:
            pygame.draw.line(self.win, BLACK, start, end, LINE_WIDTH)

    def initialize(self):
        # Example line added
        self.addLine((0,0), (0,100))
