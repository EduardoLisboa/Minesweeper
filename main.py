import pygame
from Constants.constants import Constants
from Assets.images import Images
from board import Board

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
    play_again()
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


def play_game() -> None:
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


def menu_texts(main_text: str, subtext=None) -> None:
    WIN.fill(Constants.BLACK)
    text = Constants.TITLE_FONT.render(main_text, True, Constants.WHITE)
    text_rect = text.get_rect(center=(Constants.WIDTH // 2, Constants.HEIGHT // 2 - 50))
    WIN.blit(text, text_rect)

    if subtext:
        text = Constants.BOMB_QTD_FONT.render(subtext, True, Constants.WHITE)
        text_rect = text.get_rect(center=(Constants.WIDTH // 2, Constants.HEIGHT // 2 + 100))
        WIN.blit(text, text_rect)


def main_menu() -> None:
    run = True
    clock = pygame.time.Clock()

    while run:

        menu_texts("Minesweeper", "Press any key to play")

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                play_game()
                run = False

        clock.tick(Constants.FPS)

    pygame.quit()


def play_again():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(Constants.FPS)

        menu_texts("Play again?", "Press any key to play again")

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                play_game()
                run = False

        

    pygame.quit()


if __name__ == "__main__":
    # play_game()
    main_menu()
