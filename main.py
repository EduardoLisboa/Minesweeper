import pygame
from Constants.constants import Constants
from Assets.images import Images
from spot import Spot
from board import Board
from random import randint

WIN = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT + 50))
pygame.display.set_caption("Minesweeper")
pygame.display.set_icon(Images.IMAGES_DICT['icon'])
pygame.font.init()


def parse_mouse_pos(pos: tuple[int, int]) -> tuple[int, int]:
    mouse_x = pos[0] // Constants.SQUARE_SIZE
    mouse_y = pos[1] // Constants.SQUARE_SIZE
    if mouse_x > 19:
        mouse_x = 19
    if mouse_y > 19:
        mouse_y = 19
    return mouse_x, mouse_y


def handle_end_game(board: Board, win: bool=False) -> None:
    board.draw_board(WIN, reveal_bombs=True)
    if win:
        board.print_text(WIN, 'YOU WIN!')
    else:
        board.print_text(WIN, 'YOU LOSE!')
    pygame.display.update()
    pygame.time.delay(3000)
    main()
    exit()


def handle_click(click: tuple[bool, bool, bool], mouse_x: int, mouse_y: int, board: Board) -> None:
    # Left click
    if click[0]:
        bomb = board.game_board[mouse_x][mouse_y].click()
        if bomb:
            handle_end_game(board, win=False)
    # Right click
    if click[2]:
        board.game_board[mouse_x][mouse_y].switch_flag()


def main() -> None:
    run = True

    board = Board(WIN)
    clock = pygame.time.Clock()
    
    while run:
        clock.tick(Constants.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = parse_mouse_pos(pygame.mouse.get_pos())

                handle_click(pygame.mouse.get_pressed(), mouse_x, mouse_y, board)
        
        if board.all_bombs_flagged():
            handle_end_game(board, win=True)

        board.draw_board(WIN)
        board.handle_bombs_left(WIN)
        
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
