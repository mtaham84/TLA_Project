"""
The Game of Life (GoL) module named in honour of John Conway

This module defines the classes required for the GoL simulation.

"""
import numpy as np
from scipy import signal, ndimage


def parse_pattern(filepath):
    live_cells = []

    if filepath.endswith(".cells"):
        with open(filepath, "r") as f:
            lines = [line.rstrip() for line in f if not line.startswith("!")]

        height = len(lines)
        width = max(len(line) for line in lines)

        for r, line in enumerate(lines):
            for c, ch in enumerate(line):
                if ch == "O":
                    live_cells.append((r, c))

        return width, height, live_cells

    elif filepath.endswith(".rle"):
        with open(filepath, "r") as f:
            lines = [line.strip() for line in f if not line.startswith("#") and line.strip()]

        header = lines[0]
        body = "".join(lines[1:])

        parts = header.split(",")

        width = int(parts[0].split("=")[1])
        height = int(parts[1].split("=")[1])

        r = 0
        c = 0
        number = ""

        for ch in body:
            if ch.isdigit():
                number += ch

            elif ch == "b":
                count = int(number) if number else 1
                c += count
                number = ""

            elif ch == "o":
                count = int(number) if number else 1
                for _ in range(count):
                    live_cells.append((r, c))
                    c += 1
                number = ""

            elif ch == "$":
                count = int(number) if number else 1
                r += count
                c = 0
                number = ""

            elif ch == "!":
                break

        return width, height, live_cells

    else:
        raise ValueError("Unsupported file format")

class GameOfLife:
    """
    Object for computing Conway's Game of Life (GoL) cellular machine/automata
    """

    def __init__(self, N=256, finite=False, fastMode=True):
        self.grid = np.zeros((N, N), np.uint)
        self.neighborhood = np.ones((3, 3), np.uint)  # 8 connected kernel
        self.neighborhood[1, 1] = 0  # do not count centre pixel
        self.finite = finite
        self.fastMode = fastMode
        self.aliveValue = 1
        self.deadValue = 0
        self.rows = N  # use for slow implementation of evolve
        self.cols = N  # use for slow implementation of evolve

    def getStates(self):
        """
        Returns the current states of the cells
        """
        return self.grid

    def getGrid(self):
        """
        Same as getStates()
        """
        return self.getStates()

    def update_grid_fast(self, grid):
        boundary = "fill" if self.finite else "wrap"

        neighbors = signal.convolve2d(
        grid,
        self.neighborhood,
        mode="same",
        boundary=boundary,
        fillvalue=0
    )

        survive = (grid == 1) & ((neighbors == 2) | (neighbors == 3))
        born = (grid == 0) & (neighbors == 3)

        new_grid = np.zeros_like(grid)

        new_grid[survive | born] = self.aliveValue

        return new_grid


    def evolve(self):
        """
        Given the current states of the cells, apply the GoL rules:
        - Any live cell with fewer than two live neighbors dies, as if by underpopulation.
        - Any live cell with two or three live neighbors lives on to the next generation.
        - Any live cell with more than three live neighbors dies, as if by overpopulation.
        - Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
        """
        if self.fastMode:
            self.grid = self.update_grid_fast(self.grid)
        else:
            new_grid = np.zeros_like(self.grid)

        for i in range(self.rows):
            for j in range(self.cols):

                neighbors = 0

                for di in (-1, 0, 1):
                    for dj in (-1, 0, 1):

                        if di == 0 and dj == 0:
                            continue

                        ni = i + di
                        nj = j + dj

                        if self.finite:

                            if 0 <= ni < self.rows and 0 <= nj < self.cols:
                                neighbors += self.grid[ni, nj]

                        else:
                            neighbors += self.grid[
                                ni % self.rows,
                                nj % self.cols
                            ]

                if self.grid[i, j] == self.aliveValue:

                    if neighbors == 2 or neighbors == 3:
                        new_grid[i, j] = self.aliveValue

                else:

                    if neighbors == 3:
                        new_grid[i, j] = self.aliveValue

        self.grid = new_grid

    def insertBlinker(self, index=(0, 0)):
        '''
        Insert a blinker oscillator construct at the index position
        '''
        self.grid[index[0], index[1] + 1] = self.aliveValue
        self.grid[index[0] + 1, index[1] + 1] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 1] = self.aliveValue

    def insertGlider(self, index=(0, 0)):
        '''
        Insert a glider construct at the index position
        '''
        self.grid[index[0], index[1] + 1] = self.aliveValue
        self.grid[index[0] + 1, index[1] + 2] = self.aliveValue
        self.grid[index[0] + 2, index[1]] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 1] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 2] = self.aliveValue

    def insertGliderGun(self, index=(0, 0)):
        '''
        TODO: [Part 1c - Glider Gun Fix]
        The current glider gun pattern is broken. Leave the broken array in the code 
        and instruct the student to debug and fix the coordinates so it loops infinitely.
        '''
        self.grid[index[0] + 1, index[1] + 26] = self.aliveValue

        self.grid[index[0] + 2, index[1] + 24] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 26] = self.aliveValue

        self.grid[index[0] + 3, index[1] + 14] = self.aliveValue
        self.grid[index[0] + 3, index[1] + 15] = self.aliveValue
        self.grid[index[0] + 3, index[1] + 22] = self.aliveValue
        self.grid[index[0] + 3, index[1] + 23] = self.aliveValue
        self.grid[index[0] + 3, index[1] + 36] = self.aliveValue
        self.grid[index[0] + 3, index[1] + 37] = self.aliveValue

        self.grid[index[0] + 4, index[1] + 13] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 17] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 22] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 23] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 36] = self.aliveValue
        self.grid[index[0] + 4, index[1] + 37] = self.aliveValue

        self.grid[index[0] + 5, index[1] + 1 + 1] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 2 + 1] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 12] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 18] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 22] = self.aliveValue
        self.grid[index[0] + 5, index[1] + 23] = self.aliveValue

        self.grid[index[0] + 6, index[1] + 1 + 1] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 2 + 1] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 12] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 16] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 18] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 19] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 24] = self.aliveValue
        self.grid[index[0] + 6, index[1] + 26] = self.aliveValue

        self.grid[index[0] + 7, index[1] + 12] = self.aliveValue
        self.grid[index[0] + 7, index[1] + 18] = self.aliveValue
        self.grid[index[0] + 7, index[1] + 26] = self.aliveValue

        self.grid[index[0] + 8, index[1] + 13] = self.aliveValue
        self.grid[index[0] + 8, index[1] + 17] = self.aliveValue

        self.grid[index[0] + 9, index[1] + 14] = self.aliveValue
        self.grid[index[0] + 9, index[1] + 15] = self.aliveValue

    def insertFromFile(self, filename, index=((0, 0))):
        '''
        Insert cells from pattern file using parse_pattern
        '''
        width, height, live_cells = parse_pattern(filename)
        for r, c in live_cells:
            target_r = index[0] + r
            target_c = index[1] + c
            if 0 <= target_r < self.rows and 0 <= target_c < self.cols:
                self.grid[target_r, target_c] = self.aliveValue