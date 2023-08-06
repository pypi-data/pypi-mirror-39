import pygame

import gym
import numpy as np
from gym import spaces
from numpy import int32

from nevolution_risk.v1.logic import Graph
from nevolution_risk.v1.view import Gui


class RiskEnv(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 10
    }

    node_count = 10
    player_count = 2
    troop_count = 0

    action_space = spaces.Box(low=0, high=10, shape=[2, ], dtype=int32)
    observation_space = spaces.Box(low=0, high=1, shape=[140, ], dtype=int32)

    def __init__(self):
        self.graph = Graph()
        self.static_agent = self.random_step
        self.gui = Gui(self.graph)
        self.reward = 0
        self.current_player = 1
        self.done = False
        self.rendering = True
        self.first_render = True

    def set_static_agent(self, step_function):
        self.static_agent = step_function

    def step(self, action):
        if self.done:
            self.reset()

        if self.graph.attack(action[0], action[1], self.graph.player1):
            self.reward = self.reward + 1
        """
        ----------------------------------------------------------------------------------
        code for opponent AI goes here
        """
        observation = self._graph_to_one_hot()

        player2_action = self.static_agent(observation)

        self.graph.attack(player2_action[0], player2_action[1], self.graph.player2)
        """
        ----------------------------------------------------------------------------------
        """

        observation = self._graph_to_one_hot()
        self.done = self.graph.is_conquered()

        return observation, self.reward, self.done, ()

    def random_step(self, observation):
        return self.action_space.sample()

    def reset(self):
        self.graph = Graph()
        self.gui.graph = self.graph
        self.reward = 0
        self.done = False
        self.rendering = True

    def render(self, mode='human', control="auto"):
        if self.first_render:
            pygame.init()
            self.first_render = False

        if control == "auto":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
        if mode == 'rgb_array':
            return self.gui.render(mode)
        else:
            self.gui.render(mode)

        if control == "auto":
            pygame.display.update()

    def _graph_to_one_hot(self):
        one_hot = np.zeros(0, int32)
        array3 = np.zeros(5, int32)

        np.append(one_hot, array3)

        player1 = self.graph.player1
        player2 = self.graph.player2

        for n in range(1, 11):
            one_hot = np.append(one_hot, to_one_hot(n, self.node_count))
            if self.graph.nodes[n].player == player1:
                one_hot = np.append(one_hot, to_one_hot(1, self.player_count))
            elif self.graph.nodes[n].player == player2:
                one_hot = np.append(one_hot, to_one_hot(2, self.player_count))
            else:
                one_hot = np.append(one_hot, to_one_hot(0, self.player_count))

        return one_hot


def to_one_hot(n, limit):
    array = np.zeros(limit + 1, np.int32)
    array[n] = 1
    return array
