import pygame
from sys import exit
from dataclasses import dataclass
import random


@dataclass
class GameSettings:
    should_full_screen: bool = False
    bg_color = pygame.Color('black')


class MemoryGame:
    def __init__(self, engine, height=4, width=4):
        if height * width % 2 != 0:
            print("Invalid board size")

        self.width = width
        self.height = height
        self.game_board = list()
        self.engine = engine
        self.create_board()

    def create_board(self):
        board_size = self.width * self.height

        self.game_board = [random.randrange(0, 99) for _ in range(int(board_size/2))]
        self.game_board.extend(self.game_board)
        random.shuffle(self.game_board)
        print(len(self.game_board))
        print(self.game_board)

    def start_game(self):
        self.engine.run_game()


class MemoryGameEngine:
    def __init__(self):
        pygame.init()
        self.screen = None
        self.clock = pygame.time.Clock()
        self.game_active = False
        self.settings = GameSettings()

        self.setup_display()
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
        self.screen.fill(self.settings.bg_color)
        pygame.display.flip()

    def _setup_game(self):
        ...

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
    mg = MemoryGame(MemoryGameEngine())
    mg.start_game()
