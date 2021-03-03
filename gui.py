import keyboard

from sliding_puzzle import Game
import tkinter as tk


class GUI:
    def __init__(self, size=4):
        self.game = Game(size)
        self.window = tk.Tk()
        self.labels = []
        for row in self.game.grid:
            cur = []
            for element in row:
                if element != -1:
                    cur.append(tk.Label(text=str(element), width=8, height=5, borderwidth=1,
                                        relief="solid"))
                else:
                    cur.append(
                        tk.Label(text="", width=8, height=5, borderwidth=1, relief="solid"))
            self.labels.append(cur)

        for i, row in enumerate(self.labels):
            for j, label in enumerate(row):
                label.grid(column=j, row=i)

    def on_keypress(self, key):
        if self.game.on_keypress(key):
            for row in self.labels:
                for label in row:
                    label.destroy()

            tk.Label(text="You Won", width=8*self.game.size, height=5*self.game.size).pack()
        else:
            self.update()
        print(self.game.get_reward())

    def update(self):
        for i, row in enumerate(self.game.grid):
            for j, element in enumerate(row):
                if element != -1:
                    self.labels[i][j]["text"] = element
                else:
                    self.labels[i][j]["text"] = ""


    def run(self):
        keyboard.add_hotkey('d', self.on_keypress, args='d')
        keyboard.add_hotkey('a', self.on_keypress, args='a')
        keyboard.add_hotkey('w', self.on_keypress, args='w')
        keyboard.add_hotkey('s', self.on_keypress, args='s')
        self.window.mainloop()

if __name__ == "__main__":
    gui = GUI(2)
    gui.run()
