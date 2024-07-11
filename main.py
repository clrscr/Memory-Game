import pygame
from sys import exit
from dataclasses import dataclass
import random


card_image = pygame.image.load('card.jpg')
font = None
font_color = None
@dataclass
class GameSettings:
    should_full_screen: bool = False
    bg_color = pygame.Color('white')


class MGCard(pygame.sprite.Sprite):
    def __init__(self, screen, card_value):
        super().__init__()
        self.screen = screen
        if self.screen is None:
            print("Failed to create card.")

        self.image = card_image

        if self.image is None:
            print("Failed to load image!!")

        self.rect = self.image.get_rect()

        self.rect.x = 0
        self.rect.y = 0

        self.x = float(self.rect.x)

        self.card_value = card_value
        self.is_flipped = False

    def clicked(self):
        self.is_flipped = not self.is_flipped
        if self.is_flipped:
            text_surface = font.render(str(self.card_value), True, font_color)
            text_rect = self.image.get_rect(center=self.image.get_rect().center)
            self.image = text_surface
            pygame.transform.smoothscale(self.image, card_image.get_size())
            pygame.draw.rect(self.image, 'red', self.image.get_rect(), 1)
            self.image.blit(text_surface, text_rect)
        else:
            self.image = card_image


class MemoryGame:
    def __init__(self, height=4, width=4):
        if height * width % 2 != 0:
            print("Invalid board size")

        print("Setting up board")
        self.width = width
        self.height = height
        self.game_board = list()
        self.settings = GameSettings()
        self.engine = MemoryGameEngine(self.draw_board, self.handle_input, self.settings)

        print("Setting up cards")
        self.cards = pygame.sprite.Group()
        self.create_board()

        global font
        font = pygame.font.SysFont('Arial', 20)
        global font_color
        font_color = pygame.Color('black')

        card_image.convert()

        print("Game initialized")

    def create_board(self):
        board_size = self.width * self.height

        self.game_board = [random.randrange(0, 99) for _ in range(int(board_size / 2))]
        self.game_board.extend(self.game_board)
        random.shuffle(self.game_board)
        print(len(self.game_board))
        print(self.game_board)

        if self.engine.screen is None:
            print("Failed to create game board!")
        self._create_cards()

    def _create_cards(self):
        card = MGCard(self.engine.screen, 0)
        card_width = card.rect.width
        current_x = 1
        current_y = 1
        for j in range(self.height):
            for k in range(self.width):
                new_card = MGCard(self.engine.screen, self.game_board[j * self.width] + k)

                new_card.x = current_x
                new_card.rect.x = current_x

                new_card.y = current_y
                new_card.rect.y = current_y
                self.cards.add(new_card)

                current_x += 1.25 * card_width

            current_x = 1
            current_y += card.rect.height

    def start_game(self):
        self.engine.run_game()

    def draw_board(self):
        self.engine.screen.fill(self.settings.bg_color)
        self.cards.draw(self.engine.screen)
        pygame.display.flip()

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            clicked_card = [card for card
                            in self.cards if card.rect.collidepoint(mouse_pos)]
            clicked_card[0].clicked()
            print(clicked_card[0].card_value)


class MemoryGameEngine:
    def __init__(self, draw_function, input_handler, settings):
        pygame.init()
        self.screen = None
        self.clock = pygame.time.Clock()
        self.game_active = False
        self.draw_function = draw_function
        self.settings = settings
        self.setup_display()
        self.cards = pygame.sprite.Group()
        self.input_handler = input_handler
        pygame.display.set_caption('Memory Game')

    def run_game(self):
        while True:
            self._check_events()
            self._update_screen()
            self.clock.tick(60)

    def _update_screen(self):
        self.draw_function()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            else:
                self.input_handler(event)

    def setup_display(self):
        if self.settings.should_full_screen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_width()
            self.settings.screen_height = self.screen.get_height()
        else:
            self.settings.screen_width = 800
            self.settings.screen_height = 900
            self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))


if __name__ == '__main__':
    mg = MemoryGame()
    mg.start_game()
