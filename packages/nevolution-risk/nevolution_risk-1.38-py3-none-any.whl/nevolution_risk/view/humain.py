from time import sleep

import pygame

import gym

from nevolution_risk.env import RiskEnv
from nevolution_risk.view.utils import find_node

if __name__ == '__main__':
    env = gym.make("nevolution-risk-v0")
    running = True

    current_player = 1
    node1 = 0
    pos1 = (0, 0)
    pos2 = (0, 0)
    mouse_pressed = False

    env.reset()
    env.render(control="manual")

    while running:
        if env.graph.is_conquered():
            print("done")
            running = False

        pos2 = pygame.mouse.get_pos()
        env.render(control="manual")

        if mouse_pressed:
            env.gui.draw_sword(pos1, pos2)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            if not mouse_pressed:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos1 = pygame.mouse.get_pos()
                        node1 = find_node(pos1)
                        mouse_pressed = True
                        env.gui.set_cursor_sword()

            if mouse_pressed:
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        node2 = find_node(pos2)
                        if (node1 != 0) and (node2 != 0):
                            env.step((node1, node2))

                    mouse_pressed = False
                    env.gui.set_cursor_arrow()

        sleep(1 / 60)
