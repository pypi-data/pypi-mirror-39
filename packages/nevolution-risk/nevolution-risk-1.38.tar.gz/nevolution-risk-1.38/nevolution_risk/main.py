import os
from time import sleep

import gym
from nevolution_risk.env import RiskEnv

if __name__ == '__main__':
    """
    gym.make doesnt work for our environment without the import of the env
    possibly a bug
    """
    env = gym.make("nevolution-risk-v0")
    env.reset()

    for i in range(200):
        print('********** Step', i + 1, '**********')
        if os.getenv('RENDER') == 'TRUE':
            env.render()
        action = env.action_space.sample()
        for n in range(0, 60):
            env.render()
            sleep(1 / 100)

        print('Action:', action)
        observation, reward, done, info = env.step(action)
        print('Reward:', reward)
        if done:
            break
