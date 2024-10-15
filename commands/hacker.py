#! /usr/bin/env python3

# Author: Joao S. O. Bueno
# gwidion@gmail.com
# GPL. v3.0
import time, math
global grid
grid = []

MAX_CASCADES = 600
MAX_COLS = 20
FRAME_DELAY = 0.05

MAX_SPEED  = 10

#import shutil, sys, time
from random import choice, randrange, paretovariate

CSI = "\x1b["
pr = lambda command: print("\x1b[", command, sep="", end="")
getchars = lambda start, end: [chr(i) for i in range(start, end)]

black, green, white = "30", "32", "37"

latin = getchars(0x30, 0x80)
greek = getchars(0x390, 0x3a0)
hebrew = getchars(0x5d0, 0x5eb)
cyrillic = getchars(0x400, 0x50)

#chars= latin + greek + hebrew + cyrillic
chars = greek
def pareto(limit):
    scale = lines // 2
    number = (paretovariate(1.16) - 1) * scale
    return max(0, limit - number)

def init(w,h):
    global cols, lines, grid, cascading
    #cols, lines = shutil.get_terminal_size()
    emptyRow = []
    grid = []
    cascading = set()
    cols = w
    lines = h
    for i in range(h):
        emptyRow.append(" ")
    for i in range(w):
        grid.append(emptyRow.copy())
    pr("?25l")  # Hides cursor
    pr("s")  # Saves cursor position

def end():
    pr("m")   # reset attributes
    pr("2J")  # clear screen
    pr("u")  # Restores cursor position
    pr("?25h")  # Show cursor

def print_at(char, x, y, color="", bright="0"):
    #pr("%d;%df" % (y, x))
    #pr(bright + ";" + color + "m")
    #print(char, end="", flush=True)
    try:
        grid[x][y] = char
    except IndexError:
        pass

def update_line(speed, counter, line):
    counter += 1
    if counter >= speed:
        line += 1
        counter = 0
    return counter, line

def cascade(col):
    speed = randrange(1, MAX_SPEED)
    espeed = randrange(1, MAX_SPEED)
    line = counter = ecounter = 0
    oldline = eline = -1
    erasing = False
    bright = "1"
    limit = pareto(lines)
    while True:
        counter, line = update_line(speed , counter, line)
        if randrange(10 * speed) < 1:
            bright = "0"
        if line > 1 and line <= limit and oldline != line:
            print_at(choice(chars),col, line-1, green, bright)
        if line < limit:
            print_at(choice(chars),col, line, white, "1")
        if erasing:
            ecounter, eline = update_line(espeed, ecounter, eline)
            print_at(" ",col, eline, black)
        else:
            erasing = randrange(line + 1) > (lines / 2)
            eline = 0
        yield None
        oldline = line
        if eline >= limit:
            print_at(" ", col, oldline, black)
            break
def rotate_matrix(m):
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0])-1,-1,-1)]
def main():
    global cascading
    cascading = set()
    added_new = True
    while True:
        while add_new(cascading): pass
        stopped = iterate(cascading)
        cascading.difference_update(stopped)
        rotatedGrid = rotate_matrix(grid)
        gridRows = []
        for x in range(len(rotatedGrid)):
            gridRows.append("".join(rotatedGrid[x]))
        final = '\n'.join([gridRows[i] for i in range((len(gridRows) - 1), -1, -1)])
        yield final

def add_new(cascading):
    global cols
    if randrange(MAX_CASCADES + 1) > len(cascading):
        col = randrange(cols)
        for i in range(randrange(MAX_COLS)):
            cascading.add(cascade((col + i) % cols))
        return True
    return False

def iterate(cascading):
    stopped = set()
    for c in cascading:
        try:
            next(c)
        except StopIteration:
            stopped.add(c)
    return stopped

def doit():
    try:
        init()
        mainCaller = main()
        while True:
            print(next(mainCaller))
    except KeyboardInterrupt:
        pass
    finally:
        end()

import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.bgGrid = []
        self.title('MPYCLI - Hacker')
        self.geometry('500x500')
        self.root = tk.Frame(self)
        self.bind("<Configure>", self.resize)
        self.font = tkfont.Font(family="Courier New", size=10, weight="normal")
        self.text = tk.Text(self.root, fg="#00FF00", font=self.font, background="black")
    
        init(*self.calcWidthHeight())
        self.mainCaller = main()
        self.textText = ""
        self.text.pack(fill=tk.BOTH, expand=True)
        self.root.config(bg='black')
        self.root.pack(fill=tk.BOTH, expand=True)
        self.after(100, self.call)
        self.showGrid()
        self.attributes("-fullscreen", True)
    def resize(self, _):
        init(*self.calcWidthHeight())
        self.text.insert('1.0', tk.END)
    def calcWidthHeight(self):
        width = self.winfo_width()
        height = self.winfo_height()
        if width <= 1:
            width = 500
        if height <= 1:
            height = 500
        width /= self.font.measure(".")
        height /= self.font.metrics('ascent')
        return math.floor(width - 0.25), math.floor(height - 0.25)
    def call(self):
        self.textText = next(self.mainCaller)
        self.showGrid()
        self.after(5, self.call)
    def showGrid(self):
        self.text.insert('1.0', self.textText)
if __name__ == "__main__":
    app = App()
    app.mainloop()