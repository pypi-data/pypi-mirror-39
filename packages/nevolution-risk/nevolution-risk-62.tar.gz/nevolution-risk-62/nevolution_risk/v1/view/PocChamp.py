# Proof of concept goes here
import os
from time import sleep

import numpy as np
import pygame
from pygame.cursors import load_xbm

from nevolution_risk.constants.colors import blue, black, deep_pink
from nevolution_risk.constants.view_settings import coordinates, radius, width, height
from nevolution_risk.v1.logic import Graph

graph = [[], [2, 3, 5], [1, 3, 4], [1, 2, 7], [2, 5, 6], [1, 4, 6], [4, 5, 7], [3, 6, 9], [9, 10], [7, 8, 10], [8, 9]]
graph1 = Graph()


def poc_render(surface, grid):
    surface.fill(deep_pink)

    for edge in grid:
        pygame.draw.line(surface, blue, edge[0], edge[1], 10)

    n = 0
    for position in coordinates:
        pygame.draw.circle(surface, graph1.nodes[n].player.color, position, radius)
        n = n + 1


def is_inside(pos1, pos2):
    square = (pos1[0] - pos2[0]) * (pos1[0] - pos2[0]) + (pos1[1] - pos2[1]) * (pos1[1] - pos2[1])
    if square < radius * radius:
        return True
    else:
        return False


def to_one_hot(n, limit):
    array = np.zeros(limit, np.int32)
    array[n - 1] = 1
    return array


def find_node(position):
    for n in range(1, 11):
        if is_inside(coordinates[n], position):
            return n

    return 0


def render_tests():
    pygame.init()
    display = pygame.display.set_mode((width, height))
    running = True
    loop = True
    current_player = 1

    grid = []
    for n in range(1, 10):
        for adjacent in graph1.nodes[n].adj_list:
            grid.append((coordinates[n], coordinates[adjacent.id]))

    node1 = 0
    pos1 = (0, 0)
    pos2 = (0, 0)
    mouse_pressed = False

    dir_name = os.path.dirname(os.path.realpath(__file__))
    void_path = os.path.join(dir_name, '../res', 'void.xbm')
    void_mask_path = os.path.join(dir_name, '../res', 'void-mask.xbm')

    void_cursor = load_xbm(void_path, void_mask_path)
    sword = pygame.image.load(os.path.join(dir_name, '../res', 'sword.png'))

    while running:
        if graph1.is_conquered():
            print("done")
            running = False

        pos2 = pygame.mouse.get_pos()
        poc_render(surface=display, grid=grid)

        if mouse_pressed:
            pygame.draw.line(display, black, pos1, pos2, 10)
            display.blit(sword, pos2)

        sleep(1 / 100)
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
                        pygame.mouse.set_cursor(*void_cursor)

            if mouse_pressed:
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        node2 = find_node(pos2)
                        if current_player == 1:
                            if (node1 != 0) and (node2 != 0):
                                graph1.attack(node1, node2, graph1.player1)
                                current_player = 2
                        else:
                            if (node1 != 0) and (node2 != 0):
                                graph1.attack(node1, node2, graph1.player2)
                                current_player = 1

                    mouse_pressed = False
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)


if __name__ == '__main__':
    render_tests()
