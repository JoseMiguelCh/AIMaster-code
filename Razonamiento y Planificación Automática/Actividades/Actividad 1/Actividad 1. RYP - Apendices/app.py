#!/usr/bin/env python
# coding: utf-8

# 2021 Modified by: Alejandro Cervantes
# 2022 Modified by: Jose Miguel Chacon

from __future__ import print_function

import math
from simpleai.search import SearchProblem, astar, breadth_first, depth_first
from simpleai.search.viewers import BaseViewer, ConsoleViewer, BaseViewer

MAP = """
########
#    T #
# #### #
#   P# #
# ##   #
#      #
########
"""
MAP = [list(x) for x in MAP.split("\n") if x]

COSTS = {
    "up": 1.0,
    "down": 1.0,
    "left": 1.0,
    "right": 1.0,
}

NU_COSTS = {
    "up": 5.0,
    "down": 1.0,
    "left": 1.0,
    "right": 1.0,
}


class GameWalkPuzzle(SearchProblem):

    def __init__(self, board, costs, heuristic=None):
        self.board = board
        self.costs = costs
        self.h = heuristic
        self.goal = (0, 0)
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x].lower() == "t":
                    self.initial = (x, y)
                elif self.board[y][x].lower() == "p":
                    self.goal = (x, y)
        super(GameWalkPuzzle, self).__init__(initial_state=self.initial)

    def actions(self, state):
        actions = []
        for action in list(self.costs.keys()):
            newx, newy = self.result(state, action)
            if self.board[newy][newx] != "#":
                actions.append(action)
        return actions

    def result(self, state, action):
        x, y = state
        if action.count("up"):
            y -= 1
        if action.count("down"):
            y += 1
        if action.count("left"):
            x -= 1
        if action.count("right"):
            x += 1
        new_state = (x, y)
        return new_state

    def is_goal(self, state):
        return state == self.goal

    def cost(self, state, action, state2):
        return self.costs[action]

    def heuristic(self, state):
        x, y = state
        gx, gy = self.goal
        h = None
        if self.h == 'manhattan':
            h = abs(x - gx) + abs(y - gy)  # Manhattan distance
        elif self.h == 'euclidean':
            h = math.sqrt((x - gx)**2 + (y - gy)**2)  # Euclidean distance
        return h


def searchInfo(problem, result, use_viewer):
    def getTotalCost(problem, result):
        originState = problem.initial_state
        totalCost = 0
        for action, endingState in result.path():
            if action is not None:
                totalCost += problem.cost(originState, action, endingState)
                originState = endingState
        return totalCost

    res = "Total length of solution: {0}\n".format(len(result.path()))
    res += "Total cost of solution: {0}\n".format(
        getTotalCost(problem, result))

    if use_viewer:
        stats = [{'name': stat.replace('_', ' '), 'value': value}
                 for stat, value in list(use_viewer.stats.items())]

        for s in stats:
            res += '{0}: {1}\n'.format(s['name'], s['value'])
    return res


def resultado_experimento(problem, MAP, result, used_viewer):
    path = [x[1] for x in result.path()]
    for y in range(len(MAP)):
        for x in range(len(MAP[y])):
            if (x, y) == problem.initial:
                print("T", end='')
            elif (x, y) == problem.goal:
                print("P", end='')
            elif (x, y) in path:
                print("·", end='')
            else:
                print(MAP[y][x], end='')
        print()
    info = searchInfo(problem, result, used_viewer)
    print(info)


def main():
    print("Amplitud - Costo uniforme")
    problem = GameWalkPuzzle(MAP, COSTS)
    used_viewer = BaseViewer()
    result = breadth_first(problem, graph_search=True, viewer=used_viewer)
    resultado_experimento(problem, MAP, result, used_viewer)

    print("Amplitud - Costo no uniforme")
    problem = GameWalkPuzzle(MAP, NU_COSTS)
    used_viewer = BaseViewer()
    result = breadth_first(problem, graph_search=True, viewer=used_viewer)
    resultado_experimento(problem, MAP, result, used_viewer)

    print("Profundidad - Costo uniforme")
    problem = GameWalkPuzzle(MAP, COSTS)
    used_viewer = BaseViewer()
    result = depth_first(problem, graph_search=True, viewer=used_viewer)
    resultado_experimento(problem, MAP, result, used_viewer)

    print("Profundidad - Costo no uniforme")
    problem = GameWalkPuzzle(MAP, NU_COSTS)
    used_viewer = BaseViewer()
    result = depth_first(problem, graph_search=True, viewer=used_viewer)
    resultado_experimento(problem, MAP, result, used_viewer)

    print("----------------------------------------------")
    print("A* - h = manhattan")
    print("A* - Costo uniforme")
    problem = GameWalkPuzzle(MAP, COSTS, 'manhattan')
    used_viewer = BaseViewer()
    result = astar(problem, graph_search=True, viewer=used_viewer)
    resultado_experimento(problem, MAP, result, used_viewer)

    print("A* - Costo no uniforme")
    problem = GameWalkPuzzle(MAP, NU_COSTS, 'manhattan')
    used_viewer = BaseViewer()
    result = astar(problem, graph_search=True, viewer=used_viewer)
    resultado_experimento(problem, MAP, result, used_viewer)

    print("----------------------------------------------")
    print("A* - h = euclidean")
    print("A* - Costo uniforme")
    problem = GameWalkPuzzle(MAP, COSTS, 'euclidean')
    used_viewer = BaseViewer()
    result = astar(problem, graph_search=True, viewer=used_viewer)
    resultado_experimento(problem, MAP, result, used_viewer)

    print("A* - Costo no uniforme")
    problem = GameWalkPuzzle(MAP, NU_COSTS, 'euclidean')
    used_viewer = BaseViewer()
    result = astar(problem, graph_search=True, viewer=used_viewer)
    resultado_experimento(problem, MAP, result, used_viewer)


if __name__ == "__main__":
    main()
