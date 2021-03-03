from sliding_puzzle import Game
import random
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import Adam
from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory
import time
import gym
from gym.utils import seeding
from gym import spaces
import tkinter as tk


class AI(Game, gym.Env):
    def __init__(self, size=4):
        super().__init__(size)
        self.score = 0
        self.update_score()  # for ai
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Space(np.array(self.grid))
        self.moves_made = 0
        self.reward_range = (0, 100000)
        self.window = tk.Tk()
        self.labels = []
        for row in self.grid:
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

    def step(self, action):
        move = self.on_keypress(['w', 'a', 's', 'd'][action])
        self.moves_made += 1
        if move:
            reward = self.get_reward()
        else:
            reward = -10
        if self.moves_made < 999:
            return self.grid, reward, self.is_complete(), {}
        else:
            return self.grid, -10000, True, {}

    def run(self): # for testing
        done = False
        while not done:
            time.sleep(0.05)
            state, reward, done, info = self.step(self.action_space.sample())

    def reset(self):
        self.window.destroy()
        self.__init__(self.size)
        return np.array(self.grid)

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def render(self, mode='human'):
        for i, row in enumerate(self.grid):
            for j, element in enumerate(row):
                if element != -1:
                    self.labels[i][j]["text"] = element
                else:
                    self.labels[i][j]["text"] = ""
        self.window.update()
        time.sleep(1)


def build_model(state, actions):
    model = Sequential()
    model.add(Flatten(input_shape=(1, state[0], state[1])))
    model.add(Dense(8*ai.size, activation='relu'))
    model.add(Dense(8*ai.size, activation='relu'))
    model.add(Dense(actions, activation="linear"))
    return model


def build_agent(model, actions):
    policy = BoltzmannQPolicy()
    memory = SequentialMemory(limit=1000, window_length=1)
    dqn = DQNAgent(model=model, memory=memory, policy=policy,
                   nb_actions=actions, nb_steps_warmup=10, target_model_update=1e-2)
    return dqn


def train(dqn):
    for i in range(0,100):
        dqn.fit(ai, nb_steps=5000, visualize=False, verbose=1)
        dqn.save_weights('2x2/dqn_weights.h5f', overwrite=True)
        dqn.test(ai, nb_episodes=10, visualize=False)

def test(dqn):
    dqn.test(ai, nb_episodes=10, visualize=True)


if __name__ == "__main__":
    ai = AI(2)

    model = build_model(np.array(ai.grid).shape, 4)
    dqn = build_agent(model, 4)

    dqn.compile(Adam(lr=1e-3), metrics=['mae'])
    dqn.load_weights('2x2/dqn_weights.h5f')
    test(dqn)