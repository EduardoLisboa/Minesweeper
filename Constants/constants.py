import pygame
pygame.font.init()

class Constants:
    WIDTH, HEIGHT = 600, 600
    TEXT_FONT = pygame.font.SysFont('calibri', WIDTH//5)
    BOMB_QTD_FONT = pygame.font.SysFont('calibri', 45)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    DARK_GREY = (70, 70, 70)
    GRID_SIZE = 20
    SQUARE_SIZE = WIDTH // GRID_SIZE
    QTD_BOMBS = 60
    FPS = 60
