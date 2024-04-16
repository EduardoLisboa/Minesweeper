import pygame
from Assets.images import Images
from Constants.constants import Constants

class Spot:

    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col
        self.x = row * Constants.SQUARE_SIZE
        self.y = col * Constants.SQUARE_SIZE
        self.image = Images.IMAGES_DICT[0]
        self.is_bomb = False
        self.number = 0
        self.is_flagged = False
        self.clicked = False
        self.neighbors = []

    def get_pos(self) -> tuple[int, int]:
        return self.row, self.col

    def draw(self, win: pygame.Surface) -> None:
        win.blit(
            self.image,
            (
                self.x + 3,
                self.y + 3
            )
        )
    
    def calc_number(self) -> None:
        for neighbor in self.neighbors:
            if neighbor.is_bomb:
                self.number += 1

    def update_neighbors(self, grid: list[list['Spot']]) -> None:
        self.neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if 0 <= self.row + i < len(grid) and 0 <= self.col + j < len(grid[0]):
                    self.neighbors.append(grid[self.row + i][self.col + j])
    
    def click(self) -> bool:
        self.clicked = True
        if self.is_bomb:
            return True
        elif self.number > 0:
            self.image = Images.IMAGES_DICT[self.number]
            return False
        elif self.number == 0:
            self.image = Images.IMAGES_DICT[0]
            for neighbor in self.neighbors:
                if not neighbor.clicked and not neighbor.is_flagged and not neighbor.is_bomb:
                    neighbor.click()
            return False
    
    def switch_flag(self) -> None:
        if not self.clicked:
            self.is_flagged = not self.is_flagged
            if self.is_flagged:
                self.image = Images.IMAGES_DICT['flag']
            else:
                self.image = Images.IMAGES_DICT[0]
