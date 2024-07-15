import pygame
from sys import exit
from dataclasses import dataclass
import random

from mgcard import MGCard, card_image
from mgengine import MemoryGameEngine
from mebutton import MeButton

font = None
font_color = None
wait_time = 60 * 2


@dataclass
class GameSettings:
    should_full_screen: bool = False
    bg_color = pygame.Color('white')


class GameOverScreen:
    def __init__(self, game):
        self.game = game
        self.screen = game.engine.screen
        self.screen_rect = self.screen.get_rect()

        self.width, self.height = 200, 50
        self.button_color = pygame.Color('white')
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 128)

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        self.msg_img = self.font.render("You won!!", True, self.text_color, self.button_color)
        self.msg_img_rect = self.msg_img.get_rect()
        self.msg_img_rect.center = self.rect.center
        self.msg_img_rect.centery -= 200

    def draw_go_screen(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_img, self.msg_img_rect)


class MemoryGame:
    def __init__(self, height=4, width=4):
        if height * width % 2 != 0:
            print("Invalid board size")

        print("Setting up board")
        self.width = width
        self.height = height
        self.game_board = list()
        self.settings = GameSettings()
        self.engine = MemoryGameEngine(self.draw_board, self.handle_input, self.update_state,
                                       self.settings, "Memory Game")

        print("Setting up cards")
        self.cards = pygame.sprite.Group()
        self.create_board()
        self.flipped_cards = 0
        self.last_clicked_card = None
        card_image.convert()

        self.has_won = False
        self.reset_next_refresh = False
        self.wait_counter = 0

        global font
        font = pygame.font.SysFont('Arial', 20)
        global font_color
        font_color = pygame.Color('black')

        self.attempts_count = 0

        self.sb = Scoreboard(self)
        self.play_button = MeButton(self, "Play")
        self.is_active = False

        self.go_screen = GameOverScreen(self)

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
        card = MGCard(self.engine.screen, 0,0,0)
        card_width = card.rect.width
        current_x = 1
        current_y = 1
        for j in range(self.height):
            for k in range(self.width):
                idx = j * self.width + k
                print(f"idx: {idx}, value {self.game_board[idx]}")
                new_card = MGCard(self.engine.screen, self.game_board[idx],current_x,current_y)

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

        if self.has_won:
            self.engine.screen.fill(self.settings.bg_color)
            self.cards.draw(self.engine.screen)
            self.go_screen.draw_go_screen()
            self.is_active = False
        else:
            self.engine.screen.fill(self.settings.bg_color)
            self.cards.draw(self.engine.screen)
            self.sb.show_score()

        if not self.is_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                exit()
            elif event.key == pygame.K_w:
                for card in self.cards:
                    card.show_card()
            elif event.key == pygame.K_s:
                self.cards.empty()
            elif event.key == pygame.K_r:
                self.reset_game()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_active:
                self.card_clicked()
            else:
                mouse_pos = pygame.mouse.get_pos()
                if self.play_button.rect.collidepoint(mouse_pos):
                    self.is_active = True
                    self.engine.should_pause = False
                    self.reset_game()

    def card_clicked(self):
        if self.reset_next_refresh:
            return
        mouse_pos = pygame.mouse.get_pos()
        clicked_card = [card for card
                        in self.cards if card.rect.collidepoint(mouse_pos)]
        if not clicked_card:
            return
        if self.last_clicked_card is None:
            self.last_clicked_card = clicked_card[0]
        self.flipped_cards = clicked_card[0].clicked(self.flipped_cards)
        print(clicked_card[0].card_value)

        if self.flipped_cards == 2:
            self.check_cards(clicked_card[0])

    def check_cards(self, card):
        print(f"Checking {card.card_value} against {self.last_clicked_card.card_value}")
        if self.last_clicked_card.card_value == card.card_value:
            self.last_clicked_card.kill()
            card.kill()
            self.last_clicked_card = None
            self.flipped_cards = 0
            self.update_attempts()

    def update_state(self):
        if len(self.cards) == 0:
            self.has_won = True
            self.is_active = False

        if self.flipped_cards == 2 and self.reset_next_refresh:
            print("Should reset")
            for card in self.cards:
                card.reset()
            self.flipped_cards = 0
            self.reset_next_refresh = False
            self.last_clicked_card = None
            self.wait_counter = 0
            self.update_attempts()
            print(f"Attempts count is now {self.attempts_count}")
        elif self.flipped_cards == 2:
            if self.wait_counter != wait_time:
                self.wait_counter += 1
            else:
                self.reset_next_refresh = True

    def update_attempts(self):
        self.attempts_count += 1
        self.sb.prep_score()

    def reset_game(self):
        self.cards.empty()
        self.attempts_count = 0
        self.has_won = False
        self.last_clicked_card = None
        self.flipped_cards = 0
        self.create_board()


class Scoreboard:
    def __init__(self, mgGame: MemoryGame):
        self.screen = mgGame.engine.screen
        self.screen_rect = self.screen.get_rect()
        self.game = mgGame
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont('Arial', 24)
        self.prep_score()

    def prep_score(self):
        score_str = str(self.game.attempts_count)
        self.score_image = self.font.render(score_str, True, self.text_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)


if __name__ == '__main__':
    mg = MemoryGame()
    mg.start_game()
