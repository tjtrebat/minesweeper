__author__ = 'Tom'

import cPickle as pickle
from Tkinter import *

class Statistics:
    def __init__(self):
        self.stats = self.get_stats()
        self.winning_streak = 0
        self.losing_streak = 0

    def show_gui(self, event=None):
        self.root = Tk()
        self.frame = Frame(self.root, padx=10, pady=10)
        self.frame.grid()
        self.add_levels()
        self.add_best_times()
        self.add_results()
        self.root.mainloop()

    def get_stats(self):
        try:
            return pickle.load(open('stats.p'))
        except IOError:
            pass
        d = {"games_played": 0, "games_won": 0, "win_percentage": 0,
                                   "longest_winning_streak": 0, "longest_losing_streak": 0,
                                   "current_streak": "0 losses", "best_times": [('', ''),] * 5}
        return {"Beginner": d, "Intermediate": d.copy(), "Advanced": d.copy()}

    def save_stats(self, level):
        if self.stats[level]["longest_winning_streak"] < self.winning_streak:
            self.stats[level]["longest_winning_streak"] = self.winning_streak
        if self.stats[level]["longest_losing_streak"] < self.losing_streak:
            self.stats[level]["longest_losing_streak"] = self.losing_streak
        pickle.dump(self.stats, open('stats.p', 'w+'))

    def add_levels(self):
        l = Listbox(self.frame)
        l.insert(END, "Beginner")
        l.insert(END, "Intermediate")
        l.insert(END, "Advanced")
        l.selection_set(0)
        l.bind("<ButtonRelease-1>", self.set_stat_labels)
        l.grid()

    def add_best_times(self):
        best_times = LabelFrame(self.frame, text="Best Times")
        self.times = self.get_times(best_times)
        for i, time in enumerate(self.times):
            time.grid(sticky="w")
        best_times.grid(padx=20, row=0, column=1, sticky="N")

    def add_results(self):
        results = Frame(self.frame)
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

    def get_stat_labels(self, frame):
        labels = {}
        for key in self.stats["Beginner"].keys():
            if key != "best_times":
                labels[key] = Label(frame, text=self.stats["Beginner"][key])
        return labels

    def set_stat_labels(self, event):
        level = event.widget.get(event.widget.curselection()[0])
        for key, label in self.stat_labels.items():
            label.config(text=self.stats[level][key])
        self.set_times(event.widget)

    def get_times(self, frame):
        labels = []
        for time in self.stats["Beginner"]["best_times"]:
            labels.append(Label(frame, text="%s\t%s" % time))
        return labels

    def set_times(self, widget):
        for i, time in enumerate(self.times):
            best_times = self.stats[widget.get(widget.curselection()[0])]["best_times"]
            if i <= len(best_times):
                time.config(text="%s\t%s" % best_times[i])
            else:
                time.config(text="")

    def set_win_percentage(self, level):
        win_percentage = 100 * (float(self.stats[level]["games_won"]) / self.stats[level]["games_played"])
        self.stats[level]["win_percentage"] = "%d%%" % win_percentage

if __name__ == "__main__":
    statistics = Statistics()
    statistics.show_gui()