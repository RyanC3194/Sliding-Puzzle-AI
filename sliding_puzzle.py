import random
import keyboard


class Game:
    def __init__(self, size=4):
        self.size = size
        number = list(range(1, size ** 2))
        random.shuffle(number)
        number.append(-1)
        self.grid = [number[size * i: size * i + size] for i in range(0, size)]

    def find_space(self):
        for i, row in enumerate(self.grid):
            for j, element in enumerate(row):
                if element == -1:
                    return i, j

    def on_keypress(self, key, p=False):
        if key == 'w':
            self.up()
        if key == 'a':
            self.left()
        if key == 's':
            self.down()
        if key == 'd':
            self.right()
        if p:
            print(self.toString())
        if self.is_complete():
            keyboard.remove_hotkey('a')
            keyboard.remove_hotkey('w')
            keyboard.remove_hotkey('s')
            keyboard.remove_hotkey('d')
            return True

    def up(self):
        i, j = self.find_space()
        if i != self.size - 1:
            self.grid[i][j] = self.grid[i + 1][j]
            self.grid[i + 1][j] = -1

    def down(self):
        i, j = self.find_space()
        if i != 0:
            self.grid[i][j] = self.grid[i - 1][j]
            self.grid[i - 1][j] = -1

    def right(self):
        i, j = self.find_space()
        if j != 0:
            self.grid[i][j] = self.grid[i][j - 1]
            self.grid[i][j - 1] = -1

    def left(self):
        i, j = self.find_space()
        if j != self.size - 1:
            self.grid[i][j] = self.grid[i][j + 1]
            self.grid[i][j + 1] = -1

    def is_complete(self):
        arr = []
        for row in self.grid:
            arr.extend(row)
        return arr[-1] == -1 and sorted(arr[:-1]) == arr[:-1]

    def __str__(self):
        return self.toString()

    def toString(self):
        out = "-" * (self.size * 3 + 1) + "\n"
        for row in self.grid:
            out += "|"
            for element in row:
                if element == -1:
                    out += "  |"
                else:
                    if element / 10 >= 1:
                        out += str(element) + "|"
                    else:
                        out += " " + str(element) + "|"
            out += "\n"
        out += "-" * (self.size * 3 + 1) + "\n"
        return out

    def start(self):
        print(self.toString())
        keyboard.add_hotkey('d', self.on_keypress, args='d')
        keyboard.add_hotkey('a', self.on_keypress, args='a')
        keyboard.add_hotkey('w', self.on_keypress, args='w')
        keyboard.add_hotkey('s', self.on_keypress, args='s')
