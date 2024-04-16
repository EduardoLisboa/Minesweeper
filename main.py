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


# def is_bomb(mouse_x, mouse_y, bombs):
#     return (mouse_x, mouse_y) in bombs


# def in_center_cell(col, row):
#     return col == 0 and row == 0


# def mouse_in_bounds(mouse_x, mouse_y):
#     return mouse_x >= 0 and mouse_x <= 19 and mouse_y >= 0 and mouse_y <= 19


# def count_bombs(mouse_x, mouse_y, bombs):
#     cont = 0
#     for col in range(-1, 2):
#         for row in range(-1, 2):
#             if in_center_cell(col, row) or not mouse_in_bounds(mouse_x, mouse_y):
#                 continue
#             if (mouse_x + col, mouse_y + row) in bombs:
#                 cont += 1

#     return cont


# def check_empty_spaces(mouse_x, mouse_y, bombs, empty_spaces, visited, not_bomb, numbers):
#     if (mouse_x, mouse_y) in visited or mouse_x < 0 or mouse_x > 19 or mouse_y < 0 or mouse_y > 19:
#         return
#     num_bombs = count_bombs(mouse_x, mouse_y, bombs)
#     if num_bombs == 0 and (mouse_x, mouse_y) not in visited:
#         if (mouse_x, mouse_y) not in not_bomb and (mouse_x, mouse_y) not in bombs and mouse_x >= 0 and mouse_x <= 19 and mouse_y >= 0 and mouse_y <= 19:
#             not_bomb.append((mouse_x, mouse_y))
#         empty_spaces.append([(mouse_x, mouse_y), 0])
#     elif num_bombs > 0 and (mouse_x, mouse_y) not in visited:
#         if (mouse_x, mouse_y) not in not_bomb and (mouse_x, mouse_y) not in bombs and mouse_x >= 0 and mouse_x <= 19 and mouse_y >= 0 and mouse_y <= 19:
#             not_bomb.append((mouse_x, mouse_y))
#         empty_spaces.append([(mouse_x, mouse_y), num_bombs])
#         numbers.append((mouse_x, mouse_y))
#         return
    
#     visited.append((mouse_x, mouse_y))

#     for col in range(-1, 2):
#         for row in range(-1, 2):
#             if col == 0 and row == 0 or mouse_x < 0 or mouse_x > 19 or mouse_y < 0 or mouse_y > 19:
#                 continue
#             check_empty_spaces(mouse_x + col, mouse_y + row, bombs, empty_spaces, visited, not_bomb, numbers)


# def create_bombs():
#     bombs = list()
#     bombs.clear()
#     col = randint(0, 19)
#     row = randint(0, 19)
#     for _ in range(0, Constants.QTD_BOMBS):
#         while (col, row) in bombs:
#             col = randint(0, 19)
#             row = randint(0, 19)
#         bombs.append((col, row))

#     no_bombs = list()
#     no_bombs.clear()
#     for col in range(0, 20):
#         for row in range(0, 20):
#             if (col, row) not in bombs:
#                 no_bombs.append((col, row))

#     return bombs, no_bombs


# def draw_bombs(bombs, image):
#     for bomb in bombs:
#         black_square = pygame.Rect(
#             bomb[0] * Constants.SQUARE_SIZE + 2,
#             bomb[1] * Constants.SQUARE_SIZE + 2,
#             Constants.SQUARE_SIZE - 3,
#             Constants.SQUARE_SIZE - 3
#         )
#         pygame.draw.rect(WIN, Constants.BLACK, black_square)
#         WIN.blit(
#             image, 
#             (
#                 bomb[0] * Constants.SQUARE_SIZE + 3,
#                 bomb[1] * Constants.SQUARE_SIZE + 3
#             )
#         )


# def draw_number(mouse_x, mouse_y, num_bombs):
#     WIN.blit(
#         Images.IMAGES_DICT[num_bombs],
#         (
#             mouse_x * Constants.SQUARE_SIZE + 3,
#             mouse_y * Constants.SQUARE_SIZE + 3
#         )
#     )


# def draw_empty_spaces(empty_spaces):
#     for space in empty_spaces:
#         if space[1] == 0:
#             WIN.blit(
#                 Images.IMAGES_DICT['empty'],
#                 (
#                     space[0][0] * Constants.SQUARE_SIZE + 3,
#                     space[0][1] * Constants.SQUARE_SIZE + 3
#                 )
#             )
#         else:
#             draw_number(space[0][0], space[0][1], space[1])


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


def main():
    run = True
    
    draw_grid()

    board = create_board()
    create_bombs(board)
    update_neighbors(board)
    draw_board(board)

    # bombs, no_bombs = create_bombs()
    # not_bomb = list()

    # pressed = list()
    # numbers = list()
    # empty_spaces = list()
    # flags = list()
    # visited = list()

    clock = pygame.time.Clock()
    
    while run:
        clock.tick(Constants.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                mouse_x, mouse_y = parse_mouse_pos(pos)

                # Left mouse click
                if pygame.mouse.get_pressed()[0]:
                    bomb = board[mouse_x][mouse_y].click()
                    draw_board(board)
                    if bomb:
                        draw_board(board, reveal_bombs=True)
                        print_text('YOU LOSE!')
                        pygame.display.update()
                        pygame.time.delay(3000)
                        main()
                # Right mouse click
                if pygame.mouse.get_pressed()[2]:
                    board[mouse_x][mouse_y].switch_flag()
                    draw_board(board)
            
                # pos = pygame.mouse.get_pos()
                # mouse_x = pos[0] // Constants.SQUARE_SIZE
                # mouse_y = pos[1] // Constants.SQUARE_SIZE

                # # Left mouse click
                # if pygame.mouse.get_pressed()[0] and (mouse_x, mouse_y) not in pressed:
                #     pressed.append((mouse_x, mouse_y))

                #     if is_bomb(mouse_x, mouse_y, bombs):
                #         draw_bombs(bombs, Images.IMAGES_DICT['bomb'])
                #         print_text('YOU LOSE!')
                #         pygame.display.update()
                #         pygame.time.delay(3000)
                #         main()
                #     else:
                #         num_bombs = count_bombs(mouse_x, mouse_y, bombs)
                #         if num_bombs > 0:
                #             draw_number(mouse_x, mouse_y, num_bombs)
                #             numbers.append((mouse_x, mouse_y))
                #             not_bomb.append((mouse_x, mouse_y))
                #         else: # EMPTY SPACE
                #             check_empty_spaces(mouse_x, mouse_y, bombs, empty_spaces, visited, not_bomb, numbers)
                #             draw_empty_spaces(empty_spaces)
                #             pressed.extend(empty_spaces[:])
                #             empty_spaces.clear()
                # # Right mouse click
                # if pygame.mouse.get_pressed()[2]:
                #     if (mouse_x, mouse_y) not in pressed and (mouse_x, mouse_y) not in numbers and (mouse_x, mouse_y) not in empty_spaces:
                #         pressed.append((mouse_x, mouse_y))
                #         black_square = pygame.Rect(
                #             mouse_x * Constants.SQUARE_SIZE + 2,
                #             mouse_y * Constants.SQUARE_SIZE + 2,
                #             Constants.SQUARE_SIZE - 3,
                #             Constants.SQUARE_SIZE - 3
                #         )
                #         pygame.draw.rect(WIN, Constants.BLACK, black_square)
                #         WIN.blit(
                #             Images.IMAGES_DICT['flag'],
                #             (
                #                 mouse_x * Constants.SQUARE_SIZE + 3,
                #                 mouse_y * Constants.SQUARE_SIZE + 3
                #             )
                #         )
                #         flags.append((mouse_x, mouse_y))
                #     elif (mouse_x, mouse_y) in pressed and (mouse_x, mouse_y) in flags:
                #         flags.remove((mouse_x, mouse_y))
                #         pressed.remove((mouse_x, mouse_y))
                #         black_square = pygame.Rect(
                #             mouse_x * Constants.SQUARE_SIZE + 2,
                #             mouse_y * Constants.SQUARE_SIZE + 2,
                #             Constants.SQUARE_SIZE - 3,
                #             Constants.SQUARE_SIZE - 3
                #         )
                #         pygame.draw.rect(WIN, Constants.BLACK, black_square)

        # if len(not_bomb) == len(no_bombs):
        #     draw_bombs(bombs, Images.IMAGES_DICT['flag'])
        #     print_text('YOU WIN!')
        #     pygame.display.update()
        #     pygame.time.delay(3000)
        #     main()

        # draw_bombs(bombs, BOMB)
        # bombs_left = len(bombs) - len(flags) if len(bombs) - len(flags) >= 0 else 0
        # bombs_qtd_text = Constants.BOMB_QTD_FONT.render(
        #     f'BOMBS LEFT: {bombs_left}',
        #     1,
        #     Constants.WHITE
        # )
        # black_rect = pygame.Rect(
        #     0,
        #     Constants.HEIGHT + 4,
        #     bombs_qtd_text.get_width() + 40,
        #     bombs_qtd_text.get_height() - 3
        # )
        # pygame.draw.rect(WIN, Constants.BLACK, black_rect)
        # WIN.blit(bombs_qtd_text, (0, Constants.HEIGHT + 5))
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
