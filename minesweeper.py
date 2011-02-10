__author__ = 'Tom'

import random
from Tkinter import *
from PIL import Image, ImageTk

class Minesweeper:
    def __init__(self, root, mines=10, size=9):
        root.title("Minesweeper")
        self.mines = mines
        self.size = size
        self.flags = []
        self.frame = Frame(root)
        self.frame.grid()
        self.board = {}
        self.buttons = {}
        self.add_board()
        self.add_mines()
        self.add_borders()
        print self
        f = Frame(root)
        f.grid()
        Button(f, text="print", command=self.print_board).grid()

    def print_board(self):
        print self

    def add_board(self):
        for i in range(self.size):
            for j in range(self.size):
                self.board[(i, j)] = '0'
                self.buttons[(i, j)] = Button(self.frame, width=1, height=1, command=lambda x= (i, j):self.found_space(x))
                self.buttons[(i, j)].grid(row=i, column=j)
                self.buttons[(i, j)].bind("<Button-3>", self.mark_mine)

    def mark_mine(self, arg):
        space = None
        for key, value in self.buttons.items():
            if value == arg.widget:
                space = key
        if space not in self.flags:
            photo = self.get_photo_image('flag.png')
            self.buttons[space].config(command=lambda: None, width=11, height=20, image=photo)
            self.buttons[space].image = photo
            self.flags.append(space)
        else:
            self.buttons[space].destroy()
            self.buttons[space] = Button(self.frame, width=1, height=1, command=lambda x= space:self.found_space(x))
            self.buttons[space].grid(row=space[0], column=space[1])
            self.buttons[space].bind("<Button-3>", self.mark_mine)
            self.flags.remove(space)
        self.has_game_over()

    def add_mines(self):
        mines = 0
        while mines < self.mines:
            mine = (random.randint(0, self.size - 3), random.randint(0, self.size - 3))
            if self.board[mine] != 'm':
                self.board[mine] = 'm'
                self.buttons[mine].config(command=self.found_mine)
                mines += 1

    def add_borders(self):
        for row in range(self.size):
            for col in range(self.size):
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
                        self.buttons[(row, col)].config(command=lambda x= (row, col):self.found_border(x))

    def found_space(self, space):
        row, col = space[0], space[1]
        self.board[(row, col)] = " "
        self.buttons[(row, col)].grid_forget()
        self.buttons[(row, col)] = Label(self.frame, text=self.board[(row, col)])
        self.buttons[(row, col)].grid(row=row, column=col)
        for i in range(3):
            for j in range(3):
                space = (row + i - 1, col + j - 1)
                try:
                    if self.board[space] == '0':
                        self.found_space(space)
                    elif self.board[space] != 'm':
                        self.buttons[space].grid_forget()
                        self.buttons[space] = Label(self.frame, text=self.board[space])
                        self.buttons[space].grid(row=space[0], column=space[1])
                except KeyError:
                    pass
        self.has_game_over()

    def found_mine(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[(i, j)] == 'm':
                    self.buttons[(i, j)].grid_forget()
                    photo = self.get_photo_image('mine.gif')
                    self.buttons[(i, j)] = Label(self.frame, image=photo)
                    self.buttons[(i, j)].image = photo
                    self.buttons[(i, j)].grid(row=i, column=j)
                if isinstance(self.buttons[(i, j)], Button):
                    self.buttons[(i, j)].config(command=lambda:None)
                    self.buttons[(i, j)].bind("<Button-3>", lambda x:None)

    def found_border(self, space):
        self.buttons[space].grid_forget()
        self.buttons[space] = Label(self.frame, width=1, height=1, text=self.board[space])
        self.buttons[space].grid(row=space[0], column=space[1])
        self.has_game_over()

    def has_game_over(self):
        num_btn = 0
        mines_found = 0
        for i in range(self.size):
            for j in range(self.size):
                if isinstance(self.buttons[(i, j)], Button):
                    num_btn += 1
                    if self.board[(i, j)] == 'm' and (i, j) in self.flags:
                        mines_found += 1
        if num_btn ==  mines_found == self.mines: # print game over
            print "GAME OVER!"

    def get_photo_image(self, image):
        return ImageTk.PhotoImage(Image.open(image))

    def __str__(self):
        s = ""
        for i in range(self.size):
            for j in range(self.size):
                s += self.board[(i, j)] + "\t"
            s += "\n"
        return s

if __name__ == "__main__":
    root = Tk()
    minesweeper = Minesweeper(root)
    root.mainloop()
