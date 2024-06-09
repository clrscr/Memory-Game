import pygame
from sys import exit
from dataclasses import dataclass
import random


@dataclass
class GameSettings:
    should_full_screen: bool = False
    bg_color = pygame.Color('white')


class MGCard(pygame.sprite.Sprite):
    def __init__(self, screen):
        print("Creating card...")
        super().__init__()
        self.screen = screen
        if self.screen is None:
            print("Failed to create card.")

        self.image = pygame.image.load('card.jpg')
        self.image = self.image.convert()

        if self.image is None:
            print("Failed to load image!!")

        self.rect = self.image.get_rect()

        self.rect.x = 0
        self.rect.y = 0

        self.x = float(self.rect.x)
        print("Card created successfully!...")


class MemoryGame:
    def __init__(self, height=4, width=4):
        if height * width % 2 != 0:
            print("Invalid board size")

        print("Setting up board")
        self.width = width
        self.height = height
        self.game_board = list()
        self.settings = GameSettings()
        self.engine = MemoryGameEngine(self.draw_board, self.settings)

        print("Setting up cards")
        self.cards = pygame.sprite.Group()
        self.create_board()

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
        card = MGCard(self.engine.screen)
        self.cards.add(card)

    def start_game(self):
        self.engine.run_game()

    def draw_board(self):
        self.engine.screen.fill(self.settings.bg_color)
        self.cards.draw(self.engine.screen)
        pygame.display.flip()


class MemoryGameEngine:
    def __init__(self, draw_function, settings):
        pygame.init()
        self.screen = None
        self.clock = pygame.time.Clock()
        self.game_active = False
        self.draw_function = draw_function
        self.settings = settings
        self.setup_display()
        self.cards = pygame.sprite.Group()
        pygame.display.set_caption('Memory Game')

    def run_game(self):
        while True:
            self._check_events()
            self._update_screen()
            self.clock.tick(60)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_q:
            exit()

    def _check_keyup_events(self, event):
        ...

    def _update_screen(self):
        self.draw_function()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

    def setup_display(self):
        if self.settings.should_full_screen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_width()
            self.settings.screen_height = self.screen.get_height()
        else:
            self.settings.screen_width = 1200
            self.settings.screen_height = 800
            self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))


if __name__ == '__main__':
    mg = MemoryGame()
    mg.start_game()
