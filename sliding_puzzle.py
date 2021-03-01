import random


class Game:
    def __init__(self, size=4):
        self.size = size
        number = list(range(1, size ** 2))
        random.shuffle(number)
        number.append("")
        self.grid = [number[size * i: size * i + size] for i in range(0, size)]

    def findSpace(self):
        for i, row in enumerate(self.grid):
            for j, element in enumerate(row):
                if element == "":
                    return i, j

    def toString(self):
        print("-" * (self.size * 3 + 1))
        for row in self.grid:
            print("|", end="")
            for element in row:
                if element == "":
                    print("  ", end="|")
                else:
                    if element / 10 >= 1:
                        print(element, end="|")
                    else:
                        print(" " + str(element), end="|")
            print("")
        print("-" * (self.size * 3 + 1))



print(Game().findSpace())
