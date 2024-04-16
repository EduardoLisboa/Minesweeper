import pygame
import os
from Constants.constants import Constants

class Images:

    @staticmethod
    def load_img(filename):
        return pygame.image.load(
            os.path.join('Assets', 'PNGs', filename)
        )

    @staticmethod
    def rescale(image):
        rescaled = pygame.transform.scale(
            image,
            (
                Constants.SQUARE_SIZE - 4,
                Constants.SQUARE_SIZE - 4
            )
        )
        return rescaled
    
    BOMB_ICON = load_img('bomb_icon.png')

    BOMB_IMAGE = load_img('bomb.png')
    BOMB = rescale(BOMB_IMAGE)

    FLAG_IMAGE = load_img('flag.png')
    FLAG = rescale(FLAG_IMAGE)

    EMPTY_IMAGE = load_img('square.png')
    EMPTY = rescale(EMPTY_IMAGE)

    ONE_IMAGE = load_img('1.png')
    ONE = rescale(ONE_IMAGE)

    TWO_IMAGE = load_img('2.png')
    TWO = rescale(TWO_IMAGE)

    THREE_IMAGE = load_img('3.png')
    THREE = rescale(THREE_IMAGE)

    FOUR_IMAGE = load_img('4.png')
    FOUR = rescale(FOUR_IMAGE)

    FIVE_IMAGE = load_img('5.png')
    FIVE = rescale(FIVE_IMAGE)

    SIX_IMAGE = load_img('6.png')
    SIX = rescale(SIX_IMAGE)

    SEVEN_IMAGE = load_img('7.png')
    SEVEN = rescale(SEVEN_IMAGE)

    EIGHT_IMAGE = load_img('8.png')
    EIGHT = rescale(EIGHT_IMAGE)

    IMAGES_DICT = {
        0: EMPTY,
        1: ONE,
        2: TWO,
        3: THREE,
        4: FOUR,
        5: FIVE,
        6: SIX,
        7: SEVEN,
        8: EIGHT,
        "bomb": BOMB,
        "flag": FLAG,
        "icon": BOMB_ICON
    }
