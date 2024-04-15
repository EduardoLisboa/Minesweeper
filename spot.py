import pygame
from Assets.images import Images
from Constants.constants import Constants

class Spot:

    def __init__(self, row, col) -> None:
        self.row = row
        self.col = col
        self.x = row * Constants.SQUARE_SIZE
        self.y = col * Constants.SQUARE_SIZE
        self.image = Images.IMAGES_DICT['empty']
        self.is_bomb = False
        self.is_number = False
        self.is_empty = False
        self.is_flagged = False
        self.clicked = False
        self.neighbors = []

    def get_pos(self):
        return self.row, self.col

    def draw(self, win):
        win.blit(
            self.image,
            (
                self.x + 3,
                self.y + 3
            )
        )

    def update_neighbors(self, grid):
        self.neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if 0 <= self.row + i < len(grid) and 0 <= self.col + j < len(grid[0]):
                    self.neighbors.append(grid[self.row + i][self.col + j])