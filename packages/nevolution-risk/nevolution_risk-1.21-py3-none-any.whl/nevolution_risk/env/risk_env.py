import gym


class RiskEnv(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 10
    }

    def __init__(self):
        self.placeholder = "holup"

    def step(self, action):
        pass

    def reset(self):
        pass

    def render(self, mode='human'):
        pass
