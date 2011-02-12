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
        self.size = size
        self.num_mines = mines
        self.board = {}
        self.buttons = {}
        self.add_menu_bar()
        self.add_header()
        self.new_game()

    def add_menu_bar(self):
        menu = Menu(self.root)
        file_menu = Menu(menu, tearoff=0)
        file_menu.add_command(label="New", command=self.new_game)
        #file_menu.add_command(label="Open", command=self.open_note)
        menu.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menu)

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

    def new_game(self):
        self.mines = self.get_mines()
        self.flags = []
        self.questions = []
        self.add_board()
        self.tv_mines.set(self.num_mines)
        if hasattr(self, "timer"):
            self.tv_timer.set(0)
            self.time.after_cancel(self.timer)
        print self

    def add_board(self):
        for key in self.buttons:
            self.buttons[key].destroy()
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
        self.tick()
        for key, value in self.board.items():
            self.configure_command(key)
        self.buttons[space].invoke()

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
            self.add_button(space, width=1, height=1)
            self.configure_command(space)
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

    def configure_command(self, key):
        if self.board[key] == 'm':
            self.buttons[key].config(command=self.found_mine)
        elif hasattr(self, "timer"):
            if self.board[key] == '0':
                self.buttons[key].config(command=lambda x= key:self.found_space(x))
            elif self.board[key] != 'm':
                self.buttons[key].config(command=lambda x= key:self.found_border(x))
        else:
            self.buttons[key].config(command=lambda x=key:self.start_game(x))

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
                if (key[0] + i - 1, key[1] + j - 1) in self.mines:
                    count += 1
        return count

    def found_space(self, key):
        self.board[key] = " "
        self.clear_button(key)
        for i in range(3):
            for j in range(3):
                space = (key[0] + i - 1, key[1] + j - 1)
                if space not in self.flags + self.questions:
                    try:
                        if self.board[space] == '0':
                            self.found_space(space)
                        elif self.board[space] != 'm':
                            self.clear_button(space)
                    except KeyError:
                        pass
        self.try_game_over()

    def clear_button(self, key):
        self.buttons[key].destroy()
        self.buttons[key] = Label(self.frame, text=self.board[key])
        self.buttons[key].grid(row=key[0], column=key[1])

    def found_mine(self):
        for i in range(self.size):
            for j in range(self.size):
                key = (i, j)
                if self.board[key] == 'm':
                    self.buttons[key].destroy()
                    photo = self.get_photo_image('mine.gif')
                    self.buttons[key] = Label(self.frame, image=photo)
                    self.buttons[key].image = photo
                    self.buttons[key].grid(row=i, column=j)
                if isinstance(self.buttons[key], Button):
                    self.buttons[key].config(command=lambda:None)
                    self.buttons[key].bind("<Button-3>", lambda x:None)
        if hasattr(self, "timer"):
            self.time.after_cancel(self.timer)

    def found_border(self, key):
        self.buttons[key].destroy()
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
