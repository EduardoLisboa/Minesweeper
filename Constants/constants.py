import pygame
pygame.font.init()

class Constants:
    WIDTH, HEIGHT = 600, 600
    TEXT_FONT = pygame.font.SysFont('calibri', WIDTH//5)
    BOMB_QTD_FONT = pygame.font.SysFont('calibri', 50)
    TITLE_FONT = pygame.font.SysFont('calibri', 100)
    YES_NO_FONT = pygame.font.SysFont('calibri', 75)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    DARK_GREY = (70, 70, 70)
    LIGHT_GREEN = (80, 250, 123)
    LIGHT_YELLOW = (248, 248, 89)
    LIGHT_RED = (255, 85, 85)
    GRID_SIZE: int = 20
    SQUARE_SIZE: int = WIDTH // GRID_SIZE
    QTD_BOMBS: int = 60
    FPS: int = 60