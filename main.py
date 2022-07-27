import pygame
from Constants.constants import *
from Assets.images import *
from random import randint

WIN = pygame.display.set_mode((WIDTH, HEIGHT + 50))
pygame.display.set_caption("Minesweeper")
pygame.display.set_icon(BOMB_ICON)

def make_table():
    WIN.fill(BLACK)
    for i in range(SQUARE_SIZE, WIDTH + SQUARE_SIZE, SQUARE_SIZE):
        vertical = pygame.Rect(i, 0, 2, HEIGHT)
        horizontal = pygame.Rect(0, i, WIDTH, 2)
        pygame.draw.rect(WIN, DARK_GREY, vertical)
        pygame.draw.rect(WIN, DARK_GREY, horizontal)


def is_bomb(mouse_x, mouse_y, bombs):
    if (mouse_x, mouse_y) in bombs:
        return True
    else:
        return False


def check_bombs(mouse_x, mouse_y, bombs):
    cont = 0
    for col in range(-1, 2):
        for row in range(-1, 2):
            if col == 0 and row == 0 or mouse_x < 0 or mouse_x > 19 or mouse_y < 0 or mouse_y > 19:
                continue
            if (mouse_x + col, mouse_y + row) in bombs:
                cont += 1

    return cont


def check_empty_spaces(mouse_x, mouse_y, bombs, empty_spaces, visited, not_bomb, numbers):
    if (mouse_x, mouse_y) in visited or mouse_x < 0 or mouse_x > 19 or mouse_y < 0 or mouse_y > 19:
        return
    num_bombs = check_bombs(mouse_x, mouse_y, bombs)
    if num_bombs == 0 and (mouse_x, mouse_y) not in visited:
        if (mouse_x, mouse_y) not in not_bomb and (mouse_x, mouse_y) not in bombs and mouse_x >= 0 and mouse_x <= 19 and mouse_y >= 0 and mouse_y <= 19:
            not_bomb.append((mouse_x, mouse_y))
        empty_spaces.append([(mouse_x, mouse_y), 0])
    elif num_bombs > 0 and (mouse_x, mouse_y) not in visited:
        if (mouse_x, mouse_y) not in not_bomb and (mouse_x, mouse_y) not in bombs and mouse_x >= 0 and mouse_x <= 19 and mouse_y >= 0 and mouse_y <= 19:
            not_bomb.append((mouse_x, mouse_y))
        empty_spaces.append([(mouse_x, mouse_y), num_bombs])
        numbers.append((mouse_x, mouse_y))
        return
    
    visited.append((mouse_x, mouse_y))

    for col in range(-1, 2):
        for row in range(-1, 2):
            if col == 0 and row == 0 or mouse_x < 0 or mouse_x > 19 or mouse_y < 0 or mouse_y > 19:
                continue
            check_empty_spaces(mouse_x + col, mouse_y + row, bombs, empty_spaces, visited, not_bomb, numbers)


def create_bombs():
    bombs = list()
    bombs.clear()
    col = randint(0, 19)
    row = randint(0, 19)
    for _ in range(0, QTD_BOMBS):
        while (col, row) in bombs:
            col = randint(0, 19)
            row = randint(0, 19)
        bombs.append((col, row))

    no_bombs = list()
    no_bombs.clear()
    for col in range(0, 20):
        for row in range(0, 20):
            if (col, row) not in bombs:
                no_bombs.append((col, row))

    return bombs, no_bombs


def draw_bombs(bombs, image):
    for bomb in bombs:
        black_square = pygame.Rect(bomb[0] * SQUARE_SIZE + 2, bomb[1] * SQUARE_SIZE + 2, SQUARE_SIZE - 3, SQUARE_SIZE - 3)
        pygame.draw.rect(WIN, BLACK, black_square)
        WIN.blit(image, (bomb[0] * SQUARE_SIZE + 3, bomb[1] * SQUARE_SIZE + 3))


def draw_number(mouse_x, mouse_y, num_bombs):
    WIN.blit(NUMBERS_DICT[num_bombs], (mouse_x * SQUARE_SIZE + 3, mouse_y * SQUARE_SIZE + 3))


def draw_empty_spaces(empty_spaces):
    for space in empty_spaces:
        if space[1] == 0:
            WIN.blit(EMPTY, (space[0][0] * SQUARE_SIZE + 3, space[0][1] * SQUARE_SIZE + 3))
        else:
            draw_number(space[0][0], space[0][1], space[1])


def print_text(text):
    draw_text = TEXT_FONT.render(text, 1, WHITE)
    black_rect = pygame.Rect(0, HEIGHT // 2 - draw_text.get_height() // 2 - 20, WIDTH, draw_text.get_height() + 30)
    pygame.draw.rect(WIN, BLACK, black_rect)
    WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, HEIGHT // 2 - draw_text.get_height() // 2))


def main():
    run = True
    
    make_table()

    bombs, no_bombs = create_bombs()
    not_bomb = list()

    pressed = list()
    numbers = list()
    empty_spaces = list()
    flags = list()
    visited = list()

    clock = pygame.time.Clock()
    
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
            
                pos = pygame.mouse.get_pos()
                mouse_x, mouse_y = pos[0] // SQUARE_SIZE, pos[1] // SQUARE_SIZE
                button = pygame.mouse.get_pressed()

                if button == (1, 0, 0) and (mouse_x, mouse_y) not in pressed:
                    pressed.append((mouse_x, mouse_y))

                    if is_bomb(mouse_x, mouse_y, bombs):
                        draw_bombs(bombs, BOMB)
                        print_text('YOU LOSE!')
                        pygame.display.update()
                        pygame.time.delay(3000)
                        main()
                    else:
                        num_bombs = check_bombs(mouse_x, mouse_y, bombs)
                        if num_bombs > 0:
                            draw_number(mouse_x, mouse_y, num_bombs)
                            numbers.append((mouse_x, mouse_y))
                            not_bomb.append((mouse_x, mouse_y))
                        else: # EMPTY SPACE
                            check_empty_spaces(mouse_x, mouse_y, bombs, empty_spaces, visited, not_bomb, numbers)
                            draw_empty_spaces(empty_spaces)
                            pressed.extend(empty_spaces[:])
                            empty_spaces.clear()
                if button == (0, 0, 1):
                    if (mouse_x, mouse_y) not in pressed and (mouse_x, mouse_y) not in numbers and (mouse_x, mouse_y) not in empty_spaces:
                        pressed.append((mouse_x, mouse_y))
                        black_square = pygame.Rect(mouse_x * SQUARE_SIZE + 2, mouse_y * SQUARE_SIZE + 2, SQUARE_SIZE - 3, SQUARE_SIZE - 3)
                        pygame.draw.rect(WIN, BLACK, black_square)
                        WIN.blit(FLAG, (mouse_x * SQUARE_SIZE + 3, mouse_y * SQUARE_SIZE + 3))
                        flags.append((mouse_x, mouse_y))
                    elif (mouse_x, mouse_y) in pressed and (mouse_x, mouse_y) in flags:
                        flags.remove((mouse_x, mouse_y))
                        pressed.remove((mouse_x, mouse_y))
                        black_square = pygame.Rect(mouse_x * SQUARE_SIZE + 2, mouse_y * SQUARE_SIZE + 2, SQUARE_SIZE - 3, SQUARE_SIZE - 3)
                        pygame.draw.rect(WIN, BLACK, black_square)

        if len(not_bomb) == len(no_bombs):
            draw_bombs(bombs, FLAG)
            print_text('YOU WIN!')
            pygame.display.update()
            pygame.time.delay(3000)
            main()

        # draw_bombs(bombs, BOMB)
        bombs_left = len(bombs) - len(flags) if len(bombs) - len(flags) >= 0 else 0
        bombs_qtd_text = BOMB_QTD_FONT.render(f'BOMBS LEFT: {bombs_left}', 1, WHITE)
        black_rect = pygame.Rect(0, HEIGHT + 4, bombs_qtd_text.get_width() + 40, bombs_qtd_text.get_height() - 3)
        pygame.draw.rect(WIN, BLACK, black_rect)
        WIN.blit(bombs_qtd_text, (0, HEIGHT + 5))
        pygame.display.update()

    
    pygame.quit()


if __name__ == "__main__":
    main()
