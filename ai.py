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


class AI(Game, gym.Env):
    def __init__(self, size=4):
        super().__init__(size)
        self.score = 0
        self.update_score()  # for ai
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Space(np.array(self.grid))
        self.moves_made = 0
        self.reward_range = (0, 100000)

    def step(self, action):
        self.on_keypress(['w', 'a', 's', 'd'][action])
        self.moves_made += 1
        if self.moves_made < 1000:
            return self.grid, self.get_reward(), self.is_complete(), {}
        else:
            return self.grid, self.get_reward(), True, {}

    def run(self):
        done = False
        while not done:
            time.sleep(0.05)
            state, reward, done, info = self.step(self.action_space.sample())

    def reset(self):
        self.__init__(2)
        return np.array(self.grid)

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def render(self, mode='human'):
        pass


def build_model(state, actions):
    model = Sequential()
    model.add(Flatten(input_shape=(1, state[0], state[1])))
    model.add(Dense(4, activation='relu'))
    model.add(Dense(4, activation='relu'))
    model.add(Dense(actions, activation="linear"))
    return model


def build_agent(model, actions):
    policy = BoltzmannQPolicy()
    memory = SequentialMemory(limit=1000, window_length=1)
    dqn = DQNAgent(model=model, memory=memory, policy=policy,
                   nb_actions=actions, nb_steps_warmup=10, target_model_update=1e-2)
    return dqn


def train(dqn):
    dqn.fit(ai, nb_steps=50000, visualize=False, verbose=1)
    dqn.save_weights('dqn_weights.h5f', overwrite=True)

def test(dqn):
    dqn.load_weights('dqn_weights.h5f')
    dqn.test(ai, nb_episodes=5, visualize=False)


if __name__ == "__main__":
    ai = AI(2)

    model = build_model(np.array(ai.grid).shape, 4)
    dqn = build_agent(model, 4)
    dqn.compile(Adam(lr=1e-3), metrics=['mae'])

    test(dqn)
