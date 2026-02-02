import pygame
from Constants.constants import Constants
from Assets.images import Images
from board import Board
from button import Button
from slider import Slider

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


def create_button(
        button_text: str,
        x_y_displacement: tuple[int, int],
        hovering_color: tuple[int, int, int]
    ) -> Button:
    return Button(
        image=None,
        pos=(
            Constants.WIDTH // 2 + x_y_displacement[0],
            Constants.HEIGHT // 2 + x_y_displacement[1]
        ),
        text_input=button_text,
        font=Constants.YES_NO_FONT,
        base_color=Constants.WHITE,
        hovering_color=hovering_color
    )

def start_text(bomb_qtd: int) -> None:
    title_text = Constants.TITLE_FONT.render('Difficulty', True, Constants.WHITE)
    title_rect = title_text.get_rect(center=(Constants.WIDTH // 2, 100))
    WIN.blit(title_text, title_rect)

    slider_label = Constants.BOMB_QTD_FONT.render('Number of Bombs:', True, Constants.WHITE)
    label_rect = slider_label.get_rect(center=(Constants.WIDTH // 2, Constants.HEIGHT // 2 - 100))
    WIN.blit(slider_label, label_rect)

    value_text = Constants.BOMB_QTD_FONT.render(str(bomb_qtd), True, Constants.LIGHT_YELLOW)
    value_rect = value_text.get_rect(center=(Constants.WIDTH // 2, Constants.HEIGHT // 2 + 20))
    WIN.blit(value_text, value_rect)


def difficulty_selection():
    run = True
    clock = pygame.time.Clock()

    slider = Slider(
        x=Constants.WIDTH // 2 - 200,
        y=Constants.HEIGHT // 2 - 50,
        width=400,
        min_value=10,
        max_value=150,
        initial_value=60
    )

    start_button = create_button('START', (0, 150), Constants.LIGHT_GREEN)

    while run:
        clock.tick(Constants.FPS)
        WIN.fill(Constants.BLACK)

        start_text(slider.get_value())

        slider.draw(WIN)
        
        mouse_pos = pygame.mouse.get_pos()
        start_button.change_color(mouse_pos)
        start_button.update(WIN)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            slider.handle_event(event)
            
            if event.type == pygame.MOUSEBUTTONDOWN and start_button.check_for_input(mouse_pos):
                Constants.QTD_BOMBS = slider.get_value()
                play_game()
                run = False


def handle_buttons(buttons: tuple[Button, Button], mouse_pos: tuple[int, int]) -> bool | None:
    if buttons[0].check_for_input(mouse_pos):
        # play_game()
        difficulty_selection()
        return False
    if buttons[1].check_for_input(mouse_pos):
        return False


def main_menu() -> None:
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(Constants.FPS)
        
        BUTTONS = (
            create_button("PLAY", (-100, 100), Constants.LIGHT_GREEN),
            create_button("QUIT", (100, 100), Constants.LIGHT_RED)
        )

        menu_texts("Minesweeper")

        mouse_pos = pygame.mouse.get_pos()

        for button in BUTTONS:
            button.change_color(mouse_pos)
            button.update(WIN)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = handle_buttons(BUTTONS, mouse_pos)

    pygame.quit()


def play_again():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(Constants.FPS)

        BUTTONS = (
            create_button("YES", (-100, 100), Constants.LIGHT_GREEN),
            create_button("NO", (100, 100), Constants.LIGHT_RED)
        )

        menu_texts("Play again?")

        mouse_pos = pygame.mouse.get_pos()

        for button in BUTTONS:
            button.change_color(mouse_pos)
            button.update(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                run = handle_buttons(BUTTONS, mouse_pos)

        pygame.display.update()
        

    pygame.quit()


if __name__ == "__main__":
    # play_game()
    main_menu()
