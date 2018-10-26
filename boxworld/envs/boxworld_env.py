import gym
import sys
import os
import copy
from gym import spaces
from gym.utils import seeding
import random
import itertools
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import numpy as np

from common.graph import *


import time

NOOP = 0
DOWN = 1
UP = 2
LEFT = 3
RIGHT = 4

class BoxWorldEnv(gym.Env):


    def __init__(self,dims=(12,12),max_depth=5,max_branches=2,max_branch_depth=1,max_nodes=10):
        self.colors = [(153, 51, 255),
              (51, 51, 255),
              (51, 153, 255),
              (51, 255, 255),
              (51, 255, 153),
              (51, 255, 51),
              (0, 153, 0),
              (255, 255, 0),
              (255, 153, 51),
              (255, 51, 51),
              (255, 51, 255)]
        #self.graph = graph
        self.max_depth=max_depth
        self.max_branches=max_branches
        self.max_branch_depth=max_branch_depth
        self.max_nodes=max_nodes
        self.dims = dims
        self.position_node_map = {}
        self.position_key_color_map = {}
        self.current_grid_map = np.zeros(dims)
        #make the walls (walls = 1)
        self.current_grid_map[0,:] = [1] * dims[0]
        self.current_grid_map[:,0] = [1] * dims[1]
        self.current_grid_map[:,-1] = [1] * dims[1]
        self.current_grid_map[-1,:] = [1] * dims[0]

        self.current_key_color = [0,0,0]

        self.base_grid_map = np.copy(self.current_grid_map)

        self.action_map = {1:lambda x: (x[0]+1,x[1]),
                           2:lambda x: (x[0]-1,x[1]),
                           3:lambda x: (x[0],x[1]-1),
                           4:lambda x: (x[0],x[1]+1)}



        #all door = 3
        #all keys = 4
        #no-go space = > 0 - (2,3)
        #will make map {tuple(map(int,val)):color} where each tuple is a coordinate in the













    def color_graph(self,graph):
        random.shuffle(self.colors)
        for node in graph.all_nodes:
            if not type(node) == Goal:
                node.color = self.colors.pop(0)


    def fill_neighbours(self,position,grid):
        if grid[position[0],position[1]-2] == 0.0:
            grid[position[0],position[1]-2] = 2
        if grid[position[0]-1,position[1]-2] == 0.0:
            grid[position[0]-1,position[1]-2] = 2
        if grid[position[0]+1,position[1]-2] == 0.0:
            grid[position[0]+1,position[1]-2] = 2
        if grid[position[0]-1,position[1]-1] == 0.0:
            grid[position[0]-1,position[1]-1] = 2
        if grid[position[0]+1,position[1]-1] == 0.0:
            grid[position[0]+1,position[1]-1] = 2
        if grid[position[0]-1,position[1]] == 0.0:
            grid[position[0]-1,position[1]] = 2
        if grid[position[0]+1,position[1]] == 0.0:
            grid[position[0]+1,position[1]] = 2
        if grid[position[0]-1,position[1]+1] == 0.0:
            grid[position[0]-1,position[1]+1] = 2
        if grid[position[0],position[1]+1] == 0.0:
            grid[position[0],position[1]+1] = 2
        if grid[position[0]+1,position[1]+1] == 0.0:
            grid[position[0]+1,position[1]+1] = 2
        if position[1] + 2 <= self.dims[1] - 1:
            if grid[position[0],position[1]+2] == 0.0:
                grid[position[0],position[1]+2] = 2
            if grid[position[0]+1,position[1]+2] == 0.0:
                grid[position[0] + 1, position[1] + 2] = 2
            if grid[position[0]-1,position[1]+2] == 0.0:
                grid[position[0] - 1, position[1] + 2] = 2




    def reset(self):
        self.graph = Graph(depth=5)
        self.color_graph(self.graph)
        current_node = self.graph.trunk_nodes[0]  # goal node
        finished_nodes = []  # ordered by placement & distance from goal
        keep_going = True

        while keep_going:

            links = [node for node in current_node.links if node not in finished_nodes]
            if not links:
                free_spaces = np.where(self.current_grid_map == 0)
                free_spaces = list(zip(free_spaces[0], free_spaces[1]))
                free_spaces = [i for i in free_spaces if i[1] > 1]  # and i[1] > 1]
                free_spaces = [i for i in free_spaces if i[0] < self.dims[0] - 1 and i[1] < self.dims[1] - 1]
                free_space = random.choice(free_spaces)
                self.current_grid_map[free_space[0], free_space[1]] = 4
                self.position_node_map[(free_space[0], free_space[1])] = node
                self.open_key = [free_space[0], free_space[1]]

                break
            for node in links:
                free_spaces = np.where(self.current_grid_map == 0)
                free_spaces = list(zip(free_spaces[0], free_spaces[1]))
                free_spaces = [i for i in free_spaces if i[1] > 1]  # and i[1] > 1]
                free_spaces = [i for i in free_spaces if i[0] < self.dims[0] - 1 and i[1] < self.dims[1] - 1]
                # pick a random free space
                free_space = random.choice(free_spaces)
                # populate the current_grid_map & store it
                self.current_grid_map[free_space[0], free_space[1]] = 3
                self.current_grid_map[free_space[0], free_space[1] - 1] = 4
                self.fill_neighbours(free_space, self.current_grid_map)
                # node.location = free_space
                # store the coordanate-node relationship
                self.position_node_map[(free_space[0], free_space[1] - 1)] = current_node
                self.position_key_color_map[(free_space[0], free_space[1])] = node.color
                # self.position_node_map[(free_space[0], free_space[1])] = node
                # self.position_key_color_map[(free_space[0], free_space[1] - 1)] = current_node.color
                finished_nodes.append(current_node)
                current_node = node

        # insert the agent
        free_spaces = np.where(self.current_grid_map == 0)
        free_spaces = list(zip(free_spaces[0], free_spaces[1]))
        free_space = random.choice(free_spaces)
        # self.agent_position = free_space
        self.current_grid_map[free_space[0], free_space[1]] = 5
        return self._gridmap_to_image()

    def _gridmap_to_image(self):
        image = np.zeros((self.dims[0],self.dims[1],3), dtype=np.uint8)
        image[:] = [96,96,96]
        #put walls in
        walls = np.where(self.current_grid_map == 1.0)
        for x,y in list(zip(walls[0],walls[1])):
            #print((x,y))
            image[x,y,:] = [0,0,0]
        boxes = np.where(self.current_grid_map == 4)
        #print("boxes",boxes)
        #print(self.position_node_map)
        #print(self.current_grid_map)
        for x,y in list(zip(boxes[0],boxes[1])):
            #print((x,y))
            color_of_box = self.position_node_map[(x,y)].color
            image[x,y,:] = color_of_box

        doors = np.where(self.current_grid_map == 3)
        zipped_doors = list(zip(doors[0],doors[1]))
        for x,y in zipped_doors:
            color_of_door = self.position_key_color_map[(x,y)]
            image[x,y,:] = color_of_door

        agent = np.where(self.current_grid_map == 5)
        image[agent[0],agent[1],:] = [192,192,192]



        return image#imresize(image, 10 * 100, interp='nearest')




    def step(self, action):
        action = int(action)
        reward, done, info = 0,0,0
        print("action", action)
        current_position = np.where(self.current_grid_map == 5)
        position_function = self.action_map[action]
        intended_position = position_function(current_position)
        intended_position_value = self.current_grid_map[intended_position[0],intended_position[1]]
        print("cur",current_position)
        print("intended",intended_position)
        print("open", self.open_key)


        #movement to empty space
        if intended_position_value == 0.0 or intended_position_value == 2.0:
            self.current_grid_map[current_position[0],current_position[1]] = 2.0
            self.current_grid_map[intended_position[0],intended_position[1]] = 5.0
        #movement to the open key
        elif intended_position[0] == self.open_key[0] and intended_position[1] == self.open_key[1]:
            self.current_key_color = self.position_node_map[(int(intended_position[0]),int(intended_position[1]))].color
            self.current_grid_map[current_position[0], current_position[1]] = 2.0
            self.current_grid_map[intended_position[0], intended_position[1]] = 5.0
        #movement to a door (need a key to open)
        elif intended_position_value == 3.0:
            print("pkcmap",self.position_key_color_map)
            print("cu col", self.current_key_color)
            if self.position_key_color_map[(int(intended_position[0]),int(intended_position[1]))] == self.current_key_color:
                self.current_grid_map[current_position[0], current_position[1]] = 2.0
                self.current_grid_map[intended_position[0], intended_position[1]] = 5.0
        #movement (left) to key.  should it become an open key instead?
        elif intended_position_value == 4.0 and action == 3:
            self.current_key_color = self.position_node_map[
                (int(intended_position[0]), int(intended_position[1]))].color
            self.current_grid_map[current_position[0], current_position[1]] = 2.0
            self.current_grid_map[intended_position[0], intended_position[1]] = 5.0
            print(type(self.position_node_map[int(intended_position[0]),int(intended_position[1])]))



        return self._gridmap_to_image(), reward, done, info

#I don't think you can reliably have more than 8 nodes
# for i in range(10000):
#     print('attempt',i)
#     a = Graph(depth=10)
#     b = BoxWorldEnv(a)
#     plt.imshow(b._gridmap_to_image())
#     plt.show()
#
#     print("asdf")
#
# print("done")

# a = Graph(depth=5)
# b = BoxWorldEnv(a)
# for i in range(10000):
#     which = random.choice([UP, DOWN, LEFT, RIGHT])
#     print("action", which)
#     img = b.step(which)[0]
#     print(b.current_grid_map)
#     # plt.imshow(img)
#     # plt.show()
#     time.sleep(5)

print("ok")


