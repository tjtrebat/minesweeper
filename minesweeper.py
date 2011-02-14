__author__ = 'Tom'

import random
from Tkinter import *
from PIL import Image, ImageTk
import cPickle as pickle

class Minesweeper:
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper")
        self.frame = Frame(root)
        self.frame.grid()
        self.size = (9,) * 2
        self.num_mines = 10
        self.winning_streak = 0
        self.losing_streak = 0
        self.buttons = {}
        self.add_menu_bar()
        self.add_header()
        self.new_game()
        self.get_stats()

    def get_stats(self):
        try:
            self.stats = pickle.load(open('stats.p'))
        except IOError:
            d = {"games_played": 0, "games_won": 0, "win_percentage": 0,
                                       "longest_winning_streak": 0, "longest_losing_streak": 0, "current_streak": "0 losses"}
            self.stats = {"Beginner": d, "Intermediate": d.copy(), "Advanced": d.copy()}

    def save_stats(self):
        if self.level != "Custom":
            if self.stats[self.level]["longest_winning_streak"] < self.winning_streak:
                self.stats[self.level]["longest_winning_streak"] = self.winning_streak
            if self.stats[self.level]["longest_losing_streak"] < self.losing_streak:
                self.stats[self.level]["longest_losing_streak"] = self.losing_streak
            pickle.dump(self.stats, open('stats.p', 'w+'))
            
    def add_menu_bar(self):
        menu = Menu(self.root)
        file_menu = Menu(menu, tearoff=0)
        file_menu.add_command(label="New", command=self.new_game)
        file_menu.add_command(label="Statistics", command=self.statistics)
        file_menu.add_separator()
        self.level = "Beginner"
        self.levels = {"Beginner": BooleanVar(), "Intermediate": BooleanVar(), "Advanced": BooleanVar(), "Custom": BooleanVar()}
        file_menu.add_checkbutton(label="Beginner", variable=self.levels["Beginner"], command=lambda x= "Beginner":self.new_game(level=x))
        file_menu.add_checkbutton(label="Intermediate", variable=self.levels["Intermediate"], command=lambda x= "Intermediate":self.new_game(level=x))
        file_menu.add_checkbutton(label="Advanced", variable=self.levels["Advanced"], command=lambda x= "Advanced":self.new_game(level=x))
        file_menu.add_command(label="Custom", command=self.custom_level)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
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

    def new_game(self, level=None):
        if level is not None:
            self.levels[self.level].set(False)
            self.level = level
            self.size = self.get_size()
            self.num_mines = self.get_num_mines()
            if self.level == "Custom":
                self.custom.destroy()
            if self.level != level:
                self.winning_streak = 0
                self.losing_streak = 0
        self.levels[self.level].set(True)
        self.mines = self.get_mines()
        self.flags = []
        self.questions = []
        self.add_board()
        self.tv_mines.set(self.num_mines)
        if hasattr(self, "timer"):
            self.tv_timer.set(0)
            self.time.after_cancel(self.timer)

    def statistics(self):
        self.stat_root = Tk()
        frame = Frame(self.stat_root, padx=10, pady=10)
        frame.grid()
        l = Listbox(frame)
        l.insert(END, "Beginner")
        l.insert(END, "Intermediate")
        l.insert(END, "Advanced")
        l.selection_set(0)
        l.bind("<ButtonRelease-1>", self.set_stat_labels)
        l.grid(row=0, column=0)
        best_times = LabelFrame(frame, padx=75, text="Best Times")
        self.times = [StringVar() for i in range(5)]
        for time in self.times:
            Label(best_times, textvariable=self.times).grid()
        best_times.grid(padx=20, row=0, column=1, sticky="N")
        results = Frame(frame)
        results.grid(row=0, column=2)
        self.stat_labels = self.get_stat_labels(results)
        Label(results, text="Games played:").grid(row=0, column=0, sticky="W")
        self.stat_labels["games_played"].grid(row=0, column=1)
        Label(results, text="Games won:").grid(row=1, column=0, sticky="W")
        self.stat_labels["games_won"].grid(row=1, column=1)
        Label(results, text="Win percentage:").grid(row=2, column=0, sticky="W")
        self.stat_labels["win_percentage"].grid(row=2, column=1)
        Label(results, text="Longest winning streak:").grid(row=3, column=0, sticky="W")
        self.stat_labels["longest_winning_streak"].grid(row=3, column=1)
        Label(results, text="Longest losing streak:").grid(row=4, column=0, sticky="W")
        self.stat_labels["longest_losing_streak"].grid(row=4, column=1)
        Label(results, text="Current streak:").grid(row=5, column=0, sticky="W")
        self.stat_labels["current_streak"].grid(row=5, column=1)
        self.set_stat_labels(l.get(l.curselection()[0]))

    def get_stat_labels(self, frame):
        labels = {}
        for key in self.stats["Beginner"].keys():
            labels[key] = Label(frame)
        return labels

    def set_stat_labels(self, level):
        if isinstance(level, Event):
            level = level.widget.get(level.widget.curselection()[0])
        for key, label in self.stat_labels.items():
            text = self.stats[level][key]
            if key == "win_percentage":
                text = "%d%%" % text
            label.config(text=text)

    def custom_level(self):
        self.custom = Tk()
        self.custom.title("Custom")
        frame = Frame(self.custom, padx=10, pady=10)
        frame.grid()
        Label(frame, text="Height:").grid(row=0, column=0)
        self.custom_height = Spinbox(frame, width=3, from_=9, to=24)
        self.custom_height.grid(row=0, column=1)
        Label(frame, text="Width:").grid(row=1, column=0)
        self.custom_width = Spinbox(frame, width=3, from_=9, to=30)
        self.custom_width.grid(row=1, column=1)
        Label(frame, text="Mines:").grid(row=2, column=0)
        self.custom_mines = Spinbox(frame, width=3, from_=10, to=668)
        self.custom_mines.grid(row=2, column=1)
        Button(frame, text="OK", command=lambda x= "Custom":self.new_game(level=x)).grid()

    def get_size(self):
        sizes = {"Beginner": (9, 9), "Intermediate": (16, 16), "Advanced": (16, 30)}
        if self.level == "Custom":
            return (int(self.custom_height.get()), int(self.custom_width.get()))
        return sizes[self.level]

    def get_num_mines(self):
        mines = {"Beginner": 10, "Intermediate": 40, "Advanced": 99}
        if self.level == "Custom":
            return int(self.custom_mines.get())
        return mines[self.level]

    def add_board(self):
        self.board = {}
        for key in self.buttons:
            self.buttons[key].destroy()
        self.buttons = {}
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                key = (i, j)
                if key in self.mines:
                    self.board[key] = 'm'
                else:
                    self.board[key] = str(self.get_mine_count(key))
                self.add_button(key, width=1, height=1, command=lambda x=key:self.start_game(x))
        print self

    def start_game(self, space):
        self.tick()
        for key, value in self.board.items():
            self.configure_command(key)
        self.stats[self.level]["games_played"] += 1
        self.save_stats()
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
            mine = (random.randint(0, self.size[0] - 1), random.randint(0, self.size[1] - 1))
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
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                key = (i, j)
                if self.board[key] == 'm':
                    self.buttons[key].destroy()
                    photo = self.get_photo_image('mine.gif')
                    self.buttons[key] = Label(self.frame, image=photo)
                    self.buttons[key].image = photo
                    self.buttons[key].grid(row=i, column=j)
                if isinstance(self.buttons[key], Button):
                    self.buttons[key].config(command=lambda:None)
                    self.buttons[key].unbind("<Button-3>")
        if hasattr(self, "timer"):
            self.time.after_cancel(self.timer)
        self.winning_streak = 0
        self.losing_streak += 1
        if self.level != "Custom":
            self.stats[self.level]["current_streak"] = "%d losses" % self.losing_streak

    def found_border(self, key):
        self.buttons[key].destroy()
        self.buttons[key] = Label(self.frame, width=1, height=1, text=self.board[key])
        self.buttons[key].grid(row=key[0], column=key[1])
        self.try_game_over()

    def try_game_over(self):
        num_btn = 0
        mines_found = 0
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if isinstance(self.buttons[(i, j)], Button):
                    num_btn += 1
                    if self.board[(i, j)] == 'm' and (i, j) in self.flags:
                        mines_found += 1
        if num_btn ==  mines_found == self.num_mines: # print game over
            self.time.after_cancel(self.timer)
            for key, value in self.buttons.items():
                value.unbind("<Button-3>")
            self.stats[self.level]["games_won"] += 1
            self.winning_streak += 1
            self.losing_streak = 0
            if self.level != "Custom":
                self.stats[self.level]["current_streak"] = "%d wins" % self.winning_streak
            self.save_stats()

    def get_photo_image(self, image):
        return ImageTk.PhotoImage(Image.open(image))

    def __str__(self):
        s = ""
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                s += self.board[(i, j)] + "\t"
            s += "\n"
        return s

if __name__ == "__main__":
    root = Tk()
    minesweeper = Minesweeper(root)
    root.mainloop()
