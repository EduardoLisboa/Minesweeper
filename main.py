import pygame
from Constants.constants import Constants
from Assets.images import Images
from spot import Spot
from random import randint

WIN = pygame.display.set_mode((Constants.WIDTH, Constants.HEIGHT + 50))
pygame.display.set_caption("Minesweeper")
pygame.display.set_icon(Images.IMAGES_DICT['icon'])
pygame.font.init()


def draw_grid():
    WIN.fill(Constants.BLACK)
    for i in range(
        0,
        Constants.WIDTH + Constants.SQUARE_SIZE,
        Constants.SQUARE_SIZE
    ):
        vertical = pygame.Rect(i, 0, 2, Constants.HEIGHT)
        horizontal = pygame.Rect(0, i, Constants.WIDTH, 2)
        pygame.draw.rect(WIN, Constants.DARK_GREY, vertical)
        pygame.draw.rect(WIN, Constants.DARK_GREY, horizontal)


def create_board():
    grid = []
    for row in range(0, 20):
        grid.append([])
        for col in range(0, 20):
            grid[row].append(Spot(row, col))
    return grid


def update_neighbors(board):
    for row in board:
        for spot in row:
            spot.update_neighbors(board)
            spot.calc_number()


def create_bombs(board):
    for _ in range(0, Constants.QTD_BOMBS):
        col = randint(0, 19)
        row = randint(0, 19)
        while board[col][row].is_bomb:
            col = randint(0, 19)
            row = randint(0, 19)
        board[col][row].is_bomb = True
        board[col][row].image = Images.IMAGES_DICT['bomb']


def draw_board(board, reveal_bombs=False):
    draw_grid()
    for row in board:
        for spot in row:
            if spot.clicked or spot.is_flagged:
                spot.draw(WIN)
            if reveal_bombs and spot.is_bomb:
                spot.image = Images.IMAGES_DICT['bomb']
                spot.draw(WIN)


def print_text(text):
    draw_text = Constants.TEXT_FONT.render(text, 1, Constants.WHITE)
    black_rect = pygame.Rect(
        0,
        Constants.HEIGHT // 2 - draw_text.get_height() // 2 - 20,
        Constants.WIDTH,
        draw_text.get_height() + 30
    )
    pygame.draw.rect(WIN, Constants.BLACK, black_rect)
    WIN.blit(
        draw_text,
        (
            Constants.WIDTH // 2 - draw_text.get_width() // 2,
            Constants.HEIGHT // 2 - draw_text.get_height() // 2
        )
    )


def parse_mouse_pos(pos):
    mouse_x = pos[0] // Constants.SQUARE_SIZE
    mouse_y = pos[1] // Constants.SQUARE_SIZE
    if mouse_x > 19:
        mouse_x = 19
    if mouse_y > 19:
        mouse_y = 19
    return mouse_x, mouse_y


def in_bounds(pos):
    return 0 <= pos[0] < Constants.WIDTH and 0 <= pos[1] < Constants.HEIGHT


def start_game():
    draw_grid()
    board = create_board()
    create_bombs(board)
    update_neighbors(board)
    draw_board(board)
    return board


def count_bombs_left(board):
    bombs_flagged = 0
    for row in board:
        for spot in row:
            if spot.is_flagged:
                bombs_flagged += 1

    bombs_diff = Constants.QTD_BOMBS - bombs_flagged
    return bombs_diff if bombs_diff >= 0 else 0


def handle_bombs_left(board):
    bombs_left = count_bombs_left(board)
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
    pygame.draw.rect(WIN, Constants.BLACK, black_rect)
    WIN.blit(bombs_qtd_text, (0, Constants.HEIGHT + 5))


def handle_end_game(board, win=False):
    draw_board(board, reveal_bombs=True)
    if win:
        print_text('YOU WIN!')
    else:
        print_text('YOU LOSE!')
    pygame.display.update()
    pygame.time.delay(3000)
    main()


def all_bombs_flagged(board):
    bombs_flagged = 0
    not_bombs_clicked = 0
    for row in board:
        for spot in row:
            if spot.is_flagged and spot.is_bomb:
                bombs_flagged += 1
            if spot.clicked and not spot.is_bomb:
                not_bombs_clicked += 1
    
    not_bombs_spaces = Constants.GRID_SIZE**2 - Constants.QTD_BOMBS

    return bombs_flagged == Constants.QTD_BOMBS or not_bombs_clicked == not_bombs_spaces


def handle_click(click, mouse_x, mouse_y, board):
    if click[0]:
        bomb = board[mouse_x][mouse_y].click()
        if bomb:
            handle_end_game(board, win=False)
    if click[2]:
        board[mouse_x][mouse_y].switch_flag()


def main():
    run = True

    board = start_game()
    clock = pygame.time.Clock()
    
    while run:
        clock.tick(Constants.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = parse_mouse_pos(pygame.mouse.get_pos())

                handle_click(pygame.mouse.get_pressed(), mouse_x, mouse_y, board)
        
        if all_bombs_flagged(board):
            handle_end_game(board, win=True)

        draw_board(board)
        handle_bombs_left(board)
        
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
