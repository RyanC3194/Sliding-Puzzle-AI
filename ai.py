from sliding_puzzle import Game
import random
import numpy as np
import time


class AI(Game):
    def __init__(self, size=4):
        super().__init__(size)
        self.score = 0
        self.update_score()  # for ai
        self.moves = ['w', 'a', 's', 'd']
        self.moves_made = 0

    def step(self, key):
        self.on_keypress(key)
        self.moves_made += 1
        if self.moves_made < 1000:
            return self.grid, self.get_reward(), self.is_complete()
        else:
            return self.grid, self.get_reward(), True

    def get_reward(self):
        old_score = self.score
        self.update_score()
        return self.score - old_score

    def update_score(self):
        if self.is_complete():
            self.score = 100000
            return
        arr = []
        for row in self.grid:
            arr.extend(row)
        self.score = 0
        for i, element in enumerate(arr):
            if i + 1 == element:
                self.score += i


    def run(self):
        print(self)
        done = False
        while not done:
            time.sleep(0.05)
            state, reward, done = self.step(self.moves[random.randint(0, 3)])
            print(self)
            print(self.moves_made)


if __name__ == "__main__":
    ai = AI()
    ai.run()
