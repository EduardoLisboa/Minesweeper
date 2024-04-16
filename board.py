from Constants.constants import Constants
from Assets.images import Images
from spot import Spot

import pygame
from random import randint

class Board:

    def __init__(self, win) -> None:
        self.game_board = self.create_board()
        self.start_game(win)
    
    def start_game(self, win):
        self.create_bombs()
        self.update_neighbors()
        self.draw_board(win)

    @staticmethod
    def create_board() -> list[list[Spot]]:
        board = []
        for row in range(0, 20):
            board.append([])
            for col in range(0, 20):
                board[row].append(Spot(row, col))
        return board
    
    def create_bombs(self) -> None:
        for _ in range(0, Constants.QTD_BOMBS):
            col = randint(0, 19)
            row = randint(0, 19)
            while self.game_board[col][row].is_bomb:
                col = randint(0, 19)
                row = randint(0, 19)
            self.game_board[col][row].is_bomb = True
            self.game_board[col][row].image = Images.IMAGES_DICT['bomb']

    def update_neighbors(self) -> None:
        for row in self.game_board:
            for spot in row:
                spot.update_neighbors(self.game_board)
                spot.calc_number()

    def draw_grid(self, win):
        win.fill(Constants.BLACK)
        for i in range(
            0,
            Constants.WIDTH + Constants.SQUARE_SIZE,
            Constants.SQUARE_SIZE
        ):
            vertical = pygame.Rect(i, 0, 2, Constants.HEIGHT)
            horizontal = pygame.Rect(0, i, Constants.WIDTH, 2)
            pygame.draw.rect(win, Constants.DARK_GREY, vertical)
            pygame.draw.rect(win, Constants.DARK_GREY, horizontal)

    def draw_board(self, win, reveal_bombs=False):
        self.draw_grid(win)
        for row in self.game_board:
            for spot in row:
                if spot.clicked or spot.is_flagged:
                    spot.draw(win)
                if reveal_bombs and spot.is_bomb:
                    spot.image = Images.IMAGES_DICT['bomb']
                    spot.draw(win)

    def all_bombs_flagged(self) -> bool:
        bombs_flagged = 0
        not_bombs_clicked = 0
        for row in self.game_board:
            for spot in row:
                if spot.is_flagged and spot.is_bomb:
                    bombs_flagged += 1
                if spot.clicked and not spot.is_bomb:
                    not_bombs_clicked += 1
        
        not_bombs_spaces = Constants.GRID_SIZE**2 - Constants.QTD_BOMBS

        return bombs_flagged == Constants.QTD_BOMBS or not_bombs_clicked == not_bombs_spaces
    
    def count_bombs_left(self) -> int:
        bombs_flagged = 0
        for row in self.game_board:
            for spot in row:
                if spot.is_flagged:
                    bombs_flagged += 1

        bombs_diff = Constants.QTD_BOMBS - bombs_flagged
        return bombs_diff if bombs_diff >= 0 else 0

    def handle_bombs_left(self, window) -> None:
        bombs_left = self.count_bombs_left()
        bombs_qtd_text = Constants.BOMB_QTD_FONT.render(
            f'BOMBS LEFT: {bombs_left}',
            1,
            Constants.WHITE
        )
        black_rect = pygame.Rect(
            0,
            Constants.HEIGHT + 4,
            bombs_qtd_text.get_width() + 40,
            bombs_qtd_text.get_height() - 3
        )
        pygame.draw.rect(window, Constants.BLACK, black_rect)
        window.blit(bombs_qtd_text, (0, Constants.HEIGHT + 5))
    
    @staticmethod
    def print_text(window, text):
        draw_text = Constants.TEXT_FONT.render(text, 1, Constants.WHITE)
        black_rect = pygame.Rect(
            0,
            Constants.HEIGHT // 2 - draw_text.get_height() // 2 - 20,
            Constants.WIDTH,
            draw_text.get_height() + 30
        )
        pygame.draw.rect(window, Constants.BLACK, black_rect)
        window.blit(
            draw_text,
            (
                Constants.WIDTH // 2 - draw_text.get_width() // 2,
                Constants.HEIGHT // 2 - draw_text.get_height() // 2
            )
        )
