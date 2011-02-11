__author__ = 'Tom'

import random
from Tkinter import *
from PIL import Image, ImageTk

class Minesweeper:
    def __init__(self, root, mines=10, size=9):
        self.root = root
        self.root.title("Minesweeper")
        self.frame = Frame(root)
        self.frame.grid()
        self.num_mines = mines
        self.size = size
        self.mines = self.get_mines()
        self.flags = []
        self.questions = []
        self.board = {}
        self.buttons = {}
        self.add_header()
        self.add_board()

    def add_header(self):
        frame = Frame(self.root)
        frame.grid()
        Label(frame, text="Timer:").grid(row=0, column=0)
        self.tv_timer = IntVar()
        self.time = Label(frame, textvariable=self.tv_timer)
        self.time.grid(row=0, column=1)
        Label(frame, text="Mines:").grid(row=0, column=2)
        self.tv_mines = IntVar()
        self.tv_mines.set(self.num_mines)
        Label(frame, textvariable=self.tv_mines).grid(row=0, column=3)

    def add_board(self):
        for i in range(self.size):
            for j in range(self.size):
                key = (i, j)
                if key in self.mines:
                    self.board[key] = 'm'
                    self.add_button(key, width=1, height=1, command=self.found_mine)
                else:
                    self.board[key] = str(self.get_mine_count(key))
                    self.add_button(key, width=1, height=1, command=lambda x=key:self.start_game(x))

    def start_game(self, space):
        for key, value in self.board.items():
            if value == '0':
                self.buttons[key].config(command=lambda x= key:self.found_space(x))
            elif value != 'm':
                self.buttons[key].config(command=lambda x= key:self.found_border(x))
        if self.board[space] == '0':
            self.found_space(space)
        elif self.board[space] != 'm':
            self.found_border(space)
        self.tick()

    def tick(self):
        self.tv_timer.set(self.tv_timer.get() + 1)
        self.timer = self.time.after(1000, self.tick)

    def mark_mine(self, arg):
        space = None
        for key, value in self.buttons.items():
            if value == arg.widget:
                space = key
        if space in self.questions:
            self.buttons[space].destroy()
            self.add_button(space, width=1, height=1, command=lambda x= space:self.found_space(x))
            self.questions.remove(space)
        elif space in self.flags:
            self.buttons[space].destroy()
            self.add_button(space, width=1, height=1, text="?")
            self.flags.remove(space)
            self.questions.append(space)
            self.tv_mines.set(self.tv_mines.get() + 1)
        else:
            photo = self.get_photo_image('flag.png')
            self.buttons[space].config(command=lambda: None, width=11, height=20, image=photo)
            self.buttons[space].image = photo
            self.flags.append(space)
            self.tv_mines.set(self.tv_mines.get() - 1)
        self.try_game_over()

    def add_button(self, key, **kwargs):
        self.buttons[key] = Button(self.frame, **kwargs)
        self.buttons[key].grid(row=key[0], column=key[1])
        self.buttons[key].bind("<Button-3>", self.mark_mine)

    def get_mines(self):
        mines = []
        while len(mines) < self.num_mines:
            mine = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))
            if mine not in mines:
                mines.append(mine)
        return mines

    def get_mine_count(self, key):
        count = 0
        for i in range(3):
            for j in range(3):
                try:
                    if (key[0] + i - 1, key[1] + j - 1) in self.mines:
                        count += 1
                except KeyError:
                    pass
        return count
    
    def found_space(self, key):
        self.board[key] = " "
        self.clear_button(key)
        for i in range(3):
            for j in range(3):
                space = (key[0] + i - 1, key[1] + j - 1)
                try:
                    if self.board[space] == '0':
                        self.found_space(space)
                    elif self.board[space] != 'm':
                        self.clear_button(space)
                except KeyError:
                    pass
        self.try_game_over()

    def clear_button(self, key):
        self.buttons[key].grid_forget()
        self.buttons[key] = Label(self.frame, text=self.board[key])
        self.buttons[key].grid(row=key[0], column=key[1])

    def found_mine(self):
        for i in range(self.size):
            for j in range(self.size):
                key = (i, j)
                if self.board[key] == 'm':
                    self.buttons[key].grid_forget()
                    photo = self.get_photo_image('mine.gif')
                    self.buttons[key] = Label(self.frame, image=photo)
                    self.buttons[key].image = photo
                    self.buttons[key].grid(row=i, column=j)
                if isinstance(self.buttons[key], Button):
                    self.buttons[key].config(command=lambda:None)
                    self.buttons[key].bind("<Button-3>", lambda x:None)
        self.time.after_cancel(self.timer)

    def found_border(self, key):
        self.buttons[key].grid_forget()
        self.buttons[key] = Label(self.frame, width=1, height=1, text=self.board[key])
        self.buttons[key].grid(row=key[0], column=key[1])
        self.try_game_over()

    def try_game_over(self):
        num_btn = 0
        mines_found = 0
        for i in range(self.size):
            for j in range(self.size):
                if isinstance(self.buttons[(i, j)], Button):
                    num_btn += 1
                    if self.board[(i, j)] == 'm' and (i, j) in self.flags:
                        mines_found += 1
        if num_btn ==  mines_found == self.num_mines: # print game over
            self.time.after_cancel(self.timer)
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
