__author__ = 'Tom'

import random
from Tkinter import *

class Minesweeper:
    def __init__(self, root):
        self.frame = Frame(root)
        self.frame.grid()
        self.board = {}
        self.buttons = {}
        self.add_board()
        self.add_mines()
        self.add_borders()
        self.print_board()
        f = Frame(root)
        f.grid()
        Button(f, text="print", command=self.print_board).grid()

    def print_board(self):
        print self

    def add_board(self):
        for i in range(9):
            for j in range(9):
                self.board[(i, j)] = '0'
                self.buttons[(i, j)] = Button(self.frame, width=1, height=1, command=lambda x= (i, j):self.found_space(x))
                self.buttons[(i, j)].grid(row=i, column=j)

    def add_mines(self):
        mines = 0
        while mines < 10:
            mine = (random.randint(0, 8), random.randint(0, 8))
            if self.board[mine] != 'm':
                self.board[mine] = 'm'
                self.buttons[mine].config(command=self.found_mine)
                mines += 1

    def add_borders(self):
        for row in range(9):
            for col in range(9):
                if self.board[(row, col)] == '0':
                    mine_count = 0
                    for i in range(3):
                        for j in range(3):
                            try:
                                if self.board[(row + i - 1, col + j - 1)] == 'm':
                                    mine_count += 1
                            except KeyError:
                                pass
                    if mine_count > 0:
                        self.board[(row, col)] = str(mine_count)
                        self.buttons[(row, col)].config(command=self.found_border)

    def found_space(self, to):
        i, j = to[0], to[1]
        self.board[(i, j)] = ''
        self.buttons[(i, j)].grid_forget()
        for space in [(i - 1, j - 1), (i - 1, j), (i - 1, j + 1), (i, j + 1),
                  (i + 1, j + 1), (i + 1, j), (i + 1, j - 1), (i, j - 1)]:
            try:
                if self.board[space] == '0':
                    self.found_space(space)
                elif self.board[space] != 'm':
                    self.buttons[space].grid_forget()
                    self.buttons[space] = Label(self.frame, width=1, height=1, text=self.board[space])
                    self.buttons[space].grid(row=space[0], column=space[1])
            except KeyError:
                pass

    def found_mine(self):
        pass

    def found_border(self):
        pass

    def __str__(self):
        s = ""
        for i in range(9):
            for j in range(9):
                s += self.board[(i, j)] + "\t"
            s += "\n"
        return s

if __name__ == "__main__":
    root = Tk()
    minesweeper = Minesweeper(root)
    root.mainloop()
