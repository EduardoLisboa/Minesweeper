import pygame
import os
from Constants.constants import SQUARE_SIZE

BOMB_ICON = pygame.image.load(os.path.join('Assets', 'PNGs', 'bomb_icon.png'))

BOMB_IMAGE = pygame.image.load(os.path.join('Assets', 'PNGs', 'bomb.png'))
BOMB = pygame.transform.scale(BOMB_IMAGE, (SQUARE_SIZE - 5, SQUARE_SIZE - 5))

FLAG_IMAGE = pygame.image.load(os.path.join('Assets', 'PNGs', 'flag.png'))
FLAG = pygame.transform.scale(FLAG_IMAGE, (SQUARE_SIZE - 5, SQUARE_SIZE - 5))

EMPTY_IMAGE = pygame.image.load(os.path.join('Assets', 'PNGs', 'square.png'))
EMPTY = pygame.transform.scale(EMPTY_IMAGE, (SQUARE_SIZE - 5, SQUARE_SIZE - 5))

ONE_IMAGE = pygame.image.load(os.path.join('Assets', 'PNGs', '1.png'))
ONE = pygame.transform.scale(ONE_IMAGE, (SQUARE_SIZE - 5, SQUARE_SIZE - 5))

TWO_IMAGE = pygame.image.load(os.path.join('Assets', 'PNGs', '2.png'))
TWO = pygame.transform.scale(TWO_IMAGE, (SQUARE_SIZE - 5, SQUARE_SIZE - 5))

THREE_IMAGE = pygame.image.load(os.path.join('Assets', 'PNGs', '3.png'))
THREE = pygame.transform.scale(THREE_IMAGE, (SQUARE_SIZE - 5, SQUARE_SIZE - 5))

FOUR_IMAGE = pygame.image.load(os.path.join('Assets', 'PNGs', '4.png'))
FOUR = pygame.transform.scale(FOUR_IMAGE, (SQUARE_SIZE - 5, SQUARE_SIZE - 5))

FIVE_IMAGE = pygame.image.load(os.path.join('Assets', 'PNGs', '5.png'))
FIVE = pygame.transform.scale(FIVE_IMAGE, (SQUARE_SIZE - 5, SQUARE_SIZE - 5))

SIX_IMAGE = pygame.image.load(os.path.join('Assets', 'PNGs', '6.png'))
SIX = pygame.transform.scale(SIX_IMAGE, (SQUARE_SIZE - 5, SQUARE_SIZE - 5))

SEVEN_IMAGE = pygame.image.load(os.path.join('Assets', 'PNGs', '7.png'))
SEVEN = pygame.transform.scale(SEVEN_IMAGE, (SQUARE_SIZE - 5, SQUARE_SIZE - 5))

EIGHT_IMAGE = pygame.image.load(os.path.join('Assets', 'PNGs', '8.png'))
EIGHT = pygame.transform.scale(EIGHT_IMAGE, (SQUARE_SIZE - 5, SQUARE_SIZE - 5))

NUMBERS_DICT = {
    1: ONE,
    2: TWO,
    3: THREE,
    4: FOUR,
    5: FIVE,
    6: SIX,
    7: SEVEN,
    8: EIGHT
}
