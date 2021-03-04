import keyboard
import random


class Game:
    def __init__(self, size=4):
        self.size = size
        number = list(range(1, size ** 2))
        number.append(-1)
        self.grid = [number[size * i: size * i + size] for i in range(0, size)]
        while self.is_complete():
            self.shuffle()
        self.score = 0
        self.update_score()
        self.max_score = 0



    def get_reward(self):
        old_score = self.score
        self.update_score()
        if self.score > self.max_score:

            self.max_score = self.score
            return self.max_score - old_score
        return -1

    def update_score(self):
        if self.is_complete():
            self.score = self.size ** 4
            return
        arr = []
        for row in self.grid:
            arr.extend(row)
        count = 0
        for i, element in enumerate(arr):
            if i + 1 == element:
                count += 1
        self.score = count ** 2

    def shuffle(self):
        for i in range(self.size ** self.size * self.size):
            r = random.randint(0, 3)
            if r == 0:
                self.up()
            if r == 1:
                self.left()
            if r == 2:
                self.right()
            if r == 3:
                self.down()

    def find_space(self):
        for i, row in enumerate(self.grid):
            for j, element in enumerate(row):
                if element == -1:
                    return i, j

    def on_keypress(self, key, p=False, gui=False):
        move = False
        if key == 'w':
            move = self.up()
        if key == 'a':
            move = self.left()
        if key == 's':
            move = self.down()
        if key == 'd':
            move = self.right()
        if p:
            print(self.toString())
        if gui:
            return self.is_complete()
        return move

    def up(self):
        i, j = self.find_space()
        if i != self.size - 1:
            self.grid[i][j] = self.grid[i + 1][j]
            self.grid[i + 1][j] = -1
            return True
        return False

    def down(self):
        i, j = self.find_space()
        if i != 0:
            self.grid[i][j] = self.grid[i - 1][j]
            self.grid[i - 1][j] = -1
            return True
        return False

    def right(self):
        i, j = self.find_space()
        if j != 0:
            self.grid[i][j] = self.grid[i][j - 1]
            self.grid[i][j - 1] = -1
            return True
        return False

    def left(self):
        i, j = self.find_space()
        if j != self.size - 1:
            self.grid[i][j] = self.grid[i][j + 1]
            self.grid[i][j + 1] = -1
            return True
        return False
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
        keyboard.wait()
