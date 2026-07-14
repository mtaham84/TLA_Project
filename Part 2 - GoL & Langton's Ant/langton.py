# -*- coding: utf-8 -*-
"""
Langton's Ant Student Template Module.
"""
import numpy as np


class LangtonsAnt:
    
    def __init__(self, N, ant_position, rules):
        """
        Initialize the Langton's Ant simulation.
        
        Args:
            N (int): The grid size (NxN).
            ant_position (tuple): Starting coordinate of the ant as (r, c).
            rules (dict): Dictionary defining transition rules.
                          Format: {current_color: (next_color, turn_direction)}
        """
        self.N = N
        self.grid = np.zeros((N, N), dtype=np.uint8)

        self.ant_row, self.ant_col = ant_position
        UP=0
        self.direction = UP

        self.rules = rules

    def get_states(self):
        """
        Returns the current state grid of the cells.
        
        Returns:
            np.ndarray: The NxN cellular grid.
        """
        return self.grid

    def get_current_position(self):
        """
        Returns the ant's current position as a tuple (r, c).
        
        Returns:
            tuple: Current coordinates of the ant.
        """
        return (self.ant_row, self.ant_col)
    

    def step(self):
        """
        Perform a single simulation step following the ruleset.
        """
        current_color = self.grid[self.ant_row, self.ant_col]

        next_color, turn = self.rules[current_color]

    
        self.grid[self.ant_row, self.ant_col] = next_color
        UP = 0
        RIGHT = 1
        DOWN = 2
        LEFT = 3

        if turn == 'R':
            self.direction = (self.direction + 1) % 4
        elif turn == 'L':
            self.direction = (self.direction - 1) % 4
        if self.direction == UP:
            self.ant_row = (self.ant_row - 1) % self.N

        elif self.direction == RIGHT:
            self.ant_col = (self.ant_col + 1) % self.N

        elif self.direction == DOWN:
            self.ant_row = (self.ant_row + 1) % self.N

        elif self.direction == LEFT:
            self.ant_col = (self.ant_col - 1) % self.N


    def update(self):
        """
        Alias for step() to support standard animation.
        """
        self.step()